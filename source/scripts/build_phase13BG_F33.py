#!/usr/bin/env python3
"""Rebuild F33 and cumulative JP patch. Only three demonstrated ending width defects change."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
from make_bps import make,apply
sha=lambda b:hashlib.sha256(b).hexdigest()
JP='64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
def integrate(prior,root):
    m=json.loads((root/'manifests/F/phase13BG_F33_changes.json').read_text());assert sha(prior)==m['base_sha256']
    rom=bytearray(prior);allowed=set()
    for c in m['changes']:
        a=c['offset'];n=c['size'];before=bytes.fromhex(c['before_hex']);after=bytes.fromhex(c['after_hex'])
        assert len(before)==len(after)==n and rom[a:a+n]==before
        assert not allowed.intersection(range(a,a+n));allowed.update(range(a,a+n));rom[a:a+n]=after
    diff={i for i,(a,b)in enumerate(zip(prior,rom))if a!=b};assert diff<=allowed
    assert int.from_bytes(rom[-2:],'little')==sum(rom[:-2])&65535
    assert sha(rom)==m['target_sha256'];return bytes(rom)
def main():
    p=argparse.ArgumentParser();p.add_argument('original',type=Path);p.add_argument('-o','--output',type=Path,required=True);p.add_argument('--bps',type=Path);a=p.parse_args()
    root=Path(__file__).resolve().parents[1];jp=a.original.read_bytes();assert sha(jp)==JP
    patch=a.bps or a.output.with_suffix('.bps');assert a.original.resolve()!=a.output.resolve()and patch.resolve()not in(a.original.resolve(),a.output.resolve())
    with tempfile.TemporaryDirectory()as d:
        previous=Path(d)/'F32.wsc';subprocess.run([sys.executable,str(root/'scripts/build_phase13BG_F32.py'),str(a.original),'-o',str(previous)],check=True,capture_output=True,timeout=180)
        target=integrate(previous.read_bytes(),root)
    bps=make(jp,target);assert apply(jp,bps)==target;a.output.write_bytes(target);patch.write_bytes(bps)
    print('F33',sha(target),'checksum',target[-2:].hex(),'BPS',sha(bps))
if __name__=='__main__':main()
