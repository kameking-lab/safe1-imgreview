# -*- coding: utf-8 -*-
"""P-T5 finalize: 採用候補(c01/c03/c05)を v14/T5/01-03.png に確定し、
元絵+3枚の T5_sheet.png を作る。非破壊(新ファイル名のみ作成)。
コーナーのスパークル(★)は隣接パッチで除去。"""
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

BASE = r"C:\Users\kanet\20260522\safe1"
CAND = os.path.join(BASE, "v14", "T5", "cand")
OUT  = os.path.join(BASE, "v14", "T5")
REF  = os.path.join(BASE, "refs", "I-T5_ref.gif")

# 採用候補 -> 確定番号（アングル違い・接触点=足の挟み込み/向き/機種は不変）
# desparkle=True の画像は右下コーナーのスパークルを隣接パッチで除去
PICKS = [("c01.png", "01", False),  # 真横: 下降昇降板の縁と地面の間で足はさまれ(接触点最明瞭)
         ("c03.png", "02", True),   # ローアングル: 地面へ降りる昇降板の縁で足を踏み込み挟まれ
         ("c05.png", "03", False)]  # 斜後/やや高所: 昇降板縁(縞鋼板)と地面の境界で足はさまれ

def autotrim(im, tol=18, border=2):
    """周辺のほぼ均一な明色枠を四辺から検出して切り落とす(枠が無ければそのまま)。"""
    arr = np.asarray(im.convert("RGB")).astype(np.int16)
    H, W, _ = arr.shape
    cs = 6
    corners = np.concatenate([
        arr[:cs, :cs].reshape(-1, 3), arr[:cs, -cs:].reshape(-1, 3),
        arr[-cs:, :cs].reshape(-1, 3), arr[-cs:, -cs:].reshape(-1, 3)])
    bg = corners.mean(axis=0)
    diff = np.abs(arr - bg).sum(axis=2)
    rowmask = (diff > tol).mean(axis=1) > 0.20
    colmask = (diff > tol).mean(axis=0) > 0.20
    ys = np.where(rowmask)[0]; xs = np.where(colmask)[0]
    if len(ys) == 0 or len(xs) == 0:
        return im
    y0, y1 = max(ys[0]-0, 0), min(ys[-1]+1, H)
    x0, x1 = max(xs[0]-0, 0), min(xs[-1]+1, W)
    y0 += border; x0 += border; y1 -= border; x1 -= border
    return im.crop((x0, y0, x1, y1))

def desparkle_corner(im):
    """右下コーナーのスパークル(★)を、その左隣の同寸パッチで上書きして消す(非破壊・新出力)。"""
    im = im.copy()
    W, H = im.size
    bw = int(W * 0.12); bh = int(H * 0.14)
    x0, y0 = W - bw, H - bh
    src_x = max(0, x0 - bw)               # 箱のすぐ左の同寸領域を採取
    patch = im.crop((src_x, y0, src_x + bw, H))
    im.paste(patch, (x0, y0))
    return im

finals = []
for src, num, despk in PICKS:
    sp = os.path.join(CAND, src)
    im = Image.open(sp).convert("RGB")
    im.save(os.path.join(CAND, f"prev_{num}.png"))  # 生プレビュー(再開/検証用)
    tr = autotrim(im)
    if despk:
        tr = desparkle_corner(tr)
    outp = os.path.join(OUT, f"{num}.png")
    tr.save(outp)
    finals.append((outp, num))
    print("saved", outp, tr.size, "<-", src, "despk=", despk)

# シート: 元絵 + 確定3枚
imgs = [("元絵 I-T5_ref", Image.open(REF).convert("RGB"))]
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
sheet.save(os.path.join(OUT, "T5_sheet.png"))
print("sheet ->", os.path.join(OUT, "T5_sheet.png"), sheet.size)
