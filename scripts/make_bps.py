#!/usr/bin/env python3
from pathlib import Path
import argparse,struct,zlib

def enc(v):
 o=bytearray()
 while True:
  x=v&0x7f; v>>=7
  if v==0:o.append(x|0x80);return bytes(o)
  o.append(x);v-=1

def make(src,tgt):
 assert len(src)==len(tgt)
 p=bytearray(b'BPS1');p+=enc(len(src));p+=enc(len(tgt));p+=enc(0)
 i=0;n=len(src)
 while i<n:
  if src[i]==tgt[i]:
   j=i+1
   while j<n and src[j]==tgt[j]:j+=1
   p+=enc(((j-i-1)<<2)|0);i=j
  else:
   j=i+1
   while j<n and src[j]!=tgt[j]:j+=1
   p+=enc(((j-i-1)<<2)|1);p+=tgt[i:j];i=j
 p+=struct.pack('<II',zlib.crc32(src)&0xffffffff,zlib.crc32(tgt)&0xffffffff)
 p+=struct.pack('<I',zlib.crc32(p)&0xffffffff)
 return bytes(p)

def dec(data,pos):
 v=0;shift=1
 while True:
  x=data[pos];pos+=1;v+=(x&0x7f)*shift
  if x&0x80:return v,pos
  shift<<=7;v+=shift

def apply(src,patch):
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
 assert sc==zlib.crc32(src)&0xffffffff and tc==zlib.crc32(out)&0xffffffff and pc==zlib.crc32(patch[:-4])&0xffffffff
 return bytes(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('target');ap.add_argument('output');a=ap.parse_args()
 s=Path(a.source).read_bytes();t=Path(a.target).read_bytes();p=make(s,t);Path(a.output).write_bytes(p);assert apply(s,p)==t;print(a.output,len(p),'PASS')
