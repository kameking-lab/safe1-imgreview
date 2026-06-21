# -*- coding: utf-8 -*-
import win32com.client as win32, os
BASE=r"C:\Users\kanet\20260522\safe1"
src=os.path.join(BASE,"proposal_hakuten.pptx")
outdir=os.path.join(BASE,"qa_prop")
app=win32.Dispatch("PowerPoint.Application")
pres=app.Presentations.Open(src, WithWindow=False)
n=pres.Slides.Count
for i in range(1, n+1):
    out=os.path.join(outdir, "r3_slide%02d.png"%i)
    pres.Slides(i).Export(out, "PNG", 1920, 1080)
    print("OK", out)
pres.Close()
app.Quit()
print("DONE", n, "slides")
