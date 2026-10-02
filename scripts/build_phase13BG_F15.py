#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,struct,zlib
ORIGINAL_SHA='64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255'
BG_B_SHA='df61c34818fb907208f1047d9abe6757d18cde1cd48be5be3f1970e4829644e4'
TARGET_SHA='fbb161d7b8dd10f279c436519d738c31aa321302019d53ca22d41300bfd55460'
def h(b): return hashlib.sha256(b).hexdigest()
def dec(data,pos):
 v=0;shift=1
 while True:
  x=data[pos];pos+=1;v+=(x&0x7f)*shift
  if x&0x80:return v,pos
  shift<<=7;v+=shift
def apply_bps(src,patch):
 assert patch[:4]==b'BPS1';pos=4
 ss,pos=dec(patch,pos);ts,pos=dec(patch,pos);ml,pos=dec(patch,pos);pos+=ml
 assert ss==len(src);out=bytearray();sr=tr=0;end=len(patch)-12
 while pos<end:
  x,pos=dec(patch,pos);mode=x&3;n=(x>>2)+1
  if mode==0:out+=src[len(out):len(out)+n]
  elif mode==1:out+=patch[pos:pos+n];pos+=n
  elif mode==2:
   d,pos=dec(patch,pos);sr+=-(d>>1) if d&1 else d>>1;out+=src[sr:sr+n];sr+=n
  else:
   d,pos=dec(patch,pos);tr+=-(d>>1) if d&1 else d>>1
   for _ in range(n):out.append(out[tr]);tr+=1
 sc,tc,pc=struct.unpack('<III',patch[-12:]);assert len(out)==ts
 assert sc==(zlib.crc32(src)&0xffffffff) and tc==(zlib.crc32(out)&0xffffffff) and pc==(zlib.crc32(patch[:-4])&0xffffffff)
 return bytes(out)
def main():
 ap=argparse.ArgumentParser(description='Rebuild Star Hearts 13BG-F15 from clean JP ROM');ap.add_argument('original');ap.add_argument('-o','--output',default='StarHearts_EN_phase13BG_F15_rebuilt.wsc');a=ap.parse_args()
 root=Path(__file__).resolve().parents[1]
 src=Path(a.original).read_bytes();assert h(src)==ORIGINAL_SHA,('wrong original',h(src))
 rom=bytearray(apply_bps(src,(root/'baseline/StarHearts_EN_phase13BG_B_2026-09-15.bps').read_bytes()));assert h(rom)==BG_B_SHA
 manifests=['phase13BG_D1_changes.json','phase13BG_D2_changes.json','phase13BG_D3_changes.json','phase13BG_D4_changes.json','phase13BG_D5_changes.json','phase13BG_E1_changes.json','phase13BG_E2_changes.json','phase13BG_E3_changes.json','phase13BG_E4_changes.json','phase13BG_E5_changes.json','phase13BG_E6_changes.json','phase13BG_E7_changes.json','phase13BG_E8_changes.json','phase13BG_E9_changes.json','phase13BG_F1_changes.json','phase13BG_F2_changes.json','phase13BG_F3_changes.json','phase13BG_F4_changes.json','phase13BG_F5_changes.json','phase13BG_F6_changes.json','phase13BG_F7_changes.json','phase13BG_F8_changes.json','phase13BG_F9_changes.json','phase13BG_F10_changes.json','phase13BG_F11_changes.json','phase13BG_F12_changes.json','phase13BG_F13_changes.json','phase13BG_F14_changes.json','phase13BG_F15_changes.json']
 for fn in manifests:
  m=json.loads((root/fn).read_text(encoding='utf-8'))
  for c in m['changes']:
   off=int(c['offset'],16);old=bytes.fromhex(c['old_hex']);new=bytes.fromhex(c['new_hex'])
   assert rom[off:off+len(old)]==old,(fn,hex(off),rom[off:off+len(old)].hex(),old.hex())
   assert len(old)==len(new),(fn,hex(off),'in-place manifest expected')
   rom[off:off+len(new)]=new
  rom[-2:]=struct.pack('<H',sum(rom[:-2])&0xffff)
 out=bytes(rom);assert h(out)==TARGET_SHA,(h(out),TARGET_SHA)
 Path(a.output).write_bytes(out)
 print(a.output,len(out),h(out),f'checksum={struct.unpack("<H",out[-2:])[0]:04X}')
if __name__=='__main__':main()
