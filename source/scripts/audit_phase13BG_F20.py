#!/usr/bin/env python3
"""Static and bounded-diff validation for Star Hearts 13BG-F20."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


F18_SHA = "fbb161d7b8dd10f279c436519d738c31aa321302019d53ca22d41300bfd55460"
F20_SHA = "3b8eafc74ba8d276d4b639bd806bfaf639786106a15e2ade9471198ad5e44a30"
MTE_START = 0x39F0C3
MTE_SIZE = 256 * 9


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("f18")
    parser.add_argument("f20")
    parser.add_argument("-o", "--output", default="I03_STATIC_VALIDATION.json")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifests/F/phase13BG_F20_changes.json").read_text(encoding="utf-8"))
    f18 = Path(args.f18).read_bytes()
    f20 = Path(args.f20).read_bytes()

    assert len(f18) == len(f20) == 4 * 1024 * 1024
    assert sha256(f18) == F18_SHA
    assert sha256(f20) == F20_SHA
    checksum = struct.unpack("<H", f20[-2:])[0]
    assert checksum == (sum(f20[:-2]) & 0xFFFF) == 0x60D5
    assert len(manifest["changes"]) == 11

    allowed: set[int] = {len(f20) - 2, len(f20) - 1}
    records = []
    for change in manifest["changes"]:
        offset = int(change["offset"], 16)
        old = bytes.fromhex(change["old_hex"])
        new = bytes.fromhex(change["new_hex"])
        assert len(old) == len(new) == change["bytes"]
        assert f18[offset : offset + len(old)] == old
        assert f20[offset : offset + len(new)] == new
        allowed.update(range(offset, offset + len(new)))
        records.append(
            {
                "record_id": change["record_id"],
                "offset": change["offset"],
                "bytes": len(new),
                "canonical": change["canonical"],
                "display": change["display"],
                "result": "PASS",
            }
        )

    actual_diff = {index for index, (before, after) in enumerate(zip(f18, f20)) if before != after}
    unexpected = sorted(actual_diff - allowed)
    assert not unexpected

    speaker_offsets = [0x217C2A, 0x218286, 0x2182C6, 0x218338, 0x218568, 0x218CBE]
    speaker_lengths = [16, 10, 10, 10, 10, 10]
    for offset, length in zip(speaker_offsets, speaker_lengths):
        assert f20[offset + length - 2 : offset + length] == b"\x00\x00"
        assert f20[offset + length : offset + length + 8] == f18[offset + length : offset + length + 8]

    link = f20[0x219610:0x219634]
    assert len(link) == 36
    assert link.count(b"\xFE") == 6
    assert link.count(b"\r\n") == 1
    assert f20[0x219634:0x219636] == f18[0x219634:0x219636] == b"\x1A\x1A"

    assert f20[0x219306:0x21930E] == f18[0x219306:0x21930E]
    assert f20[0x219442:0x21944A] == f18[0x219442:0x21944A]
    assert f20[0x219440:0x219442] == b"\x00\x00"

    assert f20[MTE_START : MTE_START + MTE_SIZE] == f18[MTE_START : MTE_START + MTE_SIZE]

    result = {
        "phase": "13BG-F20",
        "result": "PASS",
        "rom": {
            "size": len(f20),
            "f18_sha256": sha256(f18),
            "f20_sha256": sha256(f20),
            "wonderswan_checksum": f"{checksum:04X}",
        },
        "records": records,
        "checks": {
            "manifest_records": 11,
            "manifest_records_pass": len(records),
            "actual_changed_bytes_including_checksum": len(actual_diff),
            "unexpected_changed_offsets": len(unexpected),
            "speaker_nul_terminators_preserved": True,
            "following_opcodes_and_parameters_preserved": True,
            "link_crlf_preserved": True,
            "link_fe_parameter_count": 6,
            "link_1a1a_terminator_preserved": True,
            "menu_neighbor_bytes_preserved": True,
            "mte_dictionary_unchanged": True,
            "pointer_repointing": False,
            "checksum_valid": True,
        },
        "gate_limits": {
            "static_encoding": "PASS_I03",
            "pointer_integrity": "PASS_I03_IN_PLACE_NO_REPOINT",
            "runtime_visual": "SEE_I03_RUNTIME_VALIDATION_PASS",
        },
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
