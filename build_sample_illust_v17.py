# -*- coding: utf-8 -*-
"""sample_illust_v17.pdf — 途中サンプル。完成事例の 元写真 vs イラスト(OpenAI/Google) 対比。
本番 compare_illust_v17.pdf とは別名・非破壊。illust_v17/ と illust_index_v17.csv を読むだけ。A4横。"""
import os, csv
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
CSVP = os.path.join(BASE, "illust_index_v17.csv")
OUT = os.path.join(BASE, "sample_illust_v17.pdf")
PW, PH = 1754, 1240
M = 50
INK=(25,25,25); GRAY=(110,110,110); RED=(192,57,43)

def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(32); FL=font(23); FS=font(19,False)

rows=list(csv.reader(open(CSVP,encoding="utf-8-sig")))
data=[r for r in rows[1:] if r and r[0].strip()]
# cols: 0 新No,1 事故タイトル,2 元写真,3 イラストOpenAI,4 イラストGoogle
pages=[]
def have(p): return os.path.exists(os.path.join(BASE,p))
def draw_img(im,d,p,box,label):
    x,y,w,h=box
    d.rectangle([x,y-30,x+w,y-4],fill=(238,240,244)); d.text((x+8,y-28),label,font=FL,fill=INK)
    d.rectangle([x,y,x+w,y+h],fill=(245,245,245),outline=(205,205,205))
    fp=os.path.join(BASE,p)
    if os.path.exists(fp):
        try:
            pic=Image.open(fp).convert("RGB"); iw,ih=pic.size; s=min((w-10)/iw,(h-10)/ih)
            nw,nh=max(1,int(iw*s)),max(1,int(ih*s)); im.paste(pic.resize((nw,nh),Image.LANCZOS),(x+(w-nw)//2,y+(h-nh)//2))
        except Exception: d.text((x+10,y+h//2),"(読込不可)",font=FS,fill=RED)
    else: d.text((x+10,y+h//2),"(未生成)",font=FS,fill=GRAY)

cnt=0
for r in data:
    n=r[0].strip(); title=r[1].strip() if len(r)>1 else ""
    photo=r[2].strip() if len(r)>2 else f"photos_v16/{n}/base.png"
    ill_o=r[3].strip() if len(r)>3 else f"illust_v17/{n}/openai_illust.png"
    ill_g=r[4].strip() if len(r)>4 else f"illust_v17/{n}/google_illust.png"
    if not (have(ill_o) and have(ill_g)): continue
    cnt+=1
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,82],fill=RED)
    head=f"{n}  {title}"
    d.text((M,14),head if d.textlength(head,font=FT)<PW-2*M else head[:46]+"…",font=FT,fill="white")
    d.text((M,54),"元写真（ベース採用）vs 事故事例イラスト（OpenAI / Google）— 物理破綻の緩和を対比",font=FS,fill=(255,235,230))
    gap=24; cw=(PW-2*M-2*gap)//3; top=150; ih=PH-top-80; x=M
    draw_img(im,d,photo,(x,top,cw,ih),"元写真（ベース）"); x+=cw+gap
    draw_img(im,d,ill_o,(x,top,cw,ih),"イラスト：OpenAI"); x+=cw+gap
    draw_img(im,d,ill_g,(x,top,cw,ih),"イラスト：Google")
    d.text((M,PH-60),"※イラストは base.png を参照に構図・向き・接触点・機種・PPEを保持しKYT安全教育調へ変換。被災の瞬間を明確化（×印/矢印）。実在ロゴ無し・流血無し。途中サンプル（完成分のみ）。",font=FS,fill=GRAY)
    pages.append(im)

if not pages: raise SystemExit("no complete illust sets")
pages[0].save(OUT,"PDF",save_all=True,append_images=pages[1:],resolution=150.0)
print("WROTE",OUT,"pages=",len(pages),"cases=",cnt)
