from PIL import Image, ImageDraw
import os
for kind in ("illust","photo"):
    d=fr"images\{kind}_v10_clean"
    ims=[]
    for i in range(1,7):
        im=Image.open(os.path.join(d,f"gen{i:02d}.png")).convert("RGB"); im.thumbnail((500,500)); ims.append((i,im))
    cw=max(i.width for _,i in ims); ch=max(i.height for _,i in ims)
    sheet=Image.new("RGB",(cw*3,ch*2),(40,40,40)); dr=ImageDraw.Draw(sheet)
    # 10% grid for coord estimation
    for k,(i,im) in enumerate(ims):
        x=(k%3)*cw;y=(k//3)*ch;sheet.paste(im,(x,y))
        for gx in range(1,10): dr.line([(x+im.width*gx//10,y),(x+im.width*gx//10,y+im.height)],fill=(255,80,80),width=1)
        for gy in range(1,10): dr.line([(x,y+im.height*gy//10),(x+im.width,y+im.height*gy//10)],fill=(255,80,80),width=1)
        dr.text((x+4,y+4),str(i),fill=(0,255,0))
    sheet.save(fr"render\_v10grid_{kind}.png")
print("ok")
