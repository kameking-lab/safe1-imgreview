# -*- coding: utf-8 -*-
"""cutout_white.py — 純白背景の画像を透過PNG化（rembg不在時のPillowフォールバック）。
使い方: py cutout_white.py <in.png> <out.png> [thresh=238]
外周から連結した白領域のみ透過にする（被写体内部の白＝ヘルメット等は残す）。輪郭1pxフェザー。"""
import sys
from collections import deque
from PIL import Image, ImageFilter

inp = sys.argv[1]; outp = sys.argv[2]
TH = int(sys.argv[3]) if len(sys.argv) > 3 else 238

im = Image.open(inp).convert("RGBA")
w, h = im.size
px = im.load()

def is_white(x, y):
    r, g, b, a = px[x, y]
    return r >= TH and g >= TH and b >= TH

# flood fill from the 4 borders over connected near-white pixels
mask = [[False]*w for _ in range(h)]
dq = deque()
for x in range(w):
    for y in (0, h-1):
        if is_white(x, y) and not mask[y][x]:
            mask[y][x] = True; dq.append((x, y))
for y in range(h):
    for x in (0, w-1):
        if is_white(x, y) and not mask[y][x]:
            mask[y][x] = True; dq.append((x, y))
while dq:
    x, y = dq.popleft()
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+dx, y+dy
        if 0 <= nx < w and 0 <= ny < h and not mask[ny][nx] and is_white(nx, ny):
            mask[ny][nx] = True; dq.append((nx, ny))

# build alpha: transparent where mask (exterior white)
alpha = Image.new("L", (w, h), 255)
ap = alpha.load()
for y in range(h):
    row = mask[y]
    for x in range(w):
        if row[x]:
            ap[x, y] = 0
# feather edge 1px to avoid white fringe
alpha = alpha.filter(ImageFilter.GaussianBlur(0.8))
im.putalpha(alpha)
im.save(outp)
# report transparent ratio
trans = sum(1 for y in range(h) for x in range(w) if mask[y][x])
print(f"WROTE {outp} transparent_px={trans} ({trans*100//(w*h)}%)")
