#!/usr/bin/env python3
"""F35 -> F36: two observed shop labels, exact native CP932 glyph pixels."""
import argparse
import hashlib
import json
from pathlib import Path
from magic_header_codec import decode
from build_epet_labels import encode

F35 = '6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084'
sha = lambda b: hashlib.sha256(b).hexdigest()

def get_pixel(data, width, x, y):
    p = (y // 8 * (width // 8) + x // 8) * 32 + y % 8 * 4 + x % 8 // 2
    return (data[p] >> (4 if x % 2 == 0 else 0)) & 15

def put_pixel(data, width, x, y, value):
    p = (y // 8 * (width // 8) + x // 8) * 32 + y % 8 * 4 + x % 8 // 2
    data[p] = (data[p] & 15) | (value << 4) if x % 2 == 0 else (data[p] & 240) | value

def frame(rom, resource, index):
    assert index < int.from_bytes(rom[resource + 1:resource + 3], 'big')
    p = resource + int.from_bytes(rom[resource + 3 + index * 3:resource + 6 + index * 3], 'big')
    data, used = decode(rom[p:])
    return p, used, data

def integrate(before, root):
    assert len(before) == 0x400000 and sha(before) == F35, 'F35 precondition'
    font_path = root / 'assets/F32/native_latin_glyphs.json'
    font = json.loads(font_path.read_text())
    assert sha((root / 'assets/F32/native_latin_atlas.png').read_bytes()) == font['reference_sha256']
    glyphs = font['glyphs']
    p, capacity, prompt = frame(before, 0x30843E, 15)
    # Exact native question-mark ink from the original JP purchase graphic.
    question = [(x - 37, y - 2) for y in range(3, 12) for x in range(37, 42)
                if get_pixel(prompt, 56, x, y) == 7]
    assert len(question) == 12
    glyphs['?'] = {'width': 5, 'points': question}
    specifications = [
        (0x30F38E, 2, 'バザー', 'Bazaar', 224, 128, (8, 0, 80, 14), 8, 2, 0, 11, None),
        (0x30843E, 15, '買う？', 'Buy?', 56, 16, (4, 1, 52, 14), None, 1, 1, 7, 6),
    ]
    target = bytearray(before)
    allowed = {len(before) - 2, len(before) - 1}
    ledger = []
    previews = []
    for res, idx, jp, en, width, height, box, start_x, start_y, background, ink, shadow in specifications:
        offset, capacity, old = frame(before, res, idx)
        assert (offset, len(old)) in ((0x30F931, 14336), (0x308E2B, 448))
        new = bytearray(old)
        x0, y0, x1, y1 = box
        ink_width = sum(glyphs[ch]['width'] for ch in en) + len(en) - 1
        cursor = (width - ink_width) // 2 if start_x is None else start_x
        origin = cursor
        assert x0 <= cursor and cursor + ink_width <= x1
        for y in range(y0, y1):
            for x in range(x0, x1):
                put_pixel(new, width, x, y, background)
        points = []
        for ch in en:
            points += [(cursor + dx, start_y + dy) for dx, dy in glyphs[ch]['points']]
            cursor += glyphs[ch]['width'] + 1
        if shadow is not None:
            for x, y in points:
                assert x0 <= x + 1 < x1 and y0 <= y + 1 < y1
                put_pixel(new, width, x + 1, y + 1, shadow)
        for x, y in points:
            assert x0 <= x < x1 and y0 <= y < y1
            put_pixel(new, width, x, y, ink)
        changed_pixels = []
        for y in range(height):
            for x in range(width):
                if get_pixel(old, width, x, y) != get_pixel(new, width, x, y):
                    assert x0 <= x < x1 and y0 <= y < y1, 'outside label rectangle'
                    changed_pixels.append([x, y])
        coded = encode(bytes(new))
        assert len(coded) <= capacity, ('compressed capacity', en, len(coded), capacity)
        assert decode(coded)[0] == new
        assert not allowed.intersection(range(offset, offset + len(coded)))
        allowed.update(range(offset, offset + len(coded)))
        target[offset:offset + len(coded)] = coded
        assert frame(target, res, idx)[2] == new
        ledger.append({'japanese': jp, 'english': en, 'resource': hex(res), 'frame': idx,
                       'offset': offset, 'capacity': capacity, 'encoded_bytes': len(coded),
                       'decoded_bytes': len(new), 'preimage_sha256': sha(before[offset:offset + len(coded)]),
                       'after_sha256': sha(coded), 'decoded_sha256': sha(new),
                       'box': box, 'origin': [origin, start_y], 'ink_width': ink_width,
                       'changed_pixels': len(changed_pixels), 'outside_box_changed_pixels': 0,
                       'unchanged_compressed_tail_bytes': capacity - len(coded)})
        previews.append((en, width, height, old, bytes(new)))
    target[-2:] = (sum(target[:-2]) & 65535).to_bytes(2, 'little')
    differences = {i for i, (x, y) in enumerate(zip(before, target)) if x != y}
    assert differences <= allowed
    # Every other frame of both shared resource containers remains byte-identical after decoding.
    for res, modified in ((0x30843E, 15), (0x30F38E, 2)):
        for idx in range(int.from_bytes(before[res + 1:res + 3], 'big')):
            if idx != modified:
                assert frame(before, res, idx)[2] == frame(target, res, idx)[2]
    report = {'base_sha256': sha(before), 'target_sha256': sha(target), 'changed_bytes': len(differences),
              'checksum': f'{int.from_bytes(target[-2:], "little"):04X}', 'changes': ledger,
              'native_atlas_sha256': font['reference_sha256'], 'native_glyphs': {ch: glyphs[ch] for ch in 'Bazruy?'},
              'question_mark_source': {'resource': '0x30843E', 'frame': 15, 'rectangle': [37, 3, 42, 12]},
              'unexpected_changed_offsets': 0, 'other_resource_frames_unchanged': True,
              'code_pointers_palettes_unchanged': True}
    return bytes(target), report, previews

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('f35', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    assert args.f35.resolve() != args.output.resolve()
    target, report, _ = integrate(args.f35.read_bytes(), Path(__file__).resolve().parents[1])
    args.output.write_bytes(target)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('target_sha256', 'changed_bytes', 'checksum')}))

if __name__ == '__main__':
    main()
