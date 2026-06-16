from PIL import Image, ImageDraw
import os
d=r"images\v13photo\case1"; ims=[]
for i in (1,2,3):
    p=os.path.join(d,f"0{i}.png")
    if os.path.exists(p): im=Image.open(p).convert("RGB"); im.thumbnail((420,420)); ims.append((i,im))
cw=max(i.width for _,i in ims); ch=max(i.height for _,i in ims)
sheet=Image.new("RGB",(cw*3,ch),(225,225,225)); dr=ImageDraw.Draw(sheet)
for k,(i,im) in enumerate(ims): sheet.paste(im,(k*cw,0)); dr.text((k*cw+5,5),str(i),fill=(255,0,0))
sheet.save(r"render\_v13c1.png"); print("ok")
