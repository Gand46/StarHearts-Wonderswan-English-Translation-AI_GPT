#!/usr/bin/env python3
"""Cumulative JP ROM -> F29: F28 plus native-font SELL category graphic."""
from pathlib import Path
import argparse
import hashlib
import struct
import subprocess
import sys
import tempfile

ORIGINAL = "64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255"
F28 = "1936a7ea0e1a254f07ee4a2aeb3c293c95c6b4b63acb215fad18c740662fc3b4"
TARGET = "4704a7d4e06696455ac6017632135c03259e42783f7af095b0231246e754eadb"
ASSET = "afb35868f0bf83fa9f9f438e89f0594ea186b7670d9e55d78f4182cacd521819"
DESCRIPTOR_OFFSET = 0x30843C
OLD_DESCRIPTOR = 0x066E
NEW_DESCRIPTOR = 0x0DEA
RESOURCE_BASE = 0x30843E
RESOURCE_OFFSET = 0x30F38E
RESOURCE_SIZE = 2048


def sha(data):
    return hashlib.sha256(data).hexdigest()


def integrate(f28, resource):
    assert sha(f28) == F28
    assert sha(resource) == ASSET and len(resource) == RESOURCE_SIZE
    assert int.from_bytes(f28[DESCRIPTOR_OFFSET:DESCRIPTOR_OFFSET + 2], "little") == OLD_DESCRIPTOR
    assert RESOURCE_BASE + NEW_DESCRIPTOR * 8 == RESOURCE_OFFSET
    assert f28[RESOURCE_OFFSET:RESOURCE_OFFSET + RESOURCE_SIZE] == bytes([0xFF]) * RESOURCE_SIZE
    rom = bytearray(f28)
    rom[DESCRIPTOR_OFFSET:DESCRIPTOR_OFFSET + 2] = NEW_DESCRIPTOR.to_bytes(2, "little")
    rom[RESOURCE_OFFSET:RESOURCE_OFFSET + RESOURCE_SIZE] = resource
    rom[-2:] = struct.pack("<H", sum(rom[:-2]) & 0xFFFF)
    assert sha(rom) == TARGET
    return bytes(rom)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original")
    parser.add_argument("-o", "--output", default="StarHearts_EN_phase13BG_F29_rebuilt.wsc")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    original = Path(args.original).read_bytes()
    assert sha(original) == ORIGINAL
    with tempfile.TemporaryDirectory() as directory:
        f28_path = Path(directory) / "F28.wsc"
        subprocess.run(
            [sys.executable, str(root / "scripts" / "build_phase13BG_F28.py"), args.original, "-o", str(f28_path)],
            check=True,
            capture_output=True,
        )
        result = integrate(f28_path.read_bytes(), (root / "assets" / "sell_category_resource.bin").read_bytes())
    Path(args.output).write_bytes(result)
    checksum = struct.unpack("<H", result[-2:])[0]
    print(args.output, len(result), sha(result), f"checksum={checksum:04X}")


if __name__ == "__main__":
    main()
