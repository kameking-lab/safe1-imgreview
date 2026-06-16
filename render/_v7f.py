from PIL import Image, ImageDraw
import os
for kind in ("illust","photo"):
    d=fr"images\{kind}_v7"
    ims=[]
    for i in range(1,7):
        im=Image.open(os.path.join(d,f"gen{i:02d}.png")).convert("RGB"); im.thumbnail((480,480)); ims.append((i,im))
    cw=max(i.width for _,i in ims); ch=max(i.height for _,i in ims)
    sheet=Image.new("RGB",(cw*3, ch*2),(200,200,200)); dr=ImageDraw.Draw(sheet)
    for k,(i,im) in enumerate(ims):
        x=(k%3)*cw;y=(k//3)*ch;sheet.paste(im,(x,y));dr.text((x+6,y+6),str(i),fill=(255,0,0))
    sheet.save(fr"render\_v7full_{kind}.png")
print("ok")
