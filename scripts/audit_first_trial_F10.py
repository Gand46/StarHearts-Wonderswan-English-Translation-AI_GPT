#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,hashlib,struct
ap=argparse.ArgumentParser();ap.add_argument('rom');ap.add_argument('--csv',default=None);a=ap.parse_args()
r=Path(a.rom).read_bytes()
assert len(r)==0x400000
DB=0x39F0C3
expect={0x79:bytes.fromhex('02 49 52 00 00 00 00 00 00'),0x2F:bytes.fromhex('02 53 54 00 00 00 00 00 00'),0x61:bytes.fromhex('02 52 49 00 00 00 00 00 00'),0x37:bytes.fromhex('02 41 4C 00 00 00 00 00 00')}
for idx,e in expect.items():
 got=r[DB+idx*9:DB+(idx+1)*9];assert got==e,(hex(idx),got.hex(),e.hex())
fixoff=0x19069E
fixed=bytes.fromhex('82 65 82 89 82 92 82 93 82 94 81 40 82 73 F0 61 F0 37')
assert r[fixoff:fixoff+len(fixed)]==fixed
sig=bytes.fromhex('82 65 F0 79 F0 2F')
h=[];p=0
while True:
 p=r.find(sig,p)
 if p<0:break
 if 0x190000<=p<0x210000:h.append(p)
 p+=1
assert len(h)==16,len(h)
rows=[]
for p in h:
 rows.append({'offset':f'0x{p:06X}','bank':f'0x{p>>16:02X}','encoding':'F + F079(ir) + F02F(st)','runtime_status':'UNTESTED_FOR_MISSING_I','action':'NO_CHANGE_F10'})
rows.insert(0,{'offset':'0x19069E','bank':'0x19','encoding':'explicit F i r s t + T + F061(ri) + F037(al)','runtime_status':'R0009_RUNTIME_DEFECT_PATCHED','action':'CHANGED_F10'})
if a.csv:
 with open(a.csv,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('dictionary_entries=PASS')
print('R0009_explicit_First=PASS')
print('remaining_compressed_First_signatures=',len(h))
print('remaining_offsets=',','.join(f'0x{x:06X}' for x in h))
print('checksum=',f'{struct.unpack("<H",r[-2:])[0]:04X}')
print('sha256=',hashlib.sha256(r).hexdigest())
