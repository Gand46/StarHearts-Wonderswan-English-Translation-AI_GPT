#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,struct,hashlib

def sha(b): return hashlib.sha256(b).hexdigest()
def has_kana_kanji(s):
    return any(('\u3040' <= c <= '\u30ff') or ('\u3400' <= c <= '\u9fff') for c in s)
def has_latin(s):
    return any(('A'<=c<='Z') or ('a'<=c<='z') or ('Ａ'<=c<='Ｚ') or ('ａ'<=c<='ｚ') for c in s)
def decode_tail(raw):
    try:return raw.decode('cp932')
    except UnicodeDecodeError:return ''
def map_label(data,abs_start):
    tail=data[abs_start+3:abs_start+67]
    ends=[]
    for pat in (b'\x00\x00',b'\xff\xff'):
        j=tail.find(pat)
        if j>=0: ends.append(j)
    e=min(ends) if ends else min(40,len(tail))
    raw=tail[:e]
    return raw,decode_tail(raw)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('rom'); ap.add_argument('--original',required=True); ap.add_argument('--outdir',required=True); a=ap.parse_args()
    cur=Path(a.rom).read_bytes(); orig=Path(a.original).read_bytes(); out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)
    rows=[]
    # BANK38 primary active text table: 257 strictly increasing u16 pointers.
    off=0x384B32; n=257; base=0x380000
    ptrs=[struct.unpack_from('<H',cur,off+2*i)[0] for i in range(n)]
    assert all(x<y for x,y in zip(ptrs,ptrs[1:])), 'BANK38 primary table not strictly increasing'
    active_jp=0; same=0; placeholders=0
    for i,p in enumerate(ptrs):
        nxt=ptrs[i+1] if i+1<n else min(0x10000,p+96)
        b=cur[base+p:base+nxt]
        ob=orig[base+p:base+nxt]
        if b==ob: same+=1
        # this table uses 1A1A text terminators in the current branch; only kana/kanji counts as JP.
        sample=b[:min(80,len(b))]
        try:s=sample.decode('cp932','ignore')
        except:s=''
        if has_kana_kanji(s): active_jp+=1
        if b.startswith(b'\x81\x48\x81\x48\x81\x48\x81\x48'): placeholders+=1
    rows.append({'table':'BANK38_PRIMARY_TEXT_U16','offset':'0x384B32','entries':n,'pointer_range':f'0x{ptrs[0]:04X}-0x{ptrs[-1]:04X}','consumer_status':'typed active text/resource table','active_jp':active_jp,'active_en_or_mte':n-placeholders-active_jp,'placeholder':placeholders,'unproven_jp_suffix':0,'binary_or_no_label':0,'notes':f'strictly increasing; {same} target slot(s) byte-identical to JP original'})

    # BANK38 world-map structural table. Table length is proved by consumer loop CX=0x0360.
    toff=0x38B712; mn=0x360
    mptrs=[struct.unpack_from('<H',cur,toff+2*i)[0] for i in range(mn)]
    assert len(set(mptrs))==mn
    assert toff+2*mn == base+min(mptrs), 'table must end exactly at first record'
    cats={'JP_SUFFIX':0,'LATIN_SUFFIX':0,'NO_LABEL':0,'OTHER_SUFFIX':0}; same_records=0
    sortedp=sorted(mptrs)
    details=[]
    for i,p in enumerate(sortedp):
        abs_s=base+p; raw,text=map_label(cur,abs_s)
        if not raw: cat='NO_LABEL'
        elif has_kana_kanji(text): cat='JP_SUFFIX'
        elif has_latin(text): cat='LATIN_SUFFIX'
        else: cat='OTHER_SUFFIX'
        cats[cat]+=1
        nxt=sortedp[i+1] if i+1<len(sortedp) else min(0x10000,p+64)
        unchanged=cur[base+p:base+nxt]==orig[base+p:base+nxt]
        same_records += int(unchanged)
        details.append({'index':i,'pointer':f'0x{p:04X}','x':cur[abs_s],'y':cur[abs_s+1],'type':cur[abs_s+2],'suffix_class':cat,'suffix_text':text,'record_unchanged_vs_original':unchanged})
    rows.append({'table':'BANK38_WORLD_MAP_RECORD_U16','offset':'0x38B712','entries':mn,'pointer_range':f'0x{min(mptrs):04X}-0x{max(mptrs):04X}','consumer_status':'active structural record table; identified x/y/type consumer reads bytes +0..+2 only','active_jp':0,'active_en_or_mte':cats['LATIN_SUFFIX'],'placeholder':0,'unproven_jp_suffix':cats['JP_SUFFIX'],'binary_or_no_label':cats['NO_LABEL']+cats['OTHER_SUFFIX'],'notes':f'864 unique pointers; table ends at first record 0x{min(mptrs):04X}; {same_records}/864 records unchanged vs original; JP suffixes not patched without textual consumer proof'})

    with (out/'ACTIVE_POINTER_CENSUS_F6.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
    with (out/'BANK38_WORLD_MAP_RECORDS_F6.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(details[0].keys()));w.writeheader();w.writerows(details)
    report={'phase':'13BG-F6','rom_sha256':sha(cur),'original_sha256':sha(orig),'binary_change':False,'tables':rows,'classification_rule':'Only kana/kanji with a demonstrated text consumer is ACTIVE_JP. Japanese bytes in retained source strings or unproven record suffixes are not patched by inference.'}
    (out/'ACTIVE_POINTER_CENSUS_F6.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
