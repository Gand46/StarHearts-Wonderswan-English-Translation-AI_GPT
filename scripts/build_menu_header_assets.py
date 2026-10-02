"""Build ten Bank-30 headers from exact native menu glyph masks."""
from pathlib import Path
import sys,json,hashlib
from PIL import Image
from magic_header_codec import decode
from collections import defaultdict,deque
def encode(data):
    # Index each literal immediately, then flush pending literals in groups.
    # This allows short-distance runs to enter the match dictionary promptly.
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
            flush()
            bit(1);bit(1);length=best-2 if best<18 else 0
            out.extend(((length<<12)|(distance-1)).to_bytes(2,'little'))
            if best>=18:out.append(best-18)
            size=best;tokens+=1
        else:pending.append(data[i]);size=1
        for p in range(i,i+size):
            if p+3<=len(data):table[data[p:p+3]].append(p)
        i+=size
    flush()
    out[1:3]=tokens.to_bytes(2,'big');assert decode(out)[0]==data
    return bytes(out)
rom=Path(sys.argv[1]).read_bytes();out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
ref=Image.open(sys.argv[3]).convert('RGB');assert ref.size==(237,144)
assert hashlib.sha256(rom).hexdigest()=='17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa'
start=0x309A56;end=0x309FC6;count=int.from_bytes(rom[start+1:start+3],'big');assert count==11
frames=[]
for i in range(count):
    p=start+int.from_bytes(rom[start+3+i*3:start+6+i*3],'big');frames.append(decode(rom[p:])[0])
original=frames[:];changes=[]
def pixels(g,m,x,y):
    cell=y//8*32+x//8;w=int.from_bytes(m[cell*2:cell*2+2],'little');px=7-x%8 if w&0x4000 else x%8;py=7-y%8 if w&0x8000 else y%8
    pos=(w&511)*32+py*4+px//2;v=g[pos];return (v>>4) if px%2==0 else (v&15)
# Prove that the accepted in-game reference uses the exact already-English header font.
assert all((pixels(frames[0],frames[1],8+x,4+y)==11)==(ref.getpixel((24+x,28+y))==(128,128,128)) for y in range(8) for x in range(60))
for n,label,box in [(2,'Armor/Charms',(24,44,90,52)),(4,'Arms',(24,28,46,36)),(6,'Armor',(24,44,55,52))]:
    gfx=bytearray(frames[n]);mp=bytearray(frames[n+1]);cells={y*32+x for y in range(2) for x in range(1,11)}
    words=[int.from_bytes(mp[p:p+2],'little')for p in range(0,len(mp),2)]
    outside={w&511 for i,w in enumerate(words)if i not in cells}
    pool=sorted({words[i]&511 for i in cells}-outside)
    # Reuse existing header-only tiles first; never modify tiles shared with the frame.
    tiles={bytes(gfx[:32]):0} if gfx[:32]==bytes(32) else {}
    used=[]
    for cell in sorted(cells):
        cx=cell%32;cy=cell//32;tile=bytearray(32)
        for yy in range(8):
            for xx in range(8):
                x=cx*8+xx;y=cy*8+yy;sx=box[0]+x-8;sy=box[1]+y-4
                v=11 if box[0]<=sx<box[2] and box[1]<=sy<box[3] and ref.getpixel((sx,sy))==(128,128,128) else 0
                p=yy*4+xx//2;tile[p]|=v<<(4 if xx%2==0 else 0)
        key=bytes(tile)
        if key not in tiles:
            if pool:idx=pool.pop(0)
            else:idx=len(gfx)//32;gfx.extend(bytes(32))
            assert idx<512;gfx[idx*32:idx*32+32]=key;tiles[key]=idx;used.append(idx)
        w=(words[cell]&~0xC1FF)|tiles[key];mp[cell*2:cell*2+2]=w.to_bytes(2,'little')
    frames[n]=bytes(gfx);frames[n+1]=bytes(mp)
    assert all(pixels(frames[n],frames[n+1],x,y)==pixels(original[n],original[n+1],x,y) for y in range(128)for x in range(224)if not (8<=x<88 and y<16))
    changes.append({'label':label,'frames':[n,n+1],'reference_box':box,'used_tiles':used,'original_gfx_bytes':len(original[n]),'new_gfx_bytes':len(gfx)})
header=bytearray((0,0,count));coded=[encode(b)for b in frames];pos=3+count*3
for block in coded:header+=pos.to_bytes(3,'big');pos+=len(block)
resource=bytes(header)+b''.join(coded)
print('Compressed frame sizes:',[len(x) for x in coded], 'decoded:', [len(x) for x in frames])
assert len(resource)<=end-start,(len(resource),end-start)
for i in range(count):
    p=int.from_bytes(resource[3+i*3:6+i*3],'big');assert decode(resource[p:])[0]==frames[i]
for i in (0,1,8,9,10):assert original[i]==frames[i]
(out/'repair_armor_headers.bin').write_bytes(resource)
(out/'asset_manifest.json').write_text(json.dumps({'resource_start':'309A56','resource_capacity':end-start,'resource_size':len(resource),'resource_sha256':hashlib.sha256(resource).hexdigest(),'source_resource_sha256':hashlib.sha256(rom[start:end]).hexdigest(),'native_reference_sha256':hashlib.sha256(Path(sys.argv[3]).read_bytes()).hexdigest(),'native_font_mask_equality':True,'changes':changes,'unchanged_frames':[0,1,8,9,10]},indent=2)+'\n')
for i,b in enumerate(frames):(out/f'frame_{i}.bin').write_bytes(b)
print('PASS',len(resource),'/',end-start,changes)
# Other observed Japanese headers in the same menu table. English terminology
# follows the already translated main menu and F29 SELL glossary.
catalog=[]
for i,label,box in [(3,'Animal Powers',(128,12,193,20)),(5,'Gear Items',(129,28,177,36)),(7,'Charms',(51,28,84,36)),(8,'Amulets',(128,60,164,68)),(11,'Skills',(24,92,47,100)),(12,'e-Pet',None),(13,'Secret Skills',(24,108,79,116))]:
    pointers=[0x30843e+8*int.from_bytes(rom[0x30841e+k*2:0x308420+k*2],'little')for k in range(16)]
    q=pointers[i];boundary=min(p for p in pointers if p>q);n=int.from_bytes(rom[q+1:q+3],'big')
    parts=[];original_blocks=[];original_offsets=[]
    for j in range(n):
        p=q+int.from_bytes(rom[q+3+j*3:q+6+j*3],'big');decoded,consumed=decode(rom[p:]);parts.append(decoded);original_blocks.append(rom[p:p+consumed]);original_offsets.append(p-q)
    graphics=bytearray(parts[0]);original_graphics=bytes(graphics)
    mask=set()
    if box:
        mask={(8+x-box[0],4+y-box[1])for y in range(box[1],box[3])for x in range(box[0],box[2])if ref.getpixel((x,y))==(128,128,128)}
    else:
        for dest,box2 in [(8,(152,60,156,68)),(22,(163,12,167,20)),(27,(152,60,156,68)),(32,(48,108,53,116))]:
            mask|={(dest+x-box2[0],4+y-box2[1])for y in range(box2[1],box2[3])for x in range(box2[0],box2[2])if ref.getpixel((x,y))==(128,128,128)}
        # Exact native dash pixels from the original e-Pet header (x25..32,y7).
        for x in range(25,33):
            off=(x//8)*32+7*4+x%8//2;v=original_graphics[off];v=v>>4 if x%2==0 else v&15
            assert v==11;mask.add((13+x-25,7))
    for y in range(16):
        for x in range(8,88):
            off=(y//8*28+x//8)*32+y%8*4+x%8//2;v=11 if (x,y)in mask else 0
            graphics[off]=(graphics[off]&15)|(v<<4)if x%2==0 else(graphics[off]&240)|v
    parts[0]=bytes(graphics);blocks=[encode(b)for b in parts];head=bytearray((0,0,n));pos=3+3*n
    for b in blocks:head+=pos.to_bytes(3,'big');pos+=len(b)
    extra=[]
    if i==12:
        # The e-Pet resource is packed tightly. Preserve its four palettes
        # byte-for-byte; move only palette 1 into the verified FF tail.
        relocation=0x30FB8E;palette=original_blocks[1]
        assert rom[relocation:relocation+len(palette)]==b'\xff'*len(palette)
        offsets=[18,relocation-q,*original_offsets[2:]]
        head=bytes((0,0,n))+b''.join(p.to_bytes(3,'big')for p in offsets)
        packed=head+blocks[0];assert len(packed)<=original_offsets[2]
        extra_name='epet_palette1.bin';(out/extra_name).write_bytes(palette)
        extra=[{'asset':extra_name,'offset':relocation,'size':len(palette),'sha256':hashlib.sha256(palette).hexdigest(),'precondition':'FF_FILL'}]
        trial=bytearray(rom);trial[q:q+len(packed)]=packed;trial[relocation:relocation+len(palette)]=palette
        for j,b in enumerate(parts):assert decode(trial[q+offsets[j]:])[0]==b
    else:
        packed=bytes(head)+b''.join(blocks);assert len(packed)<=boundary-q,(i,len(packed),boundary-q)
        for j,b in enumerate(parts):assert decode(packed[int.from_bytes(packed[3+j*3:6+j*3],'big'):])[0]==b
    name=f'header_{i:02d}.bin';(out/name).write_bytes(packed)
    catalog.append({'resource_index':i,'label':label,'offset':q,'capacity':boundary-q,'size':len(packed),'asset':name,'sha256':hashlib.sha256(packed).hexdigest(),'preimage_sha256':hashlib.sha256(rom[q:q+len(packed)]).hexdigest(),'only_decoded_header_rectangle_changed':True,'external_chunks':extra})
(out/'additional_headers.json').write_text(json.dumps(catalog,indent=2)+'\n')
print('Additional headers:',[(x['label'],x['size'],x['capacity'])for x in catalog])
