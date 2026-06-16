# -*- coding: utf-8 -*-
"""make_review_assets.py <ver>  各版の災害イラスト(clean)を GitHub公開用に整形。
出力: imgreview/v{n}_illust/01..06.png, v{n}_photo/01..06.png（最大幅1024）
      imgreview/v{n}_illust.png, v{n}_photo.png（6枚コンタクトシート, 各タイル幅640）
※守秘: 生の災害イラストのみ。ロゴ/テンプレ/社名/フッターは一切含まない。"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
BASE = r"C:\Users\kanet\20260522\safe1"
VER = sys.argv[1]
IMG = os.path.join(BASE, "imgreview")
def font(sz):
    for p in (r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc", r"C:\Windows\Fonts\msgothic.ttc"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()
F = font(30)
LAB = {1:"①墜落",2:"②はさまれ",3:"③荷の転倒",4:"④バケット墜落",5:"⑤車両転倒",6:"⑥上方はさまれ"}

def do(kind):
    sd = os.path.join(BASE, "images", f"{kind}_v{VER}_clean")
    if not os.path.isdir(sd):
        sd = os.path.join(BASE, "images", f"{kind}_v{VER}")  # clean無ければ生
    od = os.path.join(IMG, f"v{VER}_{kind}"); os.makedirs(od, exist_ok=True)
    tiles=[]
    for i in range(1,7):
        p = os.path.join(sd, f"gen{i:02d}.png")
        if not os.path.exists(p): continue
        im = Image.open(p).convert("RGB")
        if im.width>1024: im = im.resize((1024, round(im.height*1024/im.width)), Image.LANCZOS)
        im.save(os.path.join(od, f"{i:02d}.png"))
        t = im.resize((640, round(im.height*640/im.width)), Image.LANCZOS)
        bar = Image.new("RGB",(640,40),(20,20,20)); dr=ImageDraw.Draw(bar)
        dr.text((10,4), f"{i:02d} {LAB[i]}", fill=(255,255,255), font=F)
        cell = Image.new("RGB",(640, t.height+40),(255,255,255)); cell.paste(bar,(0,0)); cell.paste(t,(0,40))
        tiles.append(cell)
    if not tiles: print(f"{kind}: no images"); return
    cw=640; ch=max(t.height for t in tiles); cols=2; rows=3
    sheet=Image.new("RGB",(cw*cols+8, ch*rows+8),(190,190,190))
    for k,t in enumerate(tiles):
        x=(k%cols)*cw+ (4 if k%cols==0 else 4); y=(k//cols)*ch+4
        sheet.paste(t,((k%cols)*cw+4,(k//cols)*ch+4))
    sheet.save(os.path.join(IMG, f"v{VER}_{kind}.png"))
    print(f"v{VER}_{kind}: {len(tiles)} imgs + contact sheet {sheet.size}")

do("illust"); do("photo")
print("DONE")
