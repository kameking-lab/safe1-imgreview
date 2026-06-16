from PIL import Image, ImageDraw
import os, json
d='refs/cand_T5'
files=sorted([f for f in os.listdir(d) if not f.startswith('_')])
cols=6; thumb=260; pad=24; lab=18
rows=(len(files)+cols-1)//cols
W=cols*(thumb+pad)+pad; H=rows*(thumb+pad+lab)+pad
sheet=Image.new('RGB',(W,H),(245,245,245))
dr=ImageDraw.Draw(sheet)
for i,fn in enumerate(files):
    try:
        im=Image.open(os.path.join(d,fn)).convert('RGB')
    except Exception:
        continue
    im.thumbnail((thumb,thumb))
    r,c=divmod(i,cols)
    x=pad+c*(thumb+pad); y=pad+r*(thumb+pad+lab)
    sheet.paste(im,(x,y))
    dr.text((x,y+thumb+2),fn.split('.')[0],fill=(0,0,0))
sheet.save('refs/cand_T5/_sheet.png')
print('rows',rows,'files',len(files))
