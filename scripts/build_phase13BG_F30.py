#!/usr/bin/env python3
"""Cumulative JP ROM -> F30: F29 plus two-glyph shop value labels."""
from pathlib import Path
import argparse
import hashlib
import struct
import subprocess
import sys
import tempfile

ORIGINAL = "64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255"
F29 = "4704a7d4e06696455ac6017632135c03259e42783f7af095b0231246e754eadb"
TARGET = "17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa"

BUYPRICE_OFFSET = 0x3769E2
REPAIR_OFFSET = 0x3769F4
FIELD_SIZE = 18
OLD_BUYPRICE = bytes.fromhex("82 61 82 74 82 78 82 6F 82 71 82 68 82 62 82 64 00 00")
OLD_REPAIR = bytes.fromhex("82 71 82 64 82 6F 82 60 82 68 82 71 81 40 81 40 00 00")
FULLWIDTH_SPACE = bytes.fromhex("81 40")
NEW_BUYPRICE = bytes.fromhex("82 61 82 6F") + FULLWIDTH_SPACE * 6 + bytes(2)  # BP
NEW_REPAIR = bytes.fromhex("82 71 82 6F") + FULLWIDTH_SPACE * 6 + bytes(2)  # RP


def sha(data):
    return hashlib.sha256(data).hexdigest()


def integrate(f29):
    assert sha(f29) == F29
    assert len(NEW_BUYPRICE) == FIELD_SIZE and len(NEW_REPAIR) == FIELD_SIZE
    assert f29[BUYPRICE_OFFSET:BUYPRICE_OFFSET + FIELD_SIZE] == OLD_BUYPRICE
    assert f29[REPAIR_OFFSET:REPAIR_OFFSET + FIELD_SIZE] == OLD_REPAIR
    rom = bytearray(f29)
    rom[BUYPRICE_OFFSET:BUYPRICE_OFFSET + FIELD_SIZE] = NEW_BUYPRICE
    rom[REPAIR_OFFSET:REPAIR_OFFSET + FIELD_SIZE] = NEW_REPAIR
    rom[-2:] = struct.pack("<H", sum(rom[:-2]) & 0xFFFF)
    assert sha(rom) == TARGET
    return bytes(rom)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original")
    parser.add_argument("-o", "--output", default="StarHearts_EN_phase13BG_F30_rebuilt.wsc")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    original = Path(args.original).read_bytes()
    assert sha(original) == ORIGINAL
    with tempfile.TemporaryDirectory() as directory:
        f29_path = Path(directory) / "F29.wsc"
        subprocess.run(
            [sys.executable, str(root / "scripts" / "build_phase13BG_F29.py"), args.original, "-o", str(f29_path)],
            check=True,
            capture_output=True,
        )
        result = integrate(f29_path.read_bytes())
    Path(args.output).write_bytes(result)
    checksum = struct.unpack("<H", result[-2:])[0]
    print(args.output, len(result), sha(result), f"checksum={checksum:04X}")


if __name__ == "__main__":
    main()
