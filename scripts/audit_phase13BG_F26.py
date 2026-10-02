#!/usr/bin/env python3
"""Validate the I09/F26 inline opcode-name integration."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path


JP_SHA = "64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255"
F25_SHA = "b9fef4f219daf66575f5c2e7c7666dff868f0013732ec8d5f75be4ba9e3d3dc1"
F26_SHA = "0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1"
CHECKSUM = 0x6ABA


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
    parser.add_argument("f25")
    parser.add_argument("f26")
    parser.add_argument("-o", "--output", default="I09_STATIC_VALIDATION.json")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "phase13BG_F26_changes.json").read_text(encoding="utf-8"))
    jp = Path(args.jp).read_bytes()
    f25 = Path(args.f25).read_bytes()
    f26 = Path(args.f26).read_bytes()
    assert sha256(jp) == JP_SHA
    assert sha256(f25) == F25_SHA
    assert sha256(f26) == F26_SHA
    assert len(manifest["entries"]) == len(manifest["changes"]) == 52

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
        assert f25[offset:terminator] == old
        assert f26[offset:terminator] == new
        assert f25[offset - 2 : offset] == f26[offset - 2 : offset] == b"\x22\x00"
        assert f25[terminator : terminator + 4] == f26[terminator : terminator + 4] == b"\x21\x00\x00\x00"
        expected_diff.update(offset + i for i, (a, b) in enumerate(zip(old, new)) if a != b)

        copied = simulate_op22(f26, offset)
        assert copied == new
        decoded = copied.decode("cp932")
        assert decoded.rstrip("　") == fullwidth(entry["integrated_display"])
        assert not has_japanese(decoded)
        if entry["companion_offset"]:
            companion = int(entry["companion_offset"], 16)
            span = int(entry["companion_padded_span"])
            assert f25[companion : companion + span] == f26[companion : companion + span]
        records.append({**entry, "result": "PASS", "delimiter_preserved": True})

    expected_diff.update(i for i in range(len(f26) - 2, len(f26)) if f25[i] != f26[i])
    actual_diff = {i for i, (a, b) in enumerate(zip(f25, f26)) if a != b}
    assert actual_diff == expected_diff
    checksum = struct.unpack_from("<H", f26, len(f26) - 2)[0]
    assert checksum == (sum(f26[:-2]) & 0xFFFF) == CHECKSUM
    by_bank = Counter(record["bank"] for record in records)
    by_strategy = Counter(record["strategy"] for record in records)
    assert by_bank == {"0x1F": 37, "0x20": 15}
    assert by_strategy == {"I09_FIELD_COMPACT_PADDED": 37, "I02_DIRECT_PADDED": 15}

    result = {
        "phase": "13BG-F26",
        "result": "PASS",
        "f26_sha256": sha256(f26),
        "wonderswan_checksum": f"{checksum:04X}",
        "records": records,
        "counts": {
            "integrated": len(records), "final": len(records), "excluded": 0,
            "bank_0x1F": by_bank["0x1F"], "bank_0x20": by_bank["0x20"],
            "direct_i02": by_strategy["I02_DIRECT_PADDED"],
            "field_compact": by_strategy["I09_FIELD_COMPACT_PADDED"],
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
    print(f"PASS records=52 banks=37+15 direct=15 compact=37 changed={len(actual_diff)} checksum={checksum:04X}")


if __name__ == "__main__":
    main()
