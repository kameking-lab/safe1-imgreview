# -*- coding: utf-8 -*-
"""cutout_rembg.py — rembg(U2Net)で背景除去して透過PNG化。
使い方: py cutout_rembg.py <in.png> <out.png>
被写体を残し背景を透過。白フチ低減のためalphaを軽く収縮(erode)。"""
import sys
from rembg import remove, new_session
from PIL import Image, ImageFilter

inp = sys.argv[1]; outp = sys.argv[2]
sess = new_session("u2net")
src = Image.open(inp).convert("RGBA")
out = remove(src, session=sess, alpha_matting=True,
             alpha_matting_foreground_threshold=240,
             alpha_matting_background_threshold=15,
             alpha_matting_erode_size=3)
# 軽くalphaを締めて白フチを抑制
r, g, b, a = out.split()
a = a.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
out = Image.merge("RGBA", (r, g, b, a))
out.save(outp)
nz = sum(1 for p in out.getdata() if p[3] > 8)
w, h = out.size
print(f"WROTE {outp} opaque_px={nz} ({nz*100//(w*h)}%)")
