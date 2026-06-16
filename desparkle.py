# -*- coding: utf-8 -*-
"""
desparkle.py [dir1 dir2 ...]  右下のGemini AIスパークル(✦)を除去し <dir>_clean に保存(非破壊)。
引数なしなら illust_v5/photo_v5 を処理(後方互換)。
手法: 右下コーナーで「左にshift px寄せた同じ行の背景」より明るい画素(=スター)だけを背景で置換+フェザー。
"""
import os, sys, numpy as np
from PIL import Image, ImageFilter
BASE = r"C:\Users\kanet\20260522\safe1"

def clean(path, outpath):
    im = Image.open(path).convert("RGB"); W,H = im.size
    arr = np.asarray(im).astype(np.int16)
    bw, bh, shift = 170, 150, 110
    x0, y0 = W-bw, H-bh
    region = arr[y0:H, x0:W].copy()
    src = arr[y0:H, x0-shift:W-shift].copy()
    diff = region.mean(axis=2) - src.mean(axis=2)
    mask = (diff > 16) & (region.mean(axis=2) > 120)
    m = Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2.0))
    ma = (np.asarray(m).astype(np.float32)/255.0)[...,None]
    arr2 = arr.astype(np.uint8).copy()
    arr2[y0:H, x0:W] = (region*(1-ma) + src*ma).astype(np.uint8)
    Image.fromarray(arr2).save(outpath)
    return int(mask.sum())

dirs = sys.argv[1:] or [r"images\illust_v5", r"images\photo_v5"]
for d in dirs:
    sd = os.path.join(BASE, d) if not os.path.isabs(d) else d
    od = sd + "_clean"; os.makedirs(od, exist_ok=True)
    for i in range(1,7):
        f = f"gen{i:02d}.png"; p = os.path.join(sd,f)
        if os.path.exists(p):
            n = clean(p, os.path.join(od,f)); print(f"{os.path.basename(sd)}/{f}: star_px={n}")
print("DONE")
