#!/usr/bin/env python3
"""Cumulative JP -> F31. Native menu headers and armor Def label; no warp hook."""
from pathlib import Path
import argparse,hashlib,json,struct,subprocess,sys,tempfile
from make_bps import make,apply

JP='64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
F30='17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa'
TARGET='fbf949271412eb023cb94765782126a689eead61e8c6a56b2a12b85ed23acd52'
sha=lambda b:hashlib.sha256(b).hexdigest()

def integrate(source,root):
    assert len(source)==0x400000 and sha(source)==F30,'F30 precondition'
    manifest=json.loads((root/'phase13BG_F31_changes.json').read_text());rom=bytearray(source);allowed=set()
    for change in manifest['changes']:
        p=change['offset'];n=change['size']
        assert 0<=p<=len(rom)-n and sha(source[p:p+n])==change['preimage_sha256'],'range/preimage'
        data=(root/change['asset']).read_bytes()if'asset'in change else bytes.fromhex(change['replacement_hex'])
        assert len(data)==n and sha(data)==change['after_sha256'],'asset mismatch'
        rom[p:p+n]=data;allowed.update(range(p,p+n))
    assert int.from_bytes(rom[-2:],'little')==sum(rom[:-2])&65535==0x4EA7
    assert sha(rom)==TARGET,'target identity'
    diff={i for i,(a,b)in enumerate(zip(source,rom))if a!=b}
    assert diff<=allowed and len(diff)==4350
    # Explicitly exclude P4 diagnostic ROM hooks from this translation build.
    assert rom[0x395CA0:0x395CA3]==source[0x395CA0:0x395CA3] and rom[0x39FF00:0x39FF35]==source[0x39FF00:0x39FF35]
    return bytes(rom)

def main():
    p=argparse.ArgumentParser();p.add_argument('original',type=Path);p.add_argument('-o','--output',type=Path,default=Path('StarHearts_EN_phase13BG_F31_rebuilt.wsc'));p.add_argument('--bps',type=Path);a=p.parse_args()
    assert a.original.resolve()!=a.output.resolve(),'refuse to overwrite original'
    root=Path(__file__).resolve().parents[1];jp=a.original.read_bytes();assert sha(jp)==JP,'Japanese source identity'
    with tempfile.TemporaryDirectory()as d:
        prior=Path(d)/'F30.wsc'
        subprocess.run([sys.executable,str(root/'scripts/build_phase13BG_F30.py'),str(a.original),'-o',str(prior)],check=True,capture_output=True)
        result=integrate(prior.read_bytes(),root)
    patch=make(jp,result);assert apply(jp,patch)==result
    bps=a.bps or a.output.with_suffix('.bps');assert bps.resolve()not in (a.original.resolve(),a.output.resolve())
    a.output.write_bytes(result);bps.write_bytes(patch)
    print(f'F31 {sha(result)} checksum=4EA7; direct JP BPS {sha(patch)}')
if __name__=='__main__':main()
