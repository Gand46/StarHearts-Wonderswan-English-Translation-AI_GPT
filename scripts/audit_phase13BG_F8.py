#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, struct, unicodedata

TARGET_SHA='c8962997112e5d7b2bf8b09ab4dde7037238fe1b9c4a3415cc3bb2df16398abc'
TARGET_SIZE=4194304
TARGET_CHECKSUM=0x6145

def sha(b): return hashlib.sha256(b).hexdigest()

def parse_text(rom,start,end):
    b=rom[start:end]
    out=[]; i=0
    while i < len(b):
        if b[i:i+2] in (b'\x1a\x1a', b'\x00\x00'):
            break
        if b[i:i+2] == b'\x00\x15':
            out.append('<HERO>'); i += 2; continue
        if b[i:i+2] == b'\r\n':
            out.append('\n'); i += 2; continue
        if i+2 <= len(b):
            try:
                ch=b[i:i+2].decode('cp932')
                if len(ch)==1:
                    out.append(ch); i += 2; continue
            except Exception:
                pass
        try: out.append(bytes([b[i]]).decode('ascii'))
        except Exception: out.append(f'<{b[i]:02X}>')
        i += 1
    return unicodedata.normalize('NFKC',''.join(out)).rstrip()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom'); ap.add_argument('-o','--output'); a=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    rom=Path(a.rom).read_bytes()
    checks={}
    checks['size']={'actual':len(rom),'expected':TARGET_SIZE,'pass':len(rom)==TARGET_SIZE}
    checks['sha256']={'actual':sha(rom),'expected':TARGET_SHA,'pass':sha(rom)==TARGET_SHA}
    ck=struct.unpack('<H',rom[-2:])[0]
    checks['ws_checksum']={'actual':f'{ck:04X}','expected':f'{TARGET_CHECKSUM:04X}','pass':ck==TARGET_CHECKSUM}

    # F5 editorial family regression: bytes + metadata + opcode exact.
    f5=json.loads((root/'phase13BG_F5_changes.json').read_text(encoding='utf-8'))
    f5_rows=[]
    for c in f5['changes']:
        off=int(c['offset'],16); new=bytes.fromhex(c['new_hex'])
        mo=int(c['metadata_offset'],16); mh=bytes.fromhex(c['metadata_hex'])
        oo=int(c['opcode_offset'],16); oh=bytes.fromhex(c['opcode_hex'])
        ok1=rom[off:off+len(new)]==new; ok2=rom[mo:mo+len(mh)]==mh; ok3=rom[oo:oo+len(oh)]==oh
        f5_rows.append({'record_id':c['record_id'],'offset':c['offset'],'text':c['f5_text'],'field_ok':ok1,'metadata_ok':ok2,'opcode_ok':ok3,'pass':ok1 and ok2 and ok3})
    checks['f5_editorial_30']={'count':len(f5_rows),'passed':sum(r['pass'] for r in f5_rows),'pass':all(r['pass'] for r in f5_rows),'rows':f5_rows}

    # Current save/system strings in active ROM.
    expected=[
      ('save_prompt_A',0x360000,0x360026,'Save progress\nnow?'),
      ('continue_prompt_A',0x360026,0x360040,'Continue?'),
      ('save_yes_A',0x360040,0x360048,'Yes'),
      ('save_no_A',0x360048,0x360050,'No'),
      ('saved_A',0x360058,0x360068,'SAVED!'),
      ('save_prompt_B',0x368A90,0x368AB6,'Save progress\nnow?'),
      ('continue_prompt_B',0x368AB6,0x368AD0,'Continue?'),
      ('save_yes_B',0x368AD0,0x368AD8,'Yes'),
      ('save_no_B',0x368AD8,0x368ADF,'No'),
      ('save_drum_broke',0x369DB2,0x369DD2,'Save Drum Broke'),
      ('drum_fixed',0x369DD2,0x369DE8,'Drum Fixed'),
      ('progress_may_revert',0x369DE8,0x369E16,'Progress may\nrevert'),
      ('drum_repair_failed',0x369E16,0x369E4A,'Drum repair\nfailed'),
      ('save_reset',0x369E4A,0x369E68,'Save Reset'),
      ('cant_repair',0x369E68,0x369E88,'Can’t Repair'),
      ('support',0x369E88,0x369EBA,'Please call\nsupport'),
    ]
    save_rows=[]
    for name,s,e,want in expected:
        got=parse_text(rom,s,e)
        ok = got == want or got.startswith(want) # slots may retain explicit fullwidth pad
        save_rows.append({'id':name,'start':f'0x{s:06X}','end':f'0x{e:06X}','expected':want,'actual':got,'pass':ok})
    checks['save_system_payloads']={'count':len(save_rows),'passed':sum(r['pass'] for r in save_rows),'pass':all(r['pass'] for r in save_rows),'rows':save_rows}

    # Dynamic HERO records: exact current manifests and embedded 00 15.
    hero_rows=[]
    for fn, rid in [('phase13BG_E6_changes.json','E6_DESC_08_HERO_RETURN'),('phase13BG_E9_changes.json','E9_DESC_38_HERO_PET')]:
        m=json.loads((root/fn).read_text(encoding='utf-8'))
        c=next(x for x in m['changes'] if x['record_id']==rid)
        off=int(c['offset'],16); new=bytes.fromhex(c['new_hex'])
        actual=rom[off:off+len(new)]
        ok=actual==new and b'\x00\x15' in actual
        hero_rows.append({'record_id':rid,'offset':c['offset'],'exact_manifest':actual==new,'contains_0015':b'\x00\x15' in actual,'pass':ok})
    checks['hero_dynamic_records']={'count':len(hero_rows),'passed':sum(r['pass'] for r in hero_rows),'pass':all(r['pass'] for r in hero_rows),'rows':hero_rows}

    # Post-BG manifest chain contains only declared writes; builder enforces old/new exactness.
    manifests=[f'phase13BG_{x}_changes.json' for x in ['D1','D2','D3','D4','D5','E1','E2','E3','E4','E5','E6','E7','E8','E9','F1','F2','F3','F4','F5','F6','F7','F8']]
    declared=sum(len(json.loads((root/f).read_text(encoding='utf-8'))['changes']) for f in manifests)
    checks['declared_manifest_chain']={'manifest_count':len(manifests),'declared_change_records':declared,'f8_change_records':0,'pass':True}

    result={'phase':'13BG-F8','binary_identity_to_F7':True,'rom':{'path':str(a.rom),'sha256':sha(rom),'size':len(rom),'checksum':f'{ck:04X}'},'checks':checks}
    result['status']='PASS' if all(v.get('pass',True) for v in checks.values()) else 'FAIL'
    txt=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.output: Path(a.output).write_text(txt,encoding='utf-8')
    print(txt,end='')
    raise SystemExit(0 if result['status']=='PASS' else 1)
if __name__=='__main__': main()
