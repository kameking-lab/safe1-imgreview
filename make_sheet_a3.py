import os, glob, json
from PIL import Image, ImageDraw, ImageFont
D="refs/cand_A3"
files=sorted(glob.glob(os.path.join(D,"z*.*")))
cols,rows=8,6; cw,ch=300,300; pad=22
W=cols*cw; H=rows*ch
sheet=Image.new("RGB",(W,H),(245,245,245))
dr=ImageDraw.Draw(sheet)
try: font=ImageFont.truetype("C:/Windows/Fonts/consola.ttf",20)
except: font=ImageFont.load_default()
for i,f in enumerate(files):
    if i>=cols*rows: break
    r,c=divmod(i,cols); x,y=c*cw,r*ch
    try:
        im=Image.open(f).convert("RGB")
        im.thumbnail((cw-10,ch-pad-10))
        sheet.paste(im,(x+5,y+pad+3))
    except Exception as e:
        dr.text((x+5,y+pad+20),"ERR",fill=(200,0,0),font=font)
    dr.rectangle([x,y,x+cw-1,y+ch-1],outline=(180,180,180))
    dr.text((x+4,y+3),os.path.basename(f),fill=(0,0,0),font=font)
out="refs/cand_A3/_sheet_a3.png"
sheet.save(out)
print("saved",out,sheet.size,"n=",len(files))
