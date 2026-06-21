# -*- coding: utf-8 -*-
from PIL import Image
import os
BASE=r"C:\Users\kanet\20260522\safe1\qa_prop"
for s in (9,10):
    im=Image.open(os.path.join(BASE,"r4_slide%02d.png"%s))
    w,h=im.size
    # bottom table region
    im.crop((0,int(h*0.46),w,h)).save(os.path.join(BASE,"r4_s%02d_bot.png"%s))
    # top photos region
    im.crop((0,0,w,int(h*0.50))).save(os.path.join(BASE,"r4_s%02d_top.png"%s))
print("OK")
