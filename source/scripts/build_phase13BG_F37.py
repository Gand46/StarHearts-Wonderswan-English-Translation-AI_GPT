#!/usr/bin/env python3
"""Clean JP -> F37, with all four retained common prompts translated."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from build_remaining_prompts import integrate
from make_bps import make, apply

JP = '64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
TARGET = 'f0791dcf53045afc126ce11ed5b9eb7091c47c1c8195eaa525737c5fec5ffb57'
sha = lambda b: hashlib.sha256(b).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('original', type=Path)
    p.add_argument('-o', '--output', type=Path, required=True)
    p.add_argument('--bps', type=Path)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    jp = args.original.read_bytes()
    assert len(jp) == 0x400000 and sha(jp) == JP, 'clean Japanese ROM required'
    patch = args.bps or args.output.with_suffix('.bps')
    assert args.original.resolve() != args.output.resolve()
    assert patch.resolve() not in (args.original.resolve(), args.output.resolve())
    with tempfile.TemporaryDirectory() as td:
        previous = Path(td) / 'F36.wsc'
        subprocess.run([sys.executable, str(root / 'scripts/build_phase13BG_F36.py'), str(args.original), '-o', str(previous)],
                       check=True, capture_output=True, timeout=300)
        target, report, _ = integrate(previous.read_bytes(), root)
    assert sha(target) == TARGET
    expected = json.loads((root / 'manifests/F/phase13BG_F37_manifest.json').read_text())
    assert report['target_sha256'] == expected['target_sha256']
    assert int.from_bytes(target[-2:], 'little') == sum(target[:-2]) & 65535
    bps = make(jp, target)
    assert apply(jp, bps) == target
    args.output.write_bytes(target); patch.write_bytes(bps)
    print('F37', sha(target), 'checksum', report['checksum'], 'BPS', sha(bps), 'changed_bytes', report['changed_bytes'])

if __name__ == '__main__':
    main()
