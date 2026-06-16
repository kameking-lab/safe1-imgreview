from PIL import Image
import os
d=r"images\fallback"
fs=[f"gen0{i}.png" for i in range(1,7)]
ims=[Image.open(os.path.join(d,f)) for f in fs]
tw=3; th=2; cw,ch=ims[0].size
sheet=Image.new("RGB",(cw*tw, ch*th),"white")
for i,im in enumerate(ims):
    sheet.paste(im,((i%tw)*cw,(i//tw)*ch))
sheet=sheet.resize((cw*tw//2, ch*th//2))
sheet.save(r"render\_fallback_sheet.png")
print("ok",sheet.size)
