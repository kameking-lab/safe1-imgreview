from PIL import Image, ImageDraw
import os
d=r"images\cand_v12\case1\illust"
ims=[]
for i in range(1,6):
    p=os.path.join(d,f"{i:02d}.png")
    if os.path.exists(p):
        im=Image.open(p).convert("RGB"); im.thumbnail((360,360)); ims.append((i,im))
if ims:
    cw=max(i.width for _,i in ims); ch=max(i.height for _,i in ims)
    sheet=Image.new("RGB",(cw*5,ch),(210,210,210)); dr=ImageDraw.Draw(sheet)
    for k,(i,im) in enumerate(ims): sheet.paste(im,(k*cw,0)); dr.text((k*cw+4,4),str(i),fill=(255,0,0))
    sheet.save(r"render\_v12c1il.png"); print("ok",[i for i,_ in ims])
