# -*- coding: utf-8 -*-
"""Geminiスクショから画像本体のみ切り出し(プロンプト枠/アイコン除外・濃い輪郭で트rim)。"""
import os, numpy as np
from PIL import Image
SS = r"C:\Users\kanet\20260522\instagram-automation\screenshots"
OUT = r"C:\Users\kanet\20260522\safe1\images\proto\parts"; os.makedirs(OUT, exist_ok=True)
def crop(ssname, outname, region=(480,245,1215,725)):
    p=os.path.join(SS,ssname)
    if not os.path.exists(p): print("missing",ssname); return False
    im=Image.open(p).convert("RGB"); c=im.crop(region)
    a=np.asarray(c).astype(int)
    content=(a.min(axis=2)<205)  # 濃い輪郭/色のみ(白・薄灰の枠を除外)
    ys,xs=np.where(content)
    if len(xs)<300: print("no content",ssname); return False
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    pad=16
    c2=c.crop((max(x0-pad,0),max(y0-pad,0),min(x1+pad,c.width),min(y1+pad,c.height)))
    c2.save(os.path.join(OUT,outname)); print(f"{outname}: {c2.size}")
    return True
crop("parts-A-1.png","A.png")
crop("parts-C2-1.png","C.png")
print("done")
