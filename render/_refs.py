from PIL import Image, ImageDraw
import os, glob
d=r"refs\anzen"; ims=[]
for c in range(1,7):
    fs=glob.glob(os.path.join(d,f"case{c}_*"))
    if fs:
        im=Image.open(fs[0]).convert("RGB"); im.thumbnail((360,360)); ims.append((c,im))
cw=max(i.width for _,i in ims); ch=max(i.height for _,i in ims)
sheet=Image.new("RGB",(cw*3,ch*2),(230,230,230)); dr=ImageDraw.Draw(sheet)
for k,(c,im) in enumerate(ims):
    x=(k%3)*cw;y=(k//3)*ch; sheet.paste(im,(x,y)); dr.text((x+5,y+5),f"case{c}",fill=(255,0,0))
sheet.save(r"render\_refs_sheet.png"); print("ok",[c for c,_ in ims])
