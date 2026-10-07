#!/usr/bin/env python3
"""Cumulative JP ROM -> F28: F27 plus visually valid two-cell shop count label."""
from pathlib import Path
import argparse,hashlib,struct,subprocess,sys,tempfile

ORIGINAL='64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
F27='641acc39309f64cc16bfeee0f450461c99dd20d4ee4a28e7d0481a54471625d4'
TARGET='1936a7ea0e1a254f07ee4a2aeb3c293c95c6b4b63acb215fad18c740662fc3b4'
OLD=bytes.fromhex('82 6E 82 76 82 6D 82 64 82 63 81 40 81 40 81 40')
NEW=bytes.fromhex('82 6D 82 6E 81 40 81 40 81 40 81 40 81 40 81 40')
OFFSET=0x3769D0
def sha(data): return hashlib.sha256(data).hexdigest()

def integrate(f27):
 assert sha(f27)==F27 and f27[OFFSET:OFFSET+16]==OLD
 rom=bytearray(f27);rom[OFFSET:OFFSET+16]=NEW
 rom[-2:]=struct.pack('<H',sum(rom[:-2])&0xffff)
 assert sha(rom)==TARGET and struct.unpack('<H',rom[-2:])[0]==0x9932
 actual={i for i,(a,b) in enumerate(zip(f27,rom)) if a!=b}
 assert actual=={0x3769D1,0x3769D3,0x3769D4,0x3769D5,0x3769D6,0x3769D7,0x3769D8,0x3769D9,0x3FFFFE}
 return bytes(rom)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('original');ap.add_argument('-o','--output',default='StarHearts_EN_phase13BG_F28_rebuilt.wsc');a=ap.parse_args()
 root=Path(__file__).resolve().parents[1];jp=Path(a.original).read_bytes();assert sha(jp)==ORIGINAL
 with tempfile.TemporaryDirectory() as d:
  f27path=Path(d)/'F27.wsc'
  subprocess.run([sys.executable,str(root/'scripts/build_phase13BG_F27.py'),a.original,'-o',str(f27path)],check=True,capture_output=True)
  f28=integrate(f27path.read_bytes())
 Path(a.output).write_bytes(f28)
 print(a.output,len(f28),sha(f28),'checksum=9932')
if __name__=='__main__':main()
