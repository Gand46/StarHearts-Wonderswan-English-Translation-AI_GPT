#!/usr/bin/env python3
"""Validate all181 mappings and native readback CSV against exact F35/F36; no ROM writes."""
import argparse,csv,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('f35',type=Path);p.add_argument('f36',type=Path);p.add_argument('--evidence',type=Path,default=Path(__file__).parent);a=p.parse_args()
b=a.f35.read_bytes();r=a.f36.read_bytes();assert hashlib.sha256(b).hexdigest()=='6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084';assert hashlib.sha256(r).hexdigest()=='da2966870ef022e68f84e07ead6d017a686c47f55a6036f57974c57c6d4578d2'
rows=list(csv.DictReader(open(a.evidence/'translation_mapping_181.csv')));hits=list(csv.DictReader(open(a.evidence/'runtime_all_f36/copies.csv')));index={x['offset']:x for x in hits};assert len(rows)==len(hits)==len(index)==181
for x in rows:
 o=int(x['offset'],16);before=bytes.fromhex(x['expected_before_hex16']);after=bytes.fromhex(x['after_hex16']);assert len(before)==len(after)==16;assert b[o:o+16]==before and r[o:o+16]==after;assert b[o-8:o]==r[o-8:o]and b[o+16:o+20]==r[o+16:o+20];h=index[x['offset']];assert h['result']=='PASS'and h['source_reads']=='8'and h['actual'].lower()==after.hex()and h['expected']==h['actual']
assert r[0x1b7d32:0x1b7d3c].hex()=='82738289829282818297';assert b[0x1b7d3c:0x1b7d40]==r[0x1b7d3c:0x1b7d40]==bytes.fromhex('1c003c00')
print(json.dumps({'status':'PASS','rows':181,'native_readback_pass':181,'metadata_preserved':181,'extra_op22':'PASS','visual_scope':'representative only','natural_reachability':'NOT_VALIDATED'}))
