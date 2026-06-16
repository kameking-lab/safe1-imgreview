from PIL import Image
import numpy as np
src=r"C:\Users\kanet\20260522\instagram-automation\screenshots\one-a1.png"
im=Image.open(src).convert("RGB")
print("ss",im.size)
W,H=im.size
card=im.crop((int(W*0.29), int(H*0.27), int(W*0.64), int(H*0.66)))
a=np.asarray(card.convert("L"))
# 画像は白カード上にあるので、非白(写真)領域をトリム
mask=(a<242)
ys,xs=np.where(mask)
if len(xs)>500:
    x0,x1,y0,y1=max(xs.min()-4,0),min(xs.max()+4,card.width),max(ys.min()-4,0),min(ys.max()+4,card.height)
    card=card.crop((x0,y0,x1,y1))
card.save(r"render\_a1crop.png")
print("crop",card.size, round(card.size[0]/card.size[1],3))
