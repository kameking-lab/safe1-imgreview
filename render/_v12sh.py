from PIL import Image, ImageDraw
import os
def sheet(c):
    rows=[]
    for kind in ("illust","photo"):
        ims=[]
        for i in range(1,6):
            p=fr"images\cand_v12\case{c}\{kind}\{i:02d}.png"
            if os.path.exists(p):
                im=Image.open(p).convert("RGB"); im.thumbnail((300,300)); ims.append(im)
        if ims:
            cw=max(i.width for i in ims); ch=max(i.height for i in ims)
            row=Image.new("RGB",(cw*5,ch),(225,225,225))
            for k,im in enumerate(ims): row.paste(im,(k*cw,0))
            rows.append((kind,row))
    if not rows: return
    W=max(r.width for _,r in rows); H=sum(r.height for _,r in rows)+40
    out=Image.new("RGB",(W,H),(255,255,255)); dr=ImageDraw.Draw(out); y=0
    for kind,row in rows:
        dr.rectangle([0,y,W,y+18],fill=(30,30,30)); dr.text((4,y+2),f"case{c} {kind}",fill="white"); y+=20
        out.paste(row,(0,y)); y+=row.height
    out.save(fr"render\_v12sheet_c{c}.png")
for c in (2,4,5,6): sheet(c)
print("ok")
