from PIL import Image
import os
d=r"images\gen"
fs=[f"gen0{i}.png" for i in range(1,7)]
ims=[]
for f in fs:
    im=Image.open(os.path.join(d,f)).convert("RGB")
    im.thumbnail((620,620))
    ims.append(im)
cw=max(i.width for i in ims); ch=max(i.height for i in ims)
tw,th=3,2
sheet=Image.new("RGB",(cw*tw, ch*th),"white")
for i,im in enumerate(ims):
    x=(i%tw)*cw+(cw-im.width)//2; y=(i//tw)*ch+(ch-im.height)//2
    sheet.paste(im,(x,y))
sheet.save(r"render\_gen_sheet.png")
print("ok", sheet.size, [i.size for i in ims])
