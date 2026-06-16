from PIL import Image, ImageDraw
import os
for kind in ("illust_v5","photo_v5"):
    d=fr"render\{kind}"
    fs=sorted([f for f in os.listdir(d) if f.endswith(".png")])
    ims=[Image.open(os.path.join(d,f)).convert("RGB") for f in fs]
    for im in ims: im.thumbnail((440,248))
    cw,ch=448,256; tw=4; th=(len(ims)+tw-1)//tw
    sheet=Image.new("RGB",(cw*tw, ch*th),(190,190,190)); dr=ImageDraw.Draw(sheet)
    for i,im in enumerate(ims):
        x=(i%tw)*cw+4; y=(i//tw)*ch+4; sheet.paste(im,(x,y)); dr.text((x+6,y+6),str(i+1),fill=(255,0,0))
    sheet.save(fr"render\_sheet_{kind}.png")
print("ok")
