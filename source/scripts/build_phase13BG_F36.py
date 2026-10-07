#!/usr/bin/env python3
"""Clean JP -> F36: purchase graphics and all 181 proven actor-name fields."""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from build_shop_buy_graphics import integrate as integrate_graphics
from make_bps import make, apply

JP = '64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
F35 = '6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084'
sha = lambda b: hashlib.sha256(b).hexdigest()

def latin(text):
    return ''.join('\u3000' if c == ' ' else chr(ord(c) + 0xFEE0) for c in text).encode('cp932')

def integrate(prior, root):
    assert len(prior) == 0x400000 and sha(prior) == F35, 'F35 identity'
    graphic_rom, graphics, _ = integrate_graphics(prior, root)
    rom = bytearray(graphic_rom)
    folder = root / 'assets/F36'
    with (folder / 'translation_mapping_181.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 181 and len({r['offset'] for r in rows}) == 181, '181-field universe'
    # Pin the reviewed offset universe independently of display wording.
    offsets = sorted(int(r['offset'], 16) for r in rows)
    assert sha(','.join(f'{p:06X}' for p in offsets).encode()) == '36b8c7b75dbfda00a5eeae34a485d1c4d204910c44399fda8f2627a245578480', 'offset universe'
    allowed = {i for i, (a, b) in enumerate(zip(prior, graphic_rom)) if a != b}
    changes = []
    for row in rows:
        p = int(row['offset'], 16)
        old, new = bytes.fromhex(row['expected_before_hex16']), bytes.fromhex(row['after_hex16'])
        assert len(old) == len(new) == 16 and rom[p:p + 16] == old, 'name precondition'
        assert prior[p - 8:p - 6] == b'\x04\x00', 'actor creation opcode'
        assert int.from_bytes(prior[p - 2:p], 'little') == int(row['actor_id'], 16), 'actor identity'
        assert 1 <= len(row['english']) <= 8 and new == latin(row['english']).ljust(16, b'\0'), 'CP932/name width'
        assert prior[p + 16:p + 20] == bytes.fromhex(row['tail_metadata_hex4']), 'tail metadata'
        assert not allowed.intersection(range(p, p + 16)), 'overlap'
        allowed.update(range(p, p + 16)); rom[p:p + 16] = new
        assert rom[p + 16:p + 20] == prior[p + 16:p + 20]
        changes.append({'offset': p, 'size': 16, 'japanese': row['japanese'], 'english': row['english'],
                        'before_hex': old.hex(), 'after_hex': new.hex(), 'source': row['sourceENreference']})
    with (folder / 'extra_op22.csv').open(encoding='utf-8-sig', newline='') as f:
        extra = list(csv.DictReader(f))
    assert len(extra) == 1 and int(extra[0]['offset'], 16) == 0x1B7D32
    row = extra[0]; p = int(row['offset'], 16)
    old, new = bytes.fromhex(row['expected_before_hex']), bytes.fromhex(row['after_hex'])
    assert len(old) == len(new) == 10 and rom[p:p + 10] == old
    assert rom[p - 2:p] == b'\x22\x00' and rom[p + 10:p + 14] == bytes.fromhex(row['following_control_hex'])
    assert new == latin(row['english']) and row['english'] == 'Tiraw'
    assert not allowed.intersection(range(p, p + 10))
    allowed.update(range(p, p + 10)); rom[p:p + 10] = new
    changes.append({'offset': p, 'size': 10, 'japanese': row['japanese'], 'english': row['english'],
                    'before_hex': old.hex(), 'after_hex': new.hex(), 'source': row['evidence']})
    allowed.update((len(rom) - 2, len(rom) - 1))
    rom[-2:] = (sum(rom[:-2]) & 65535).to_bytes(2, 'little')
    diff = {i for i, (a, b) in enumerate(zip(prior, rom)) if a != b}
    assert diff <= allowed, 'unexplained modification'
    report = {'base_sha256': F35, 'target_sha256': sha(rom), 'checksum': f'{int.from_bytes(rom[-2:], "little"):04X}',
              'changed_bytes': len(diff), 'unexpected_changed_offsets': 0, 'companion_fields': 181,
              'additional_inline_names': 1, 'graphics': graphics, 'name_changes': changes,
              'name_metadata_preserved': True, 'no_code_or_pointer_changes': True}
    return bytes(rom), report

def main():
    p = argparse.ArgumentParser()
    p.add_argument('original', type=Path)
    p.add_argument('-o', '--output', type=Path, required=True)
    p.add_argument('--bps', type=Path)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    jp = args.original.read_bytes()
    assert len(jp) == 0x400000 and sha(jp) == JP, 'clean JP source required'
    patch = args.bps or args.output.with_suffix('.bps')
    assert args.output.resolve() != args.original.resolve() and patch.resolve() not in (args.output.resolve(), args.original.resolve())
    with tempfile.TemporaryDirectory() as tmp:
        f35 = Path(tmp) / 'F35.wsc'
        subprocess.run([sys.executable, str(root / 'scripts/build_phase13BG_F35.py'), str(args.original), '-o', str(f35)],
                       check=True, capture_output=True, timeout=240)
        target, report = integrate(f35.read_bytes(), root)
    expected = json.loads((root / 'manifests/F/phase13BG_F36_manifest.json').read_text())
    assert report['target_sha256'] == expected['target_sha256'], 'F36 identity'
    assert report['changed_bytes'] == expected['changed_bytes']
    bps = make(jp, target)
    assert apply(jp, bps) == target
    args.output.write_bytes(target); patch.write_bytes(bps)
    print('F36', sha(target), 'checksum', report['checksum'], 'BPS', sha(bps), 'changed_bytes', report['changed_bytes'])

if __name__ == '__main__':
    main()
