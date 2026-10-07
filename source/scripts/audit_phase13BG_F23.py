#!/usr/bin/env python3
"""Validate the I06/F23 inline opcode-name integration."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path


JP_SHA = "64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255"
F22_SHA = "3219fb1a0b49793ee7a9245e5468907c23a28f2b9125743d3cd17837e6485296"
F23_SHA = "48238577e0e8ea736f4809621dc045369b4674a91fc06975c1f552b7cb958f28"
CHECKSUM = 0x34B3


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fullwidth(text: str) -> str:
    return "".join("　" if c == " " else chr(ord(c) + 0xFEE0) for c in text)


def simulate_op22(data: bytes, offset: int) -> bytes:
    output = bytearray()
    for index in range(8):
        cursor = offset + index * 2
        word = (data[cursor] << 8) | data[cursor + 1]
        if word < 0x8140:
            break
        output.extend(data[cursor : cursor + 2])
    return bytes(output)


def has_japanese(text: str) -> bool:
    return any("\u3040" <= c <= "\u30ff" or "\u3400" <= c <= "\u9fff" for c in text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("jp")
    parser.add_argument("f22")
    parser.add_argument("f23")
    parser.add_argument("-o", "--output", default="I06_STATIC_VALIDATION.json")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifests/F/phase13BG_F23_changes.json").read_text(encoding="utf-8"))
    jp = Path(args.jp).read_bytes()
    f22 = Path(args.f22).read_bytes()
    f23 = Path(args.f23).read_bytes()
    assert sha256(jp) == JP_SHA
    assert sha256(f22) == F22_SHA
    assert sha256(f23) == F23_SHA
    assert len(manifest["entries"]) == len(manifest["changes"]) == 45

    expected_diff: set[int] = set()
    records = []
    for entry, change in zip(manifest["entries"], manifest["changes"], strict=True):
        assert entry["record_id"] == change["record_id"]
        offset = int(entry["operand_offset"], 16)
        terminator = int(entry["terminator_offset"], 16)
        old = bytes.fromhex(change["old_hex"])
        new = bytes.fromhex(change["new_hex"])
        assert offset == int(change["offset"], 16)
        assert len(old) == len(new) == change["bytes"] == entry["capacity_glyphs"] * 2
        assert f22[offset:terminator] == old
        assert f23[offset:terminator] == new
        assert f22[offset - 2 : offset] == f23[offset - 2 : offset] == b"\x22\x00"
        assert f22[terminator : terminator + 4] == f23[terminator : terminator + 4] == b"\x21\x00\x00\x00"
        expected_diff.update(offset + i for i, (a, b) in enumerate(zip(old, new)) if a != b)

        copied = simulate_op22(f23, offset)
        assert copied == new
        decoded = copied.decode("cp932")
        assert decoded.rstrip("　") == fullwidth(entry["integrated_display"])
        assert not has_japanese(decoded)
        if entry["companion_offset"]:
            companion = int(entry["companion_offset"], 16)
            span = int(entry["companion_padded_span"])
            assert f22[companion : companion + span] == f23[companion : companion + span]
        records.append({**entry, "result": "PASS", "delimiter_preserved": True})

    expected_diff.update(i for i in range(len(f23) - 2, len(f23)) if f22[i] != f23[i])
    actual_diff = {i for i, (a, b) in enumerate(zip(f22, f23)) if a != b}
    assert actual_diff == expected_diff
    checksum = struct.unpack_from("<H", f23, len(f23) - 2)[0]
    assert checksum == (sum(f23[:-2]) & 0xFFFF) == CHECKSUM
    by_bank = Counter(record["bank"] for record in records)
    by_strategy = Counter(record["strategy"] for record in records)
    assert by_bank == {"0x19": 24, "0x1A": 21}
    assert by_strategy == {"I06_FIELD_COMPACT_PADDED": 31, "I02_DIRECT_PADDED": 14}

    result = {
        "phase": "13BG-F23",
        "result": "PASS",
        "f23_sha256": sha256(f23),
        "wonderswan_checksum": f"{checksum:04X}",
        "records": records,
        "counts": {
            "integrated": len(records), "final": len(records), "excluded": 0,
            "bank_0x19": by_bank["0x19"], "bank_0x1A": by_bank["0x1A"],
            "direct_i02": by_strategy["I02_DIRECT_PADDED"],
            "field_compact": by_strategy["I06_FIELD_COMPACT_PADDED"],
            "japanese_survivors_in_operands": 0,
        },
        "checks": {
            "consumer_proven": True,
            "fullwidth_cp932_roundtrip": True,
            "exact_inline_capacity_preserved": True,
            "opcode_0x0022_preserved": True,
            "delimiter_0x0021_0x0000_preserved": True,
            "companion_fields_unchanged": True,
            "unexpected_changed_offsets": 0,
            "checksum_valid": True,
        },
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS records=45 banks=24+21 direct=14 compact=31 changed={len(actual_diff)} checksum={checksum:04X}")


if __name__ == "__main__":
    main()
