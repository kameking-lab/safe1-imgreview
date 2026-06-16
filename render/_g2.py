from PIL import Image
import os
d=r"images\gen"
ims=[]
for f in ["gen02a.png","gen02b.png"]:
    p=os.path.join(d,f)
    if os.path.exists(p):
        im=Image.open(p).convert("RGB"); im.thumbnail((640,640)); ims.append((f,im))
    else: print("MISSING",f)
if ims:
    cw=max(i.width for _,i in ims); ch=max(i.height for _,i in ims)
    sheet=Image.new("RGB",(cw*len(ims), ch),"white")
    for k,(f,im) in enumerate(ims): sheet.paste(im,(k*cw,0))
    sheet.save(r"render\_gen02ab.png"); print("ok",[(f,i.size) for f,i in ims])
