#!/usr/bin/env python3
"""Cumulative JP ROM -> F27: F26 source plus native-font Magic graphic."""
from pathlib import Path
import argparse,hashlib,subprocess,sys,tempfile,struct
from magic_header_codec import decode,encode
from build_phase13BG_F26 import apply_bps

def sha(data):return hashlib.sha256(data).hexdigest()
ORIGINAL='64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
F26='0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1'
TARGET='641acc39309f64cc16bfeee0f450461c99dd20d4ee4a28e7d0481a54471625d4'
CODED='1b15782a8da146dcc01d1ebc9997ab37bd882dd538e7e2f73ea5e499d1320ef1'
TILES='a5cc8923b5eb746da17fc09eede753cadb4a74d1f9fc9d2286e882700fa23221'

def integrate(f26,tiles):
 assert sha(f26)==F26 and sha(tiles)==TILES and len(tiles)==576
 rom=bytearray(f26)
 assert rom[0x308422:0x308424]==bytes.fromhex('58 02')
 assert rom[0x3096fe:0x309707]==bytes.fromhex('00 00 02 00 00 09 00 01 35')
 old=bytes(rom[0x309707:0x309833]);plain,n=decode(old)
 assert n==len(old) and len(plain)==14336
 target=bytearray(plain)
 for row in range(2):
  for col in range(9):
   idx=(row*9+col)*32;tile=(col+1 if row==0 else col+29)
   target[tile*32:tile*32+32]=tiles[idx:idx+32]
 coded=encode(bytes(target))
 assert sha(coded)==CODED and decode(coded)[0]==bytes(target)
 second=bytes(rom[0x309833:0x309856]);offset=9+len(coded)
 resource=b'\x00\x00\x02\x00\x00\x09'+offset.to_bytes(3,'big')+coded+second
 start=0x30f13e
 assert len(resource)==589 and rom[start:start+len(resource)]==b'\xff'*len(resource)
 assert (start-0x30843e)//8==0x0da0 and (start-0x30843e)%8==0
 rom[0x308422:0x308424]=(0x0da0).to_bytes(2,'little')
 rom[start:start+len(resource)]=resource
 rom[-2:]=struct.pack('<H',sum(rom[:-2])&0xffff)
 assert sha(rom)==TARGET and struct.unpack('<H',rom[-2:])[0]==0x99b2
 actual={i for i,(a,b) in enumerate(zip(f26,rom)) if a!=b}
 expected=set(range(0x308422,0x308424))|set(range(start,start+len(resource)))|set(range(len(rom)-2,len(rom)))
 assert actual<=expected and set(range(0x308422,0x308424))<=actual and set(range(len(rom)-2,len(rom)))<=actual
 return bytes(rom)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('original');ap.add_argument('-o','--output',default='StarHearts_EN_phase13BG_F27_rebuilt.wsc');a=ap.parse_args()
 root=Path(__file__).resolve().parents[1]
 jp=Path(a.original).read_bytes();assert sha(jp)==ORIGINAL
 with tempfile.TemporaryDirectory() as d:
  f26path=Path(d)/'F26.wsc'
  subprocess.run([sys.executable,str(root/'scripts/build_phase13BG_F26.py'),a.original,'-o',str(f26path)],check=True,capture_output=True)
  f27=integrate(f26path.read_bytes(),(root/'assets/magic_header_tiles.bin').read_bytes())
 Path(a.output).write_bytes(f27)
 print(a.output,len(f27),sha(f27),'checksum=99B2')

if __name__=='__main__':main()
