from PIL import Image, ImageDraw
import os
d=r"images\photo_v7"
ims=[]
for i in (2,6):
    p=os.path.join(d,f"gen{i:02d}.png")
    if os.path.exists(p):
        im=Image.open(p).convert("RGB"); im.thumbnail((560,560)); ims.append((i,im))
if ims:
    cw=max(i.width for _,i in ims); ch=max(i.height for _,i in ims)
    sheet=Image.new("RGB",(cw*len(ims), ch),(200,200,200)); dr=ImageDraw.Draw(sheet)
    for k,(i,im) in enumerate(ims):
        sheet.paste(im,(k*cw,0)); dr.text((k*cw+6,6),str(i),fill=(255,0,0))
    sheet.save(r"render\_v7ph_26.png"); print("ok",[i for i,_ in ims])
