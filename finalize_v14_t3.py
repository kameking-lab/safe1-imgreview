# -*- coding: utf-8 -*-
"""P-T3 finalize: 採用候補(c02/c08/c06)のラウンドカード枠を自動トリムして
v14/T3/01-03.png に確定し、元絵+3枚の T3_sheet.png を作る。非破壊(新ファイル名)。"""
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

BASE = r"C:\Users\kanet\20260522\safe1"
CAND = os.path.join(BASE, "v14", "T3", "cand")
OUT  = os.path.join(BASE, "v14", "T3")
REF  = os.path.join(BASE, "refs", "I-T3_ref.png")

# 採用候補 -> 確定番号（アングル違い・接触点/向き/機種は不変）
PICKS = [("c02.png", "01"),  # 斜後/やや高所: 板が傾斜板を滑落し下の作業者を下敷き
         ("c08.png", "02"),  # ローアングル: 後傾板から板が滑落し作業者を下敷き
         ("c06.png", "03")]  # 水平3/4: 滑落した板の下に作業者

def autotrim(im, tol=18, border=2):
    """周辺のラウンドカード枠(ほぼ均一な明色)を四辺から検出して切り落とす。"""
    arr = np.asarray(im.convert("RGB")).astype(np.int16)
    H, W, _ = arr.shape
    # 四隅の平均を枠色とみなす
    cs = 6
    corners = np.concatenate([
        arr[:cs, :cs].reshape(-1, 3), arr[:cs, -cs:].reshape(-1, 3),
        arr[-cs:, :cs].reshape(-1, 3), arr[-cs:, -cs:].reshape(-1, 3)])
    bg = corners.mean(axis=0)
    diff = np.abs(arr - bg).sum(axis=2)            # 枠色との差
    rowmask = (diff > tol).mean(axis=1) > 0.20     # 行に内容が2割以上
    colmask = (diff > tol).mean(axis=0) > 0.20
    ys = np.where(rowmask)[0]; xs = np.where(colmask)[0]
    if len(ys) == 0 or len(xs) == 0:
        return im
    y0, y1 = max(ys[0]-0, 0), min(ys[-1]+1, H)
    x0, x1 = max(xs[0]-0, 0), min(xs[-1]+1, W)
    # 角の丸み分を少し内側へ
    y0 += border; x0 += border; y1 -= border; x1 -= border
    return im.crop((x0, y0, x1, y1))

finals = []
for src, num in PICKS:
    sp = os.path.join(CAND, src)
    im = Image.open(sp).convert("RGB")
    # 確定前の生プレビューを保存（再開/検証用・非破壊）
    im.save(os.path.join(CAND, f"prev_{num}.png"))
    tr = autotrim(im)
    outp = os.path.join(OUT, f"{num}.png")
    tr.save(outp)
    finals.append((outp, num))
    print("saved", outp, tr.size, "<-", src)

# シート: 元絵 + 確定3枚
imgs = [("元絵 I-T3_ref", Image.open(REF).convert("RGB"))]
for outp, num in finals:
    imgs.append((num, Image.open(outp).convert("RGB")))
cell = 760; pad = 28; lab = 30; cols = 2
rows = (len(imgs) + cols - 1) // cols
W = cols * cell + (cols + 1) * pad
H = rows * (cell + lab) + (rows + 1) * pad
sheet = Image.new("RGB", (W, H), (244, 244, 246))
dr = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
except Exception:
    font = ImageFont.load_default()
for i, (label, im) in enumerate(imgs):
    im = im.copy(); im.thumbnail((cell, cell))
    r, c = divmod(i, cols)
    x = pad + c * (cell + pad); y = pad + r * (cell + lab + pad)
    x += (cell - im.size[0]) // 2
    sheet.paste(im, (x, y))
    dr.text((pad + c * (cell + pad), y + im.size[1] + 4), label, fill=(20, 20, 20), font=font)
sheet.save(os.path.join(OUT, "T3_sheet.png"))
print("sheet ->", os.path.join(OUT, "T3_sheet.png"), sheet.size)
