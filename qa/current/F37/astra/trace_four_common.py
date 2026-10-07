from pathlib import Path
import json,csv,hashlib,subprocess,argparse
ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--jp',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
out=args.out;out.mkdir(parents=True,exist_ok=True)
rom=args.rom;r=rom.read_bytes();w=lambda p:int.from_bytes(r[p:p+2],'little')
assert hashlib.sha256(r).hexdigest()=='da2966870ef022e68f84e07ead6d017a686c47f55a6036f57974c57c6d4578d2'
find=lambda p:[i for i in range(len(r)) if r.startswith(p,i)]
# Byte hits are candidates. Entry/callsite ranges below have been disassembled and examined.
scan={}
for name,p in [('decoder254C',bytes.fromhex('9a4c2500a0')),('decoder2618',bytes.fromhex('9a182600a0')),('resource2530',bytes.fromhex('9a302500a0')),('resource25EE',bytes.fromhex('9aee2500a0')),('common_table_far_pointer',bytes.fromhex('1c840020'))]:scan[name]=[hex(x) for x in find(p)]
b=r[0x3a0000:0x3b0000]
callers=[i for i in range(len(b)-2) if b[i]==0xe8 and (i+3+int.from_bytes(b[i+1:i+3],'little'))%65536==0x94f0]
scan['loader94F0_callers']=[hex(x+0x3a0000) for x in callers]
scan['near_decoder_transfers']=[hex(i+0x3a0000) for i in range(len(b)-2) if b[i] in [0xe8,0xe9] and (i+3+int.from_bytes(b[i+1:i+3],'little'))%65536 in [0x254c,0x2618]]
# Parse all 19 menu records independently, including mode0 omitted in historical common_consumers.json.
records=[]
for mode in range(19):
 p=0x360000+w(0x365f94+mode*2);s=p;resource=w(p);p+=2;rf=[]
 while w(p)!=65535:rf.append([w(p),hex(w(p+2))]);p+=4
 p+=2;dest=w(p);p+=2;common=[]
 if dest!=65535:
  while w(p)!=65535:common.append(w(p));p+=2
 records.append(dict(mode=mode,record=hex(s),resource=resource,resource_frames=rf,common_destination=hex(dest),common_frames=common))
scan['menu_records']=records
scan['menu_common_union']=sorted({f for rec in records for f in rec['common_frames']})
scan['F36_sha256']=hashlib.sha256(r).hexdigest()
scan['original_sha256']=hashlib.sha256(args.jp.read_bytes()).hexdigest()
(out/'scan.json').write_text(json.dumps(scan,indent=2))
with (out/'four_graphics_consumers.csv').open('w') as f:
 fields=['frame','resource_rom','block_rom','japanese','english_recommendation','consumer','static_status','natural_runtime','evidence','limitation'];wr=csv.DictWriter(f,fields);wr.writeheader()
 for frame,block,jp,en in [(12,0x308be3,'対戦？','Battle?'),(13,0x308ca9,'値段？','Price?'),(14,0x308d6b,'伝授？','Teach?'),(17,0x308f86,'戻す？','Return?')]:
  wr.writerow(dict(frame=frame,resource_rom='0x30843E',block_rom=hex(block),japanese=jp,english_recommendation=en,consumer='No selected consumer identified in audited routes',static_status='RECURSO_CONSERVADO_SIN_SELECCION_EN_RUTAS_AUDITADAS',natural_runtime='NOT_VALIDATED',evidence='scan.json; focused_disassembly.asm; static_report.txt',limitation='Does not prove globally unused; no natural operation semantics confirmed'))
# Focused disassembly explicitly restarts on known entry boundaries, avoiding data-induced drift.
sections=[(0x3a2530,0x3a25ee),(0x3a94f0,0x3a9594),(0x3a3604,0x3a3642),(0x3a3c34,0x3a3c72),(0x3a9c8e,0x3a9ccc),(0x3aa0a4,0x3aa0e2),(0x3aa634,0x3aa672),(0x3a8d06,0x3a8d54),(0x340268,0x34031a),(0x396504,0x396550)]
for c in callers: sections.append((0x3a0000+c-22,0x3a0000+c+3))
texts=[]
for start,end in sections:
 p=out/'fragment.bin';p.write_bytes(r[start:end]);s=subprocess.check_output(['objdump','-D','-b','binary','-m','i8086','-Mintel',f'--adjust-vma={start}',str(p)]).decode();texts.append(f'\nROM {start:06X}..{end:06X}\n'+s)
(out/'focused_disassembly.asm').write_text(''.join(texts));(out/'fragment.bin').unlink()
print('decoder calls',len(scan['decoder254C']),'alternate calls',len(scan['decoder2618']),'loader callsites',len(callers),'common frames',scan['menu_common_union'])
