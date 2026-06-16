# -*- coding: utf-8 -*-
"""make_v12_assets.py : cand_v12_clean を GitHub公開用に整形。
imgreview/v12/case{N}/{kind}/NN.png（最大幅1024）＋ imgreview/v12/case{N}_sheet.png（10枚一覧）。"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
BASE=r"C:\Users\kanet\20260522\safe1"
CLEAN=os.path.join(BASE,"images","cand_v12_clean")
DST=os.path.join(BASE,"imgreview","v12")
def font(sz):
    for p in (r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
F=font(26)
for c in range(1,7):
    tiles=[]
    for kind in ("illust","photo"):
        od=os.path.join(DST,f"case{c}",kind); os.makedirs(od,exist_ok=True)
        for i in range(1,6):
            p=os.path.join(CLEAN,f"case{c}",kind,f"{i:02d}.png")
            if not os.path.exists(p): continue
            im=Image.open(p).convert("RGB")
            if im.width>1024: im=im.resize((1024,round(im.height*1024/im.width)),Image.LANCZOS)
            im.save(os.path.join(od,f"{i:02d}.png"))
            t=im.resize((420,round(im.height*420/im.width)),Image.LANCZOS)
            bar=Image.new("RGB",(420,34),(20,20,20)); ImageDraw.Draw(bar).text((6,4),f"{kind} {i}",fill="white",font=F)
            cell=Image.new("RGB",(420,t.height+34),"white"); cell.paste(bar,(0,0)); cell.paste(t,(0,34)); tiles.append(cell)
    if tiles:
        cw=420; ch=max(t.height for t in tiles); cols=5
        rows=(len(tiles)+cols-1)//cols
        sheet=Image.new("RGB",(cw*cols+8,ch*rows+8),(190,190,190))
        for k,t in enumerate(tiles): sheet.paste(t,((k%cols)*cw+4,(k//cols)*ch+4))
        sheet.save(os.path.join(DST,f"case{c}_sheet.png"))
        print(f"case{c}: {len(tiles)} imgs + sheet")
print("DONE")
