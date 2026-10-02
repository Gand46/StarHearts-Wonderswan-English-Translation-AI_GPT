#!/usr/bin/env python3
"""Bounded static validation for Star Hearts 13BG-F21 (Bank 0x37)."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


F20_SHA = "3b8eafc74ba8d276d4b639bd806bfaf639786106a15e2ade9471198ad5e44a30"
F21_SHA = "00f46965177716ec459ac2a0f6e89a4e50548af205582e6d0ba176c015fc36ec"
TARGET_CHECKSUM = 0x5B38
POINTERS = {
    0x3AAA2C: (0x69D0, 0x7000),
    0x3AA9CE: (0x69E2, 0x7000),
    0x3AA974: (0x69F4, 0x7000),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("f20")
    parser.add_argument("f21")
    parser.add_argument("-o", "--output", default="I04_STATIC_VALIDATION.json")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "phase13BG_F21_changes.json").read_text(encoding="utf-8"))
    f20 = Path(args.f20).read_bytes()
    f21 = Path(args.f21).read_bytes()
    assert len(f20) == len(f21) == 4 * 1024 * 1024
    assert sha256(f20) == F20_SHA
    assert sha256(f21) == F21_SHA

    expected_diff: set[int] = {len(f21) - 2, len(f21) - 1}
    records = []
    for change in manifest["changes"]:
        offset = int(change["offset"], 16)
        old = bytes.fromhex(change["old_hex"])
        new = bytes.fromhex(change["new_hex"])
        assert len(old) == len(new) == change["bytes"]
        assert f20[offset : offset + len(old)] == old
        assert f21[offset : offset + len(new)] == new
        expected_diff.update(offset + i for i, pair in enumerate(zip(old, new)) if pair[0] != pair[1])
        terminator = new.find(b"\x00\x00")
        assert terminator >= 0 and terminator % 2 == 0
        decoded = new[:terminator].decode("cp932")
        records.append(
            {
                "record_id": change["record_id"],
                "offset": change["offset"],
                "bytes": change["bytes"],
                "display": change["display"],
                "decoded": decoded.rstrip("\u3000"),
                "nul_terminated": True,
                "result": "PASS",
            }
        )

    actual_diff = {i for i, pair in enumerate(zip(f20, f21)) if pair[0] != pair[1]}
    assert actual_diff == expected_diff
    pointer_results = []
    for offset, expected in POINTERS.items():
        before = struct.unpack_from("<HH", f20, offset)
        after = struct.unpack_from("<HH", f21, offset)
        assert before == after == expected
        physical = ((0x30 + (after[1] >> 12)) << 16) | after[0]
        assert physical in {0x3769D0, 0x3769E2, 0x3769F4}
        pointer_results.append(
            {
                "code_offset": f"0x{offset:06X}",
                "far_pointer": f"{after[1]:04X}:{after[0]:04X}",
                "physical_target": f"0x{physical:06X}",
                "unchanged": True,
            }
        )

    checksum = struct.unpack_from("<H", f21, len(f21) - 2)[0]
    assert checksum == (sum(f21[:-2]) & 0xFFFF) == TARGET_CHECKSUM
    result = {
        "phase": "13BG-F21",
        "result": "PASS",
        "rom": {
            "size": len(f21),
            "f20_sha256": sha256(f20),
            "f21_sha256": sha256(f21),
            "wonderswan_checksum": f"{checksum:04X}",
        },
        "records": records,
        "far_pointers": pointer_results,
        "checks": {
            "manifest_records": len(records),
            "manifest_records_pass": sum(r["result"] == "PASS" for r in records),
            "actual_changed_bytes_including_checksum": len(actual_diff),
            "unexpected_changed_offsets": 0,
            "field_boundaries_preserved": True,
            "nul_terminators_preserved": True,
            "following_table_at_0x37001C_preserved": f20[0x37001C:0x370040] == f21[0x37001C:0x370040],
            "shop_neighbor_bytes_preserved": f20[0x3769C0:0x3769D0] == f21[0x3769C0:0x3769D0]
            and f20[0x376A06:0x376A20] == f21[0x376A06:0x376A20],
            "far_pointers_unchanged": True,
            "pointer_targets_in_bounds": True,
            "font_data_unchanged": True,
            "repointing": False,
            "checksum_valid": True,
        },
        "gate_limits": {
            "static_encoding": "PASS_I04",
            "pointer_integrity": "PASS_I04_FAR_POINTERS",
            "runtime_visual": "OPEN_UNTIL_I04_RUNTIME_VALIDATION",
        },
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"PASS records={len(records)} changed={len(actual_diff)} "
        f"unexpected=0 checksum={checksum:04X} f21={sha256(f21)}"
    )


if __name__ == "__main__":
    main()
