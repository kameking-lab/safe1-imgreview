from PIL import Image, ImageDraw
items=[("illust_v8","gen03","il3"),("photo_v8","gen03","ph3"),("photo_v8","gen02","ph2")]
ims=[]
import os
for d,f,lab in items:
    im=Image.open(fr"images\{d}\{f}.png").convert("RGB"); im.thumbnail((520,520)); ims.append((lab,im))
cw=max(i.width for _,i in ims); ch=max(i.height for _,i in ims)
sheet=Image.new("RGB",(cw*3,ch),(200,200,200)); dr=ImageDraw.Draw(sheet)
for k,(lab,im) in enumerate(ims): sheet.paste(im,(k*cw,0)); dr.text((k*cw+6,6),lab,fill=(255,0,0))
sheet.save(r"render\_v8chk.png"); print("ok")
