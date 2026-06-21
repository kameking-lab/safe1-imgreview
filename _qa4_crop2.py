# -*- coding: utf-8 -*-
from PIL import Image
import os
BASE=r"C:\Users\kanet\20260522\safe1\qa_prop"
for s in (9,10):
    im=Image.open(os.path.join(BASE,"r4_slide%02d.png"%s))
    w,h=im.size
    # just the 4-row table body, left half
    im.crop((0,int(h*0.50),int(w*0.55),int(h*0.92))).save(os.path.join(BASE,"r4_s%02d_tblL.png"%s))
    im.crop((int(w*0.45),int(h*0.50),w,int(h*0.92))).save(os.path.join(BASE,"r4_s%02d_tblR.png"%s))
print("OK")
