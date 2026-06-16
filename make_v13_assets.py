# -*- coding: utf-8 -*-
"""v13photo_clean とrefsを GitHub公開用に整形。
imgreview/v13photo/case{N}/0{i}.png(最大幅1024)＋ case{N}_sheet.png(3枚一覧)＋ imgreview/refs/case{N}_ref.jpg"""
import os, glob, shutil
from PIL import Image, ImageDraw, ImageFont
BASE=r"C:\Users\kanet\20260522\safe1"
CLEAN=os.path.join(BASE,"images","v13photo_clean")
DST=os.path.join(BASE,"imgreview","v13photo"); REFD=os.path.join(BASE,"imgreview","refs")
REFSRC=os.path.join(BASE,"refs","anzen")
os.makedirs(REFD,exist_ok=True)
def font(sz):
    for p in (r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
F=font(26)
for c in range(1,7):
    od=os.path.join(DST,f"case{c}"); os.makedirs(od,exist_ok=True)
    tiles=[]
    for i in range(1,4):
        p=os.path.join(CLEAN,f"case{c}",f"0{i}.png")
        if not os.path.exists(p): continue
        im=Image.open(p).convert("RGB")
        if im.width>1024: im=im.resize((1024,round(im.height*1024/im.width)),Image.LANCZOS)
        im.save(os.path.join(od,f"0{i}.png"))
        t=im.resize((460,round(im.height*460/im.width)),Image.LANCZOS)
        bar=Image.new("RGB",(460,34),(20,20,20)); ImageDraw.Draw(bar).text((6,4),f"case{c} photo {i}",fill="white",font=F)
        cell=Image.new("RGB",(460,t.height+34),"white"); cell.paste(bar,(0,0)); cell.paste(t,(0,34)); tiles.append(cell)
    if tiles:
        cw=460; ch=max(t.height for t in tiles)
        sheet=Image.new("RGB",(cw*len(tiles)+8,ch+8),(190,190,190))
        for k,t in enumerate(tiles): sheet.paste(t,(k*cw+4,4))
        sheet.save(os.path.join(DST,f"case{c}_sheet.png"))
    # 参照見本(refs)
    rs=glob.glob(os.path.join(REFSRC,f"case{c}_*"))
    if rs: shutil.copy(rs[0], os.path.join(REFD,f"case{c}_ref{os.path.splitext(rs[0])[1]}"))
    print(f"case{c}: {len(tiles)} photos + sheet + ref")
print("DONE")
