from pathlib import Path
import sys,struct,hashlib,json
from collections import Counter
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from magic_header_codec import decode,encode
FONT={
'A':['.###.','#...#','#...#','#####','#...#','#...#','#...#'],
'C':['.####','#....','#....','#....','#....','#....','.####'],
'D':['####.','#...#','#...#','#...#','#...#','#...#','####.'],
'E':['#####','#....','#....','####.','#....','#....','#####'],
'G':['.####','#....','#....','#.###','#...#','#...#','.###.'],
'I':['###','.#.','.#.','.#.','.#.','.#.','###'],
'K':['#...#','#..#.','#.#..','##...','#.#..','#..#.','#...#'],
'M':['#...#','##.##','#.#.#','#.#.#','#...#','#...#','#...#'],
'N':['#...#','##..#','##..#','#.#.#','#..##','#..##','#...#'],
'O':['.###.','#...#','#...#','#...#','#...#','#...#','.###.'],
'P':['####.','#...#','#...#','####.','#....','#....','#....'],
'S':['.####','#....','#....','.###.','....#','....#','####.'],
'T':['#####','..#..','..#..','..#..','..#..','..#..','..#..'],
'a':['....','....','.###','...#','####','#..#','.###'],
'b':['#...','#...','###.','#..#','#..#','#..#','###.'],
'c':['....','....','.###','#...','#...','#...','.###'],
'd':['...#','...#','.###','#..#','#..#','#..#','.###'],
'e':['....','....','.##.','#..#','####','#...','.###'],
'g':['....','.###','#..#','#..#','.###','...#','###.'],
'h':['#...','#...','###.','#..#','#..#','#..#','#..#'],
'i':['.#.','...','##.','.#.','.#.','.#.','###'],
'k':['#...','#...','#..#','#.#.','##..','#.#.','#..#'],
'l':['##.','.#.','.#.','.#.','.#.','.#.','###'],
'm':['.....','.....','##.#.','#.#.#','#.#.#','#.#.#','#.#.#'],
'n':['....','....','###.','#..#','#..#','#..#','#..#'],
'o':['....','....','.##.','#..#','#..#','#..#','.##.'],
'p':['....','###.','#..#','#..#','###.','#...','#...'],
'r':['...','...','##.','#.#','#..','#..','#..'],
's':['....','.###','#...','.##.','...#','...#','###.'],
't':['.#.','.#.','###','.#.','.#.','.#.','.##'],
'u':['....','....','#..#','#..#','#..#','#..#','.###'],
'v':['.....','.....','#...#','#...#','#...#','.#.#.','..#..'],
'w':['.....','.....','#...#','#...#','#.#.#','##.##','#...#'],
'y':['....','#..#','#..#','#..#','.###','...#','###.'],
'/':['...#','...#','..#.','..#.','.#..','.#..','#...'],
' ':['...']*7,
}
LABELS=[('Magic',24,12),('Arms/Charms',24,28),('Armor/Charms',24,44),('Trance',24,60),('Events',24,76),('Skills',24,92),('Secret Skills',24,108),('Animal Powers',128,12),('Gear Items',128,28),('Key Items',128,44),('Amulets',128,60),('Status',128,76),('Dungeons',128,92),('Options',128,108)]
source=Path(sys.argv[1]).read_bytes();out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
assert hashlib.sha256(source).hexdigest()=='d22bb029570e1b053e7cc11bd0cd1632ff310343d3c44ffaa072f771ae820ca0','F34 base identity'
q=0x309036;end=0x309856
assert source[q:q+3]==bytes([0,0,3]);offsets=[int.from_bytes(source[q+3+i*3:q+6+i*3],'big')for i in range(3)]
assert offsets==[12,1215,1701]
frames=[decode(source[q+z:])[0]for z in offsets]
assert tuple(map(len,frames))==(5216,1024,64)
gfx,mp=frames[:2];original_gfx=gfx;original_mp=mp
words=list(struct.unpack('<512H',mp));assert max(w&511 for w in words)<=240
# The text screen is 32x16 BG tiles; native graphics IDs begin at 78.
affected={(x,y)for y in range(1,15)for x in list(range(3,13))+list(range(16,28))}
assert all((words[y*32+x]&0xC000)==0 for x,y in affected)
# Menu-specific redraw on the native 8x8 grid; this is a documented typography redesign.
# These complete 5x7 strokes replace defective early English graphic lettering,
# leaving original palette, background, menus and native-layout cells unchanged.
pixels={}
for s,x,y in LABELS:
 start=x
 for ch in s:
  rows=FONT[ch];width=len(rows[0]);assert all(len(r)==width for r in rows),(ch,rows)
  for yy,row in enumerate(rows):
   for xx,c in enumerate(row):
    if c=='#':pixels[x+xx,y+yy]=8
  x+=width+2
 assert x-2<=224 and (x-2<=104 if start==24 else True),(s,x)
# Preserve all cells outside the exact text rows. Modified cells receive deduplicated tiles.
reserved={words[i]&511 for i in range(len(words))if (i%32,i//32)not in affected}
assert min(reserved)>=0
pool=[i for i in range(78,241)if i not in reserved]
assert len(pool)>100,len(pool)
result=bytearray(gfx);catalog={bytes(gfx[(i-78)*32:(i-77)*32]):i for i in reserved if 78<=i<241}
allocated={}
for y in range(1,15):
 for x in list(range(3,13))+list(range(16,28)):
  tile=bytearray(32)
  for yy in range(8):
   for xx in range(8):
    v=pixels.get((x*8+xx,y*8+yy),0)
    z=yy*4+xx//2;tile[z]|=v<<(4 if xx%2==0 else 0)
  key=bytes(tile)
  if key not in catalog:
   assert pool,'gfx tile budget exhausted'
   idx=pool.pop(0);catalog[key]=idx;allocated[idx]=key
   result[(idx-78)*32:(idx-77)*32]=key
  orig=words[y*32+x];words[y*32+x]=(orig&~511)|catalog[key]
newmap=struct.pack('<512H',*words)
# The tilemap must only change within the label cells; native palette and graphics outside remain.
assert all(words[i]==struct.unpack_from('<H',mp,i*2)[0]for i in range(512)if(i%32,i//32)not in affected)
assert all(result[(i-78)*32:(i-77)*32]==gfx[(i-78)*32:(i-77)*32]for i in reserved if 78<=i<241)
# Fixed individual compressed slots; no pointer relocation or resource growth.
# Graphics stay in their original compressed slot; the revised tile map uses
# a verified FF tail in this same bank, as the F31 e-Pet palette relocation does.
rom=bytearray(source)
coded_gfx=encode(bytes(result));coded_map=encode(newmap)
assert len(coded_gfx)<=offsets[1]-offsets[0]
relocation=0x30fc0f
assert source[relocation:relocation+len(coded_map)]==bytes([0xff])*len(coded_map)
assert relocation+len(coded_map)<=0x310000
rom[q+offsets[0]:q+offsets[0]+len(coded_gfx)]=coded_gfx
rom[relocation:relocation+len(coded_map)]=coded_map
rom[q+6:q+9]=(relocation-q).to_bytes(3,'big')
print('encoded',len(coded_gfx),'/',offsets[1]-offsets[0],len(coded_map),'relocated',hex(relocation))
assert decode(rom[q+offsets[0]:])[0]==bytes(result)
assert decode(rom[relocation:])[0]==newmap
assert decode(rom[q+offsets[2]:])[0]==frames[2]
rom[-2:]=struct.pack('<H',sum(rom[:-2])&0xffff)
assert len(rom)==len(source)
assert hashlib.sha256(rom).hexdigest()=='6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084','F35 target identity'
(out/'F35_menu_integrated.wsc').write_bytes(rom)
image=Image.new('RGB',(224,128),'#0b1d21')
for y in range(128):
 for x in range(224):
  z=words[(y//8)*32+x//8];tile=(z&511)-78
  if not 0<=tile<len(result)//32:continue
  xx=7-x%8 if z&0x4000 else x%8;yy=7-y%8 if z&0x8000 else y%8
  a=result[tile*32+yy*4+xx//2];v=a>>4 if xx%2==0 else a&15
  if v:image.putpixel((x,y),(220,220,220))
image.resize((1344,768),Image.Resampling.NEAREST).save(out/'F35_menu_resource_preview.png')
print('allocated',len(allocated),'available',len(pool),'changed gfx bytes',sum(a!=b for a,b in zip(result,gfx)),'changed map words',sum(a!=b for a,b in zip(words,struct.unpack('<512H',mp))),'SHA',hashlib.sha256(rom).hexdigest(),'checksum',rom[-2:].hex())
