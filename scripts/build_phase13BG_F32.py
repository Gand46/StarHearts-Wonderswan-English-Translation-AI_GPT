#!/usr/bin/env python3
"""Direct JP -> F32. e-Pet labels/layout and shared Gnome description."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
from make_bps import make,apply
JP='64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
F31='fbf949271412eb023cb94765782126a689eead61e8c6a56b2a12b85ed23acd52'
TARGET='8b7afc0975bdaa91c25aad5b9b5aa722af310421db472bbc917752432ebdbc7a'
sha=lambda b:hashlib.sha256(b).hexdigest()

def integrate(before,root):
    assert len(before)==0x400000 and sha(before)==F31,'F31 precondition'
    manifest=json.loads((root/'phase13BG_F32_changes.json').read_text());rom=bytearray(before);allowed=set()
    for row in manifest['changes']:
        p=row['offset'];n=row['size'];assert 0<=p<=len(rom)-n
        assert sha(before[p:p+n])==row['preimage_sha256'],'preimage'
        data=(root/row['asset']).read_bytes()if'asset'in row else bytes.fromhex(row['replacement_hex'])
        assert len(data)==n and sha(data)==row['after_sha256'],'replacement'
        assert not allowed.intersection(range(p,p+n)),'overlapping ranges'
        allowed.update(range(p,p+n));rom[p:p+n]=data
    differences={i for i,(a,b)in enumerate(zip(before,rom))if a!=b}
    assert differences<=allowed and len(differences)==1226
    assert int.from_bytes(rom[-2:],'little')==sum(rom[:-2])&65535==0x3D99
    assert sha(rom)==TARGET,'F32 target identity'
    assert rom[0x395CA0:0x395CA3]==before[0x395CA0:0x395CA3]and rom[0x39FF00:0x39FF35]==before[0x39FF00:0x39FF35]
    return bytes(rom)

def main():
    p=argparse.ArgumentParser();p.add_argument('original',type=Path);p.add_argument('-o','--output',type=Path,default=Path('StarHearts_EN_phase13BG_F32_rebuilt.wsc'));p.add_argument('--bps',type=Path);args=p.parse_args()
    root=Path(__file__).resolve().parents[1];jp=args.original.read_bytes();assert sha(jp)==JP,'JP source identity'
    patchpath=args.bps or args.output.with_suffix('.bps')
    assert args.original.resolve()!=args.output.resolve()and patchpath.resolve()not in(args.original.resolve(),args.output.resolve()),'refuse input/output alias'
    with tempfile.TemporaryDirectory()as d:
        prior=Path(d)/'F31.wsc'
        subprocess.run([sys.executable,str(root/'scripts/build_phase13BG_F31.py'),str(args.original),'-o',str(prior)],check=True,capture_output=True,timeout=180)
        target=integrate(prior.read_bytes(),root)
    patch=make(jp,target);assert apply(jp,patch)==target
    args.output.write_bytes(target);patchpath.write_bytes(patch)
    print('F32',sha(target),'checksum=3D99; direct JP BPS',sha(patch))
if __name__=='__main__':main()
