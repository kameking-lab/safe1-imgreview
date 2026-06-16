# -*- coding: utf-8 -*-
"""全17スライドPNGを横1280pxに揃え、上端に番号ラベル帯を付けて縦連結する。"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
W = 1280
LABEL_H = 36
GAP = 6
TITLES = {
 1:"表紙",2:"統計｜TGL災害",3:"統計｜高所作業車",
 4:"事例① TGL 昇降板からの墜落(概要)",5:"事例① 表",
 6:"事例② TGL 昇降中のはさまれ(概要)",7:"事例② 表",
 8:"事例③ カゴ車の転倒・下敷き(概要)",9:"事例③ 表",
 10:"事例④ バケットからの墜落(概要)",11:"事例④ 表",
 12:"事例⑤ 走行・旋回中の転倒(概要)",13:"事例⑤ 表",
 14:"事例⑥ 上方構造物とのはさまれ(概要)",15:"事例⑥ 表",
 16:"現場チェックリスト",17:"出典・参考資料",
}
def font(sz):
    for p in (r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\msgothic.ttc"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

F = font(22)

def build(kind):
    d = os.path.join(BASE, "render", kind)
    fs = sorted([f for f in os.listdir(d) if f.endswith(".png")])
    tiles = []
    for i, f in enumerate(fs, start=1):
        im = Image.open(os.path.join(d, f)).convert("RGB")
        if im.width != W:
            im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        bar = Image.new("RGB", (W, LABEL_H), (28, 28, 28))
        dr = ImageDraw.Draw(bar)
        dr.text((14, 6), f"{i:02d}  {TITLES.get(i,'')}", fill=(255, 255, 255), font=F)
        tiles.append(bar); tiles.append(im)
        tiles.append(Image.new("RGB", (W, GAP), (210, 210, 210)))
    total_h = sum(t.height for t in tiles)
    canvas = Image.new("RGB", (W, total_h), (255, 255, 255))
    y = 0
    for t in tiles:
        canvas.paste(t, (0, y)); y += t.height
    out = os.path.join(BASE, "review2", "img", f"{kind}_all.png")
    canvas.save(out, optimize=True)
    print(f"{kind}_all.png  {canvas.size}  {os.path.getsize(out)//1024} KB")

build("illust_v5")
build("photo_v5")
print("DONE")
