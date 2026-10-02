#!/usr/bin/env python3
"""Rebuild the SELL category resource with native English glyph pixels.

The glyph masks are copied from an accepted in-game menu capture, never from an
external font.  The original background, palette selection, map and bottom rule
remain unchanged.
"""
from pathlib import Path
import argparse
from PIL import Image

from magic_header_codec import decode, encode

RESOURCE = 0x30B7AE
GRAY = (128, 128, 128)


def decode_frames(rom):
    count = int.from_bytes(rom[RESOURCE + 1:RESOURCE + 3], "big")
    assert count == 4
    result = []
    for index in range(count):
        offset = int.from_bytes(rom[RESOURCE + 3 + index * 3:RESOURCE + 6 + index * 3], "big")
        result.append(decode(rom[RESOURCE + offset:])[0])
    assert [len(value) for value in result] == [2144, 1024, 14336, 64]
    return result


def set_tile_pixel(graphics, index, x, y, value):
    offset = index * 32 + y * 4 + x // 2
    old = graphics[offset]
    graphics[offset] = ((value << 4) | (old & 15)) if x % 2 == 0 else ((old & 0xF0) | value)


def set_map_pixel(graphics, tilemap, x, y, value):
    cell = (y // 8) * 32 + x // 8
    word = int.from_bytes(tilemap[cell * 2:cell * 2 + 2], "little")
    set_tile_pixel(graphics, word & 0x1FF, x & 7, y & 7, value)


def copy_mask(source, box, graphics, tilemap, destination):
    x0, y0, x1, y1 = box
    dx, dy = destination
    for y in range(y0, y1):
        for x in range(x0, x1):
            if source.getpixel((x, y)) == GRAY:
                set_map_pixel(graphics, tilemap, dx + x - x0, dy + y - y0, 8)


def build_frames(rom, reference):
    original = decode_frames(rom)
    graphics = bytearray(original[0])
    tilemap = bytearray(original[1])

    # Give every label-area map cell its own blank tile.  This avoids modifying
    # reused Japanese tile fragments elsewhere in the same resource.
    for map_y in range(1, 11):
        for map_x in range(3, 12):
            index = len(graphics) // 32
            assert index < 0x200
            graphics.extend(bytes(32))
            cell = map_y * 32 + map_x
            word = int.from_bytes(tilemap[cell * 2:cell * 2 + 2], "little")
            word = (word & ~0x1FF) | index
            tilemap[cell * 2:cell * 2 + 2] = word.to_bytes(2, "little")

    # Exact native-font masks from the already approved English menu.
    copy_mask(reference, (129, 28, 177, 36), graphics, tilemap, (24, 8),)   # Gear Items
    copy_mask(reference, (24, 28, 46, 36), graphics, tilemap, (24, 28),)    # Arms
    copy_mask(reference, (24, 44, 55, 52), graphics, tilemap, (24, 44),)    # Armor
    copy_mask(reference, (51, 28, 84, 36), graphics, tilemap, (24, 60),)    # Charms
    copy_mask(reference, (128, 60, 164, 68), graphics, tilemap, (24, 76),)  # Amulets
    return [bytes(graphics), bytes(tilemap), original[2], original[3]]


def pack_frames(values):
    header_size = 3 + len(values) * 3
    chunks = []
    offsets = []
    position = header_size
    for value in values:
        coded = encode(value)
        assert decode(coded)[0] == value
        offsets.append(position)
        chunks.append(coded)
        position += len(coded)
    result = bytearray((0, 0, len(values)))
    for offset in offsets:
        result.extend(offset.to_bytes(3, "big"))
    for chunk in chunks:
        result.extend(chunk)
    return bytes(result)


def render(graphics, tilemap):
    image = Image.new("P", (256, 128), 0)
    palette = [0, 0, 0] * 256
    palette[8 * 3:8 * 3 + 3] = [128, 128, 128]
    image.putpalette(palette)
    for cell in range(32 * 16):
        word = int.from_bytes(tilemap[cell * 2:cell * 2 + 2], "little")
        index = word & 0x1FF
        if index * 32 + 32 > len(graphics):
            continue
        tile = graphics[index * 32:index * 32 + 32]
        x0, y0 = (cell % 32) * 8, (cell // 32) * 8
        for y in range(8):
            for pair in range(4):
                value = tile[y * 4 + pair]
                image.putpixel((x0 + pair * 2, y0 + y), value >> 4)
                image.putpixel((x0 + pair * 2 + 1, y0 + y), value & 15)
    return image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("resource_output", type=Path)
    parser.add_argument("preview_output", type=Path)
    args = parser.parse_args()
    rom = args.rom.read_bytes()
    reference = Image.open(args.reference).convert("RGB")
    assert reference.size == (237, 144)
    values = build_frames(rom, reference)
    resource = pack_frames(values)
    args.resource_output.write_bytes(resource)
    render(values[0], values[1]).save(args.preview_output)
    print(args.resource_output, len(resource), [len(value) for value in values])


if __name__ == "__main__":
    main()
