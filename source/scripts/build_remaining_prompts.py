#!/usr/bin/env python3
"""F36 -> F37. Four retained common prompts; native glyphs, guarded local writes."""
import argparse
import hashlib
import json
from pathlib import Path
from build_shop_buy_graphics import frame, get_pixel, put_pixel
from build_epet_labels import encode
from magic_header_codec import decode

F36 = 'da2966870ef022e68f84e07ead6d017a686c47f55a6036f57974c57c6d4578d2'
sha = lambda b: hashlib.sha256(b).hexdigest()
SPEC = [
    (12, '対戦？', 'Battle?', 0x308BE3, 198),
    (13, '値段？', 'Price?', 0x308CA9, 194),
    (14, '伝授？', 'Teach?', 0x308D6B, 192),
    (17, '戻す？', 'Return?', 0x308F86, 171),
]

def integrate(before, root):
    assert len(before) == 0x400000 and sha(before) == F36, 'F36 identity'
    font = json.loads((root / 'assets/F32/native_latin_glyphs.json').read_text())
    assert sha((root / 'assets/F32/native_latin_atlas.png').read_bytes()) == font['reference_sha256']
    glyphs = font['glyphs']
    glyphs['?'] = json.loads((root / 'assets/F36/shop_graphics_manifest.json').read_text())['native_glyphs']['?']
    rom = bytearray(before)
    allowed = {len(before) - 2, len(before) - 1}
    changes = []
    previews = []
    for index, japanese, english, expected_offset, expected_capacity in SPEC:
        offset, capacity, old = frame(before, 0x30843E, index)
        assert (offset, capacity, len(old)) == (expected_offset, expected_capacity, 448)
        new = bytearray(old)
        # Preserve the original 56x16 graphic's corner masks and palette indices.
        box = [4, 1, 52, 14]
        for y in range(box[1], box[3]):
            for x in range(box[0], box[2]):
                put_pixel(new, 56, x, y, 1)
        width = sum(glyphs[c]['width'] for c in english) + len(english) - 1
        cursor = (56 - width) // 2
        origin = cursor
        points = []
        for character in english:
            points.extend((cursor + x, 1 + y) for x, y in glyphs[character]['points'])
            cursor += glyphs[character]['width'] + 1
        for x, y in points:
            assert box[0] <= x + 1 < box[2] and box[1] <= y + 1 < box[3]
            put_pixel(new, 56, x + 1, y + 1, 6)
        for x, y in points:
            put_pixel(new, 56, x, y, 7)
        changed_pixels = 0
        for y in range(16):
            for x in range(56):
                if get_pixel(old, 56, x, y) != get_pixel(new, 56, x, y):
                    assert box[0] <= x < box[2] and box[1] <= y < box[3]
                    changed_pixels += 1
        coded = encode(bytes(new))
        assert decode(coded)[0] == new
        destination = offset
        pointer_change = None
        if len(coded) > capacity:
            # F35's relocated menu map ends at 0x30FE80. Use only its verified
            # remaining FF bank tail; the decoder's source still stays in Bank30.
            assert index == 17 and len(coded) == 196
            destination = 0x30FE80
            assert destination + len(coded) <= 0x310000
            assert before[destination:destination + len(coded)] == b'\xff' * len(coded)
            pointer = 0x30843E + 3 + index * 3
            expected = (offset - 0x30843E).to_bytes(3, 'big')
            replacement = (destination - 0x30843E).to_bytes(3, 'big')
            assert before[pointer:pointer + 3] == expected
            allowed.update(range(pointer, pointer + 3))
            rom[pointer:pointer + 3] = replacement
            pointer_change = {'offset': pointer, 'before_hex': expected.hex(), 'after_hex': replacement.hex()}
        assert not allowed.intersection(range(destination, destination + len(coded)))
        allowed.update(range(destination, destination + len(coded)))
        rom[destination:destination + len(coded)] = coded
        assert frame(rom, 0x30843E, index)[2] == new
        changes.append({'frame': index, 'japanese': japanese, 'english': english,
                        'original_offset': offset, 'offset': destination, 'capacity': capacity, 'encoded_bytes': len(coded),
                        'pointer_change': pointer_change,
                        'decoded_bytes': len(new), 'source_block_sha256': sha(before[offset:offset + capacity]),
                        'replacement_sha256': sha(coded), 'decoded_sha256': sha(new),
                        'box': box, 'origin': [origin, 1], 'ink_width': width,
                        'changed_pixels': changed_pixels, 'outside_box_changed_pixels': 0,
                        'unchanged_compressed_tail_bytes': capacity if pointer_change else capacity - len(coded)})
        previews.append((index, old, bytes(new)))
    for index in range(int.from_bytes(before[0x30843F:0x308441], 'big')):
        if index not in {s[0] for s in SPEC}:
            assert frame(before, 0x30843E, index)[2] == frame(rom, 0x30843E, index)[2]
    rom[-2:] = (sum(rom[:-2]) & 65535).to_bytes(2, 'little')
    differences = {i for i, (x, y) in enumerate(zip(before, rom)) if x != y}
    assert differences <= allowed
    report = {'base_sha256': F36, 'target_sha256': sha(rom), 'changed_bytes': len(differences),
              'checksum': f'{int.from_bytes(rom[-2:], "little"):04X}', 'changes': changes,
              'native_atlas_sha256': font['reference_sha256'],
              'glyph_reference': {c: glyphs[c] for c in sorted(set(''.join(s[2] for s in SPEC)))},
              'unexpected_changed_offsets': 0, 'all_other_common_frames_unchanged': True,
              'code_palettes_unchanged': True, 'only_pointer_change': 'common frame17, 0x308474',
              'names_181_unchanged': True}
    return bytes(rom), report, previews

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('f36', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    assert args.f36.resolve() != args.output.resolve()
    target, report, _ = integrate(args.f36.read_bytes(), Path(__file__).resolve().parents[1])
    args.output.write_bytes(target)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: report[k] for k in ('target_sha256', 'changed_bytes', 'checksum')}))

if __name__ == '__main__':
    main()
