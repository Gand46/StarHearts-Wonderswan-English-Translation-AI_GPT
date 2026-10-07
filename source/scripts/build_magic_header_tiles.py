#!/usr/bin/env python3
"""Extract the native rendered Magic glyph pixels; make 4bpp top-header tiles.
This only prepares a diagnostic tile overlay; ROM integration is separate.
"""
from pathlib import Path
from PIL import Image
import argparse,hashlib
p=argparse.ArgumentParser();p.add_argument('native_screenshot',type=Path);p.add_argument('out',type=Path);a=p.parse_args()
im=Image.open(a.native_screenshot).convert('RGB')
assert im.size==(237,144)
white=(240,240,240)
# Fullwidth native glyph cells are 12 pixels wide, x=8..67, at y=129..138.
assert sum(im.getpixel((x,y))==white for y in range(129,139) for x in range(8,68))>=75
# Nine header tiles per row cover x=8..79. Native glyphs occupy x=8..67;
# the original final Japanese tile at x=68..79 is cleared.
out=bytearray()
for tile_row in range(2):
 for tile_col in range(1,10):
  for yy in range(8):
   for pair in range(4):
    nib=[]
    for xoff in (0,1):
     x=tile_col*8+pair*2+xoff;y=tile_row*8+yy
     source_y=129+(y-2)
     nib.append(0xB if 8<=x<68 and 129<=source_y<=138 and im.getpixel((x,source_y))==white else 0)
    out.append((nib[0]<<4)|nib[1])
assert len(out)==576
a.out.write_bytes(out)
print(len(out),hashlib.sha256(out).hexdigest())
