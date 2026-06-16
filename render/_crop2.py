from PIL import Image
import os
src=r"C:\Users\kanet\20260522\instagram-automation\screenshots\gen2-v1-a1.png"
im=Image.open(src).convert("RGB")
print("ss size", im.size)
# 生成画像カード領域を切り出し
card=im.crop((476, 306, 1214, 712))
# 余白トリム(白背景の周囲を少し削る)
import numpy as np
a=np.asarray(card.convert("L"))
mask=a<245
ys,xs=np.where(mask)
if len(xs):
    x0,x1,y0,y1=max(xs.min()-12,0),min(xs.max()+12,card.width),max(ys.min()-12,0),min(ys.max()+12,card.height)
    card=card.crop((x0,y0,x1,y1))
# 1.832比のキャンバスに白で配置(他のGemini画像と縦横比を合わせる)
ratio=1.832
cw,ch=card.size
tw,th=cw,int(cw/ratio)
if th<ch:
    th=ch; tw=int(ch*ratio)
canvas=Image.new("RGB",(tw,th),"white")
canvas.paste(card,((tw-cw)//2,(th-ch)//2))
canvas=canvas.resize((1024,559),Image.LANCZOS)
canvas.save(r"images\gen\gen02.png")
print("saved gen02 from screenshot crop", canvas.size, "card was", card.size)
