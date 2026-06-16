# -*- coding: utf-8 -*-
"""images/v13photo/case{N}/0{i}.png の右下スパークル除去→ v13photo_clean(非破壊)。"""
import os, glob, numpy as np
from PIL import Image, ImageFilter
BASE=r"C:\Users\kanet\20260522\safe1"
SRC=os.path.join(BASE,"images","v13photo"); DST=os.path.join(BASE,"images","v13photo_clean")
def clean(path,outpath):
    im=Image.open(path).convert("RGB"); W,H=im.size; arr=np.asarray(im).astype(np.int16)
    # 右下スパークル除去
    bw,bh,shift=min(170,W//4),min(150,H//4),min(110,W//6); x0,y0=W-bw,H-bh
    region=arr[y0:H,x0:W].copy(); src=arr[y0:H,x0-shift:W-shift].copy()
    diff=region.mean(axis=2)-src.mean(axis=2); mask=(diff>16)&(region.mean(axis=2)>120)
    if mask.sum()>0:
        m=Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2.0))
        ma=(np.asarray(m).astype(np.float32)/255.0)[...,None]
        arr[y0:H,x0:W]=(region*(1-ma)+src*ma).astype(np.uint8)
    # 右上のGemini操作アイコン(共有/コピー/DL)を左隣からクローンで隠す
    tw,th=min(150,W//4),min(70,H//6); tx0=W-tw; ts=min(160,W//5)
    treg=arr[0:th,tx0:W].copy(); tsrc=arr[0:th,tx0-ts:W-ts].copy()
    arr[0:th,tx0:W]=tsrc
    Image.fromarray(arr.astype(np.uint8)).save(outpath)
n=0
for p in glob.glob(os.path.join(SRC,"case*","0*.png")):
    rel=os.path.relpath(p,SRC); outp=os.path.join(DST,rel); os.makedirs(os.path.dirname(outp),exist_ok=True)
    try: clean(p,outp); n+=1
    except Exception as e: print("ERR",rel,e)
print(f"desparkled {n} -> {DST}")
