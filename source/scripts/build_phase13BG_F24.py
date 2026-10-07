#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, struct, zlib

ORIGINAL_SHA = "64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255"
BG_B_SHA = "df61c34818fb907208f1047d9abe6757d18cde1cd48be5be3f1970e4829644e4"
TARGET_SHA = "3db95bd8c4935d262939acd253ea9428bf9131c0e3af35b0b858ea383cd0ea80"

def sha256(data): return hashlib.sha256(data).hexdigest()

def dec(data, pos):
    value = 0; shift = 1
    while True:
        byte = data[pos]; pos += 1; value += (byte & 0x7F) * shift
        if byte & 0x80: return value, pos
        shift <<= 7; value += shift

def apply_bps(source, patch):
    assert patch[:4] == b"BPS1"; pos = 4
    source_size, pos = dec(patch, pos); target_size, pos = dec(patch, pos)
    metadata_size, pos = dec(patch, pos); pos += metadata_size
    assert source_size == len(source)
    output = bytearray(); source_relative = target_relative = 0; end = len(patch) - 12
    while pos < end:
        command, pos = dec(patch, pos); mode = command & 3; length = (command >> 2) + 1
        if mode == 0: output += source[len(output):len(output) + length]
        elif mode == 1: output += patch[pos:pos + length]; pos += length
        elif mode == 2:
            delta, pos = dec(patch, pos); source_relative += -(delta >> 1) if delta & 1 else delta >> 1
            output += source[source_relative:source_relative + length]; source_relative += length
        else:
            delta, pos = dec(patch, pos); target_relative += -(delta >> 1) if delta & 1 else delta >> 1
            for _ in range(length): output.append(output[target_relative]); target_relative += 1
    source_crc, target_crc, patch_crc = struct.unpack("<III", patch[-12:])
    assert len(output) == target_size
    assert source_crc == (zlib.crc32(source) & 0xFFFFFFFF)
    assert target_crc == (zlib.crc32(output) & 0xFFFFFFFF)
    assert patch_crc == (zlib.crc32(patch[:-4]) & 0xFFFFFFFF)
    return bytes(output)

def main():
    parser = argparse.ArgumentParser(description="Rebuild Star Hearts 13BG-F24 from clean JP ROM")
    parser.add_argument("original")
    parser.add_argument("-o", "--output", default="StarHearts_EN_phase13BG_F24_rebuilt.wsc")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = Path(args.original).read_bytes(); assert sha256(source) == ORIGINAL_SHA
    rom = bytearray(apply_bps(source, (root / "baseline/StarHearts_EN_phase13BG_B_2026-09-15.bps").read_bytes()))
    assert sha256(rom) == BG_B_SHA
    manifests = [
        "manifests/D/phase13BG_D1_changes.json", "manifests/D/phase13BG_D2_changes.json", "manifests/D/phase13BG_D3_changes.json",
        "manifests/D/phase13BG_D4_changes.json", "manifests/D/phase13BG_D5_changes.json", "manifests/E/phase13BG_E1_changes.json",
        "manifests/E/phase13BG_E2_changes.json", "manifests/E/phase13BG_E3_changes.json", "manifests/E/phase13BG_E4_changes.json",
        "manifests/E/phase13BG_E5_changes.json", "manifests/E/phase13BG_E6_changes.json", "manifests/E/phase13BG_E7_changes.json",
        "manifests/E/phase13BG_E8_changes.json", "manifests/E/phase13BG_E9_changes.json", "manifests/F/phase13BG_F1_changes.json",
        "manifests/F/phase13BG_F2_changes.json", "manifests/F/phase13BG_F3_changes.json", "manifests/F/phase13BG_F4_changes.json",
        "manifests/F/phase13BG_F5_changes.json", "manifests/F/phase13BG_F6_changes.json", "manifests/F/phase13BG_F7_changes.json",
        "manifests/F/phase13BG_F8_changes.json", "manifests/F/phase13BG_F9_changes.json", "manifests/F/phase13BG_F10_changes.json",
        "manifests/F/phase13BG_F11_changes.json", "manifests/F/phase13BG_F12_changes.json", "manifests/F/phase13BG_F13_changes.json",
        "manifests/F/phase13BG_F14_changes.json", "manifests/F/phase13BG_F15_changes.json", "manifests/F/phase13BG_F16_changes.json",
        "manifests/F/phase13BG_F17_changes.json", "manifests/F/phase13BG_F18_changes.json", "manifests/F/phase13BG_F20_changes.json",
        "manifests/F/phase13BG_F21_changes.json", "manifests/F/phase13BG_F22_changes.json", "manifests/F/phase13BG_F23_changes.json",
        "manifests/F/phase13BG_F24_changes.json"
    ]
    for filename in manifests:
        manifest = json.loads((root / filename).read_text(encoding="utf-8"))
        for change in manifest["changes"]:
            offset = int(change["offset"], 16)
            new = bytes.fromhex(change["new_hex"])
            if "old_hex" in change:
                old = bytes.fromhex(change["old_hex"])
            else:
                old = bytes([int(change["old_fill"], 16)]) * change["bytes"]
            assert len(old) == len(new) == change.get("bytes", len(old))
            assert rom[offset:offset + len(old)] == old, (filename, hex(offset))
            rom[offset:offset + len(new)] = new
        rom[-2:] = struct.pack("<H", sum(rom[:-2]) & 0xFFFF)
    output = bytes(rom); assert sha256(output) == TARGET_SHA, sha256(output)
    Path(args.output).write_bytes(output)
    print(args.output, len(output), sha256(output), f"checksum={struct.unpack('<H', output[-2:])[0]:04X}")

if __name__ == "__main__": main()
