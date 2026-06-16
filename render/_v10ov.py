from PIL import Image, ImageDraw
import os
overs=[4,6,8,10,12,14]  # 概要スライド番号
for kind in ("illust","photo"):
    crops=[]
    for n in overs:
        im=Image.open(fr"render\{kind}_v10\slide{n:02d}.png"); W,H=im.size
        c=im.crop((int(W*0.02),int(H*0.16),int(W*0.62),int(H*0.92))); c.thumbnail((400,400)); crops.append(c)
    cw=max(c.width for c in crops); ch=max(c.height for c in crops)
    sheet=Image.new("RGB",(cw*3,ch*2),(230,230,230))
    for k,c in enumerate(crops): sheet.paste(c,((k%3)*cw,(k//3)*ch))
    sheet.save(fr"render\_v10ov_{kind}.png")
print("ok")
