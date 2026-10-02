#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,struct,hashlib
ap=argparse.ArgumentParser(description='F7 diagnostic only: overwrite all BANK38 JP map suffix payload bytes while preserving x/y/type and record terminators.')
ap.add_argument('rom'); ap.add_argument('records_csv'); ap.add_argument('-o','--output',required=True); a=ap.parse_args()
b=bytearray(Path(a.rom).read_bytes()); base=0x380000; changed=0; records=0
with Path(a.records_csv).open(encoding='utf-8') as f: rows=list(csv.DictReader(f))
for row in rows:
    if row['suffix_class']!='JP_SUFFIX': continue
    p=int(row['pointer'],16); start=base+p+3; tail=b[start:start+64]; ends=[]
    for pat in (b'\x00\x00',b'\xff\xff'):
        j=tail.find(pat)
        if j>=0: ends.append(j)
    e=min(ends) if ends else min(40,len(tail))
    for i in range(e):
        new=ord('Z') if i%2==0 else ord('X')
        if b[start+i]!=new: b[start+i]=new; changed+=1
    records+=1
b[-2:]=struct.pack('<H',sum(b[:-2])&0xffff)
out=Path(a.output); out.write_bytes(b)
print('records',records,'changed_bytes',changed,'sha256',hashlib.sha256(b).hexdigest(),'checksum',f'{struct.unpack("<H",b[-2:])[0]:04X}')
