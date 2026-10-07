#!/usr/bin/env python3
"""Cumulative Japanese ROM -> F35 menu typography revision (internal test)."""
from pathlib import Path
import argparse,hashlib,subprocess,sys,tempfile,struct
from make_bps import make,apply
H=lambda x:hashlib.sha256(x).hexdigest()
JP='64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
F34='d22bb029570e1b053e7cc11bd0cd1632ff310343d3c44ffaa072f771ae820ca0'
F35='6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('original',type=Path);ap.add_argument('-o','--output',type=Path,required=True);ap.add_argument('--bps',type=Path);a=ap.parse_args()
 root=Path(__file__).resolve().parents[1];src=a.original.read_bytes();assert len(src)==0x400000 and H(src)==JP
 patch=a.bps or a.output.with_suffix('.bps');assert a.output.resolve()!=a.original.resolve() and patch.resolve()not in (a.original.resolve(),a.output.resolve())
 with tempfile.TemporaryDirectory() as tmp:
  td=Path(tmp);prior=td/'F34.wsc'
  subprocess.run([sys.executable,str(root/'scripts/build_phase13BG_F34.py'),str(a.original),'-o',str(prior)],check=True,capture_output=True,timeout=180)
  old=prior.read_bytes();assert H(old)==F34
  subprocess.run([sys.executable,str(root/'scripts/rebuild_main_menu_font.py'),str(prior),str(td)],check=True,capture_output=True,timeout=60)
  target=(td/'F35_menu_integrated.wsc').read_bytes();assert H(target)==F35
 assert len(target)==len(src) and struct.unpack_from('<H',target,len(target)-2)[0]==sum(target[:-2])&0xffff
 allowed=lambda i: (0x30903c<=i<0x3094f5)or(0x30fc0f<=i<0x30fe80)or i>=len(src)-2
 diff=[i for i,(x,y)in enumerate(zip(old,target))if x!=y]
 assert diff and all(allowed(i) for i in diff),('out-of-scope modification',diff[:10])
 bps=make(src,target);assert apply(src,bps)==target
 a.output.write_bytes(target);patch.write_bytes(bps)
 print('F35',H(target),'checksum',target[-2:].hex(),'BPS',H(bps),'changed_bytes',len(diff))
if __name__=='__main__':main()
