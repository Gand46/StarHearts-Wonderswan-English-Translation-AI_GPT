#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,hashlib,struct,unicodedata
ap=argparse.ArgumentParser();ap.add_argument('rom');ap.add_argument('--csv',required=True);a=ap.parse_args();r=Path(a.rom).read_bytes();assert len(r)==0x400000
DB=0x39F0C3
# dictionary facts used by F10/F11
exp={0x79:'IR',0x2F:'ST',0x61:'RI',0x37:'AL',0x4C:'EN'}
for idx,s in exp.items():
 b=r[DB+idx*9:DB+(idx+1)*9];assert b[0]==len(s) and b[1:1+len(s)]==s.encode(),(idx,b.hex(),s)
eventpats=[bytes.fromhex('82 64 82 75 82 64 82 6D 82 73 81 46'), bytes.fromhex('82 64 82 75 F0 4C 82 73 81 46')]
events=[]
for eventpat in eventpats:
 p=0
 while True:
  p=r.find(eventpat,p,0x210000)
  if p<0:break
  e=r.find(b'\x1a\x1a',p,min(p+128,0x210000));assert e>p
  body=r[p:e]
  toks=[body[i+1] for i in range(len(body)-1) if body[i]==0xF0]
  events.append((p,0x79 in toks,body));p+=1
events.sort(key=lambda x:x[0])
# F10 repaired banner is explicit First
fix1=0x19069E
assert r[fix1:fix1+18]==bytes.fromhex('82 65 82 89 82 92 82 93 82 94 81 40 82 73 F0 61 F0 37')
# F11 repaired second banner prefix + First + Trial
fix2=0x191DFC
new=bytes.fromhex('82 64 82 75 F0 4C 82 73 81 46 81 40 82 65 82 89 82 92 F0 2F 81 40 82 73 F0 61 F0 37')
assert r[fix2:fix2+len(new)]==new
# no EVENT banner should retain F079 after F11
assert not any(has79 for _,has79,_ in events),[(hex(p),b.hex()) for p,h,b in events if h]
# Remaining normal-dialogue First signatures
sig=bytes.fromhex('82 65 F0 79 F0 2F');offs=[];p=0
while True:
 p=r.find(sig,p,0x210000)
 if p<0:break
 if p>=0x190000:offs.append(p)
 p+=1
# F10 had 16; F11 removes the event one => 15
assert len(offs)==15,len(offs)
rows=[]
for p in offs:
 pre=r[max(0,p-20):p]
 rows.append({'offset':f'0x{p:06X}','bank':f'0x{p>>16:02X}','class':'NORMAL_DIALOGUE_FIRST','event_prefix_within_20_bytes':'NO','action':'NO_CHANGE_F11','runtime_status':'NOT_PROVEN_DEFECTIVE'})
with open(a.csv,'w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('event_banners=',len(events));print('event_banners_with_F079=0');print('remaining_normal_dialogue_First=',len(offs));print('sha256=',hashlib.sha256(r).hexdigest());print('checksum=',f'{struct.unpack("<H",r[-2:])[0]:04X}')
