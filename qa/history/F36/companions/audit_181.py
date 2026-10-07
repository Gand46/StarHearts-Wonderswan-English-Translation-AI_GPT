#!/usr/bin/env python3
"""Read-only F35 companion audit and bounded insertion manifest; no ROM writes."""
import argparse,csv,json,hashlib,struct,unicodedata
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,default=Path('audit/roms/StarHearts_F35.wsc'));p.add_argument('--audit',type=Path,default=Path('audit/astra'));p.add_argument('--project',type=Path,default=Path('audit/private/StarHearts_AUDIT_PROJECT_v1_2026-09-26'));p.add_argument('--out',type=Path,default=Path('audit/f36_companions'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
r=a.rom.read_bytes();sha=hashlib.sha256(r).hexdigest();assert sha=='6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084'
def u(o):return struct.unpack_from('<H',r,o)[0]
def rows(f):return list(csv.DictReader(open(f,encoding='utf8')))
def save(f,rs):
 with open(a.out/f,'w',newline='',encoding='utf8')as h:
  w=csv.DictWriter(h,rs[0].keys());w.writeheader();w.writerows(rs)
def enc(s):return ''.join(chr(ord(c)+0xfee0)if '!'<=c<='~'else '\u3000'if c==' 'else c for c in s).encode('cp932')
checks={0x393182:'f831',0x3931f8:'9ada0e009083c61a',0x3973c1:'bb0000b9080090268b400689416283c302e2f4',0x391f9f:'bb0000b9080090268b400689416283c302e2f4',0x39e929:'837d6200747306568bf783c66233c08ec0bfa0739adeb700a0',0x394228:'2de001',0x39424a:'606b0080',0x3ab7e4:'bd0000b90800'}
for o,h in checks.items():assert r[o:o+len(bytes.fromhex(h))]==bytes.fromhex(h),(hex(o),r[o:o+len(bytes.fromhex(h))].hex(),h)
gloss={x['japanese']:x for x in rows(a.project/'iterations/I02/I02_GLOSSARY.csv')}
table=[x for x in rows(a.audit/'known_pointer_tables.csv')if x['family']=='entity_names'];assert len(table)==160
entries=rows(a.audit/'companion_fields_unresolved.csv');assert len(entries)==181
res=[]
for x in entries:
 o=int(x['offset'],16);jp=x['japanese'];id=u(o-2);assert u(o-8)==4
 raw=r[o:o+16];text=raw.split(b'\0\0')[0].decode('cp932');assert text==jp
 primary='';status='PROVEN_CONSUMER_INITIAL_NAME';review='PASS';note='';sourcejp=jp
 if 0x1e0<=id<0x280:
  t=table[id-0x1e0];sourcejp=t['original_japanese'];assert jp.startswith(sourcejp),(jp,sourcejp)
  en=unicodedata.normalize('NFKC',t['current_text']);primary=f"entity ID {id:#06x}; table slot {t['slot']}; real target {t['target']}"
  if len(en)>8:
   g=gloss[sourcejp];en=g['encoded_display'];primary+='; '+g['term_id']+' approved 8-glyph display'
  note='Actor ID indexing independently confirmed by 394228/39424A; field JP starts with canonical JP. Not inferred from nearest OP22.'
 elif jp in gloss:
  g=gloss[jp];en=g['encoded_display'];primary=g['term_id'];note='Exact JP match to approved glossary; not inferred from nearest OP22.'
 elif jp=='ティラワカミ':
  g=gloss['ティラワカ'];en=g['encoded_display'];primary=g['term_id']+'; actor ID0014; inline JP at1B7D32';note='Same actor0014 and same Tirawaka prefix; suffixミ differs from later display alias.'
 elif jp=='ジムス':en='Jimusu';primary='NEW_EDITORIAL_ROMANIZATION';review='ROOT_EDITORIAL_APPROVED';note='Do not adopt nearby Pergypt Soldier; distinct source JP proper name.'
 elif jp=='えいへい':en='Guard';primary='ROOT_APPROVED_Guard_0x365C9A';review='ROOT_EDITORIAL_APPROVED';note='Guard initial label; later ???? is deliberate anonymity, not canonical translation of this field.'
 elif jp=='ポコ':en='Poco';primary='ROOT_VERIFIED_DIALOGUE_0x1E714E_0x1E74BC_MISSION_0x36518C';review='ROOT_EDITORIAL_APPROVED';note='Direct romanization; following opcode0021 0001 hides speaker name in inspected local path.'
 else:raise ValueError((hex(o),jp))
 b=enc(en);assert len(b)<=16,(jp,en);after=b.ljust(16,b'\0');end=o+20;op=r.find(b'\x22\x00',end,end+180)
 res.append(dict(offset=f'0x{o:06X}',japanese=jp,english=en,actor_id=f'0x{id:04X}',actor_key1=f'0x{u(o-6):04X}',actor_key2=f'0x{u(o-4):04X}',opcode_offset=f'0x{o-8:06X}',copy_consumer='0x391FA6'if 0x9f<=id<0xb0 else '0x3973C8',buffer='actor+0x62 (16 bytes)',render_consumer='0x39E929 -> 0x3AB7DE',sourceENreference=primary,canonical_japanese=sourcejp,expected_before_hex16=raw.hex(),after_hex16=after.hex(),tail_metadata_hex4=r[o+16:o+20].hex(),glyphs=len(b)//2,max_width_pixels=len(b)//2*8,classification=status,linguistic_mapping=review,runtime_copy='NOT_YET_RUN',runtime_render='REPRESENTATIVE_ONLY',natural_reachability='NOT_VALIDATED',visual_approval='NOT_VALIDATED',next_op22=f'0x{op:06X}'if op>=0 else '',next_op22_distance_after_struct=op-end if op>=0 else '',note=note))
save('translation_mapping_181.csv',res);save('exceptions_17.csv',[x for x in res if int(x['actor_id'],16)<0x1e0]);extra=[dict(offset='0x1B7D32',japanese='ティラワカ',english='Tiraw',expected_before_hex=r[0x1b7d32:0x1b7d3c].hex(),after_hex=enc('Tiraw').hex(),following_control_hex=r[0x1b7d3c:0x1b7d40].hex(),evidence='Real OP0022 operand terminated by next opcode001C, not strict21000000 grammar; handler3564 stops CP932 copy when word<8140; distinct from181')];save('extra_op22.csv',extra)
(a.out/'static_summary.json').write_text(json.dumps(dict(rom_sha256=sha,count=181,id_table_linked=sum(0x1e0<=int(x['actor_id'],16)<0x280 for x in res),exceptions=17,consumer_proven=181,guarded_code_ranges={hex(k):v for k,v in checks.items()},new_editorial=[x['offset']for x in res if x['linguistic_mapping']!='PASS'],extra_op22=extra),ensure_ascii=False,indent=2))
print('181 mappings; 164 linked by actor ID to table386B60; 17 exceptions; 3 editorial reviews; extra OP22 found.')
