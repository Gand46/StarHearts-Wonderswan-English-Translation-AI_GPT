"""Translate e-Pet's graphic labels using exact native runtime Latin glyphs."""
from pathlib import Path
from collections import Counter,defaultdict,deque
import sys,json,hashlib
from PIL import Image
from magic_header_codec import decode

def encode(data):
    out=bytearray(b'\0\0\0');table=defaultdict(lambda:deque(maxlen=128));flagbit=8;flagpos=0;tokens=0
    def bit(v):
        nonlocal flagbit,flagpos
        if flagbit==8:flagpos=len(out);out.append(0);flagbit=0
        out[flagpos]|=v<<flagbit;flagbit+=1
    pending=bytearray()
    def flush():
        nonlocal tokens
        while pending:
            size=min(266,len(pending))
            if size>=11:bit(1);bit(0);out.append(size-11);out.extend(pending[:size]);tokens+=1
            else:
                for value in pending[:size]:bit(0);out.append(value);tokens+=1
            del pending[:size]
    i=0
    while i<len(data):
        best=0;distance=0
        for old in reversed(table.get(data[i:i+3],())):
            d=i-old
            if d>4096:break
            n=3
            while n<min(273,len(data)-i) and data[i+n]==data[i+n-d]:n+=1
            if n>best:best=n;distance=d
            if n==273:break
        if best>=3:
            flush();bit(1);bit(1);length=best-2 if best<18 else 0
            out.extend(((length<<12)|(distance-1)).to_bytes(2,'little'))
            if best>=18:out.append(best-18)
            size=best;tokens+=1
        else:pending.append(data[i]);size=1
        for p in range(i,i+size):
            if p+3<=len(data):table[data[p:p+3]].append(p)
        i+=size
    flush();out[1:3]=tokens.to_bytes(2,'big');assert decode(out)[0]==data
    return bytes(out)

def main():
    rom=Path(sys.argv[1]).read_bytes();atlas_path=Path(sys.argv[2]);out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(rom).hexdigest()=='fbf949271412eb023cb94765782126a689eead61e8c6a56b2a12b85ed23acd52'
    atlas=Image.open(atlas_path).convert('RGB');glyphs={}
    alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-/'
    for i,ch in enumerate(alphabet):
        index=i//7;col=i%7;x=(8 if index%2==0 else 120)+12*col;y=24+16*(index//2)
        points={(xx,yy)for yy in range(12)for xx in range(12)if atlas.getpixel((x+xx,y+yy))==(240,240,240)}
        left=min(p[0]for p in points);right=max(p[0]for p in points)
        glyphs[ch]={'width':right-left+1,'points':sorted((px-left,py)for px,py in points),'native_cell':[x,y,12,12],'x_trim':left}
    glyphs[' ']={'width':4,'points':[]}
    q=0x30AA96;n=int.from_bytes(rom[q+1:q+3],'big');assert n==5
    offsets=[int.from_bytes(rom[q+3+i*3:q+6+i*3],'big')for i in range(n)]
    original=decode(rom[q+offsets[0]:])[0];assert len(original)==16128
    graphics=bytearray(original);allowed=set();ledger=[]
    def pixel(b,x,y):
        p=(y//8*28+x//8)*32+y%8*4+x%8//2
        return b[p]>>4 if x%2==0 else b[p]&15
    def put(x,y,value):
        p=(y//8*28+x//8)*32+y%8*4+x%8//2
        graphics[p]=(graphics[p]&15)|(value<<4)if x%2==0 else(graphics[p]&240)|value
    def label(jp,en,x,y,w,color,clear_y=None,clear_h=14):
        cy=y if clear_y is None else clear_y
        width=sum(glyphs[ch]['width']for ch in en)+max(0,len(en)-1)
        assert width<=w,(en,width,w)
        for yy in range(cy,cy+clear_h):
            for xx in range(x,x+w):allowed.add((xx,yy));put(xx,yy,0)
        cursor=x
        for ch in en:
            g=glyphs[ch]
            for dx,dy in g['points']:
                assert (cursor+dx,y+dy)in allowed,(en,dy)
                put(cursor+dx,y+dy,color)
            cursor+=g['width']+1
        ledger.append({'japanese':jp,'english':en,'box':[x,cy,w,clear_h],'native_cell_y':y,'glyph_color':color,'ink_width':width})
    label('ライフ','Life',8,24,72,11,22)
    label('マジック','Magic',8,40,72,11,38)
    label('対戦数','Battles',128,24,68,9,22)
    label('勝星数','Wins',128,40,68,9,38)
    label('ステータス','Status',8,65,102,11,64)
    for row,(jp,en)in enumerate([('つよさ','Str'),('まもり','Def'),('かしこさ','Int'),('すばやさ','Agi')]):
        y=80+row*16;label(jp,en,8,y,48,11,clear_h=12);label('レベル','Lv',64,y,40,11,clear_h=12)
    for jp,en,x,y in [('火','Fire',120,64),('水','Wtr',168,64),('風','Wnd',120,80),('地','Erth',168,80),('光','Lgt',120,96),('闇','Dark',168,96),('氷','Ice',120,112),('雷','Thun',168,112),('神','Holy',120,128)]:
        label(jp,en,x,y,28,10,clear_h=12)
    for y in range(144):
        for x in range(224):
            if (x,y)not in allowed:assert pixel(original,x,y)==pixel(graphics,x,y)
    packed=rom[q:q+18]+encode(bytes(graphics))
    assert len(packed)<=offsets[2],(len(packed),offsets[2])
    assert decode(packed[18:])[0]==graphics
    (out/'epet_body_resource.bin').write_bytes(packed)
    (out/'native_latin_glyphs.json').write_text(json.dumps({'reference_sha256':hashlib.sha256(atlas_path.read_bytes()).hexdigest(),'method':'native CP932 renderer; temporary skill-name buffers; no resized/reconstructed glyphs','glyphs':glyphs},indent=2)+'\n')
    (out/'epet_labels.json').write_text(json.dumps({'labels':ledger,'label_occurrences':len(ledger),'unique_labels':len({r['english']for r in ledger}),'resource_offset':q,'asset_size':len(packed),'capacity_before_next_preserved_palette':offsets[2],'decoded_bytes':len(graphics),'unchanged_outside_label_boxes':True,'palette_frames_unchanged':[1,2,3,4],'header_unchanged':True},indent=2,ensure_ascii=False)+'\n')
    print('e-Pet',len(ledger),'labels;',len(packed),'/',offsets[2],'bytes; native glyphs, outside boxes unchanged')

if __name__=='__main__':main()
