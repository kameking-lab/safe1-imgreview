from PIL import Image
import os
d=r"render\v1"
fs=sorted([f for f in os.listdir(d) if f.endswith(".png")])
ims=[Image.open(os.path.join(d,f)).convert("RGB") for f in fs]
for im in ims: im.thumbnail((440,248))
cw,ch=448,256; tw=4; th=(len(ims)+tw-1)//tw
sheet=Image.new("RGB",(cw*tw, ch*th),(200,200,200))
from PIL import ImageDraw
dr=ImageDraw.Draw(sheet)
for i,im in enumerate(ims):
    x=(i%tw)*cw+4; y=(i//tw)*ch+4
    sheet.paste(im,(x,y))
    dr.text((x+6,y+6),str(i+1),fill=(255,0,0))
sheet.save(r"render\_v1_sheet.png")
print("ok",sheet.size,"slides",len(ims))
