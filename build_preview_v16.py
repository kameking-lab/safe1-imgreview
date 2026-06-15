# -*- coding: utf-8 -*-
"""preview_v16.pdf — リアル化画像 途中プレビュー。1事例1ページ・横3枚(base/OpenAI/Google)大判。
photos_v16/ と img_index_v16.csv を読むだけ。新規生成・破壊なし。A4横。"""
import os, csv
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
PV16 = os.path.join(BASE, "photos_v16")
CSVP = os.path.join(BASE, "img_index_v16.csv")
OUT = os.path.join(BASE, "preview_v16.pdf")

PW, PH = 1754, 1240   # A4 landscape @150dpi
M = 50
INK=(25,25,25); GRAY=(110,110,110); BLUE=(11,102,195); RED=(192,57,43)

def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(34); FL=font(24); FS=font(20,False)

rows=list(csv.reader(open(CSVP,encoding="utf-8-sig")))
hdr=rows[0]; data=[r for r in rows[1:] if r and r[0].strip()]
# columns: 0 新No,1 旧番号,2 創作タイトル,3 元採用案,4 base,5 openai,6 google
SLOTS=[("base.png","ベース（前回採用案）"),("openai.png","OpenAI リアル化"),("google.png","Google リアル化")]

def complete(n):
    return all(os.path.exists(os.path.join(PV16,n,f)) for f,_ in SLOTS)

pages=[]
def wrap(d,t,f,mw):
    o,c=[],""
    for ch in t:
        if d.textlength(c+ch,font=f)<=mw: c+=ch
        else: o.append(c); c=ch
    if c: o.append(c)
    return o

cnt=0
for r in data:
    n=r[0].strip(); old=r[1].strip() if len(r)>1 else ""; title=r[2].strip() if len(r)>2 else ""; adopt=r[3].strip() if len(r)>3 else ""
    if not complete(n): continue
    cnt+=1
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,86],fill=RED)
    head=f"{n}  {title}"
    d.text((M,16),head if d.textlength(head,font=FT)<PW-2*M else head[:46]+"…",font=FT,fill="white")
    d.text((M,58),f"旧番号 #{old} ／ 前回採用案 {adopt}（リアル化＋イベント設営版／3案・選抜用）",font=FS,fill=(255,235,230))
    # 3 images across
    gap=24; cw=(PW-2*M-2*gap)//3; top=150; ih=PH-top-90
    x=M
    for f,label in SLOTS:
        d.rectangle([x,top-34,x+cw,top-6],fill=(238,240,244))
        d.text((x+8,top-32),label,font=FL,fill=INK)
        d.rectangle([x,top,x+cw,top+ih],fill=(245,245,245),outline=(205,205,205))
        p=os.path.join(PV16,n,f)
        try:
            pic=Image.open(p).convert("RGB"); iw,ih0=pic.size
            s=min((cw-10)/iw,(ih-10)/ih0); nw,nh=max(1,int(iw*s)),max(1,int(ih0*s))
            im.paste(pic.resize((nw,nh),Image.LANCZOS),(x+(cw-nw)//2,top+(ih-nh)//2))
        except Exception:
            d.text((x+10,top+ih//2),"(読込不可)",font=FS,fill=RED)
        x+=cw+gap
    d.text((M,PH-66),"※ベース＝前回採用案のコピー。OpenAI（gpt-image-2）／Google（Nano Banana Pro）で写真リアル化＋展示会・イベント設営の想定事故に寄せた創作。日本の会場・PPE・実在ロゴ無し・流血無し。",font=FS,fill=GRAY)
    d.text((PW-M-110,PH-40),f"preview_v16",font=font(16,False),fill=GRAY)
    pages.append(im)

if not pages:
    raise SystemExit("no complete sets")
pages[0].save(OUT,"PDF",save_all=True,append_images=pages[1:],resolution=150.0)
print("WROTE",OUT,"pages=",len(pages),"cases=",cnt)
