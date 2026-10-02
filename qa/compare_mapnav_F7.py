#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageChops
import argparse
ap=argparse.ArgumentParser(); ap.add_argument('baseline_dir'); ap.add_argument('diagnostic_dir'); a=ap.parse_args()
b=Path(a.baseline_dir); d=Path(a.diagnostic_dir)
count=0
for bf in sorted(b.glob('f*.png')):
    df=d/bf.name
    ib=Image.open(bf).convert('RGB').crop((0,0,224,144))
    id=Image.open(df).convert('RGB').crop((0,0,224,144))
    box=ImageChops.difference(ib,id).getbbox()
    print(f'{bf.name}: pixel_diff_bbox={box}')
    if box is not None: raise SystemExit(2)
    count+=1
print(f'PASS: {count}/{count} normalized WonderSwan frames pixel-identical')
