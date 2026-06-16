# -*- coding: utf-8 -*-
"""compare_illust_v17.pdf — 本番対比PDF（新ファイル・非破壊）。
1事例1ページ・A4横。左＝元写真（ベース採用）、右＝生成イラスト2枚（OpenAI/Google）を大きく対比。
illust_v17/ と illust_index_v17.csv を読むだけ。既存PDFは上書きしない。"""
import os, csv
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
CSVP = os.path.join(BASE, "illust_index_v17.csv")
OUT = os.path.join(BASE, "compare_illust_v17.pdf")
PW, PH = 1754, 1240          # A4横 @150dpi
M = 50
INK=(25,25,25); GRAY=(110,110,110); RED=(192,57,43)

def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b
              else [r"C:\Windows\Fonts\YuGothR.ttc",r"C:\Windows\Fonts\meiryo.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(34); FL=font(24); FS=font(19,False)

def have(p): return os.path.exists(os.path.join(BASE,p))

def draw_img(im,d,p,box,label):
    x,y,w,h=box
    d.rectangle([x,y-32,x+w,y-4],fill=(238,240,244)); d.text((x+8,y-30),label,font=FL,fill=INK)
    d.rectangle([x,y,x+w,y+h],fill=(245,245,245),outline=(205,205,205))
    fp=os.path.join(BASE,p)
    if os.path.exists(fp):
        try:
            pic=Image.open(fp).convert("RGB"); iw,ih=pic.size; s=min((w-10)/iw,(h-10)/ih)
            nw,nh=max(1,int(iw*s)),max(1,int(ih*s))
            im.paste(pic.resize((nw,nh),Image.LANCZOS),(x+(w-nw)//2,y+(h-nh)//2))
        except Exception: d.text((x+10,y+h//2),"(読込不可)",font=FS,fill=RED)
    else: d.text((x+10,y+h//2),"(未生成)",font=FS,fill=GRAY)

rows=list(csv.reader(open(CSVP,encoding="utf-8-sig")))
data=[r for r in rows[1:] if r and r[0].strip()]
pages=[]; cnt=0
for r in data:
    n=r[0].strip(); title=r[1].strip() if len(r)>1 else ""
    photo=r[2].strip() if len(r)>2 else f"photos_v16/{n}/base.png"
    ill_o=r[3].strip() if len(r)>3 else f"illust_v17/{n}/openai_illust.png"
    ill_g=r[4].strip() if len(r)>4 else f"illust_v17/{n}/google_illust.png"
    cnt+=1
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,84],fill=RED)
    head=f"{n}  {title}"
    while d.textlength(head,font=FT)>PW-2*M and len(head)>10: head=head[:-2]
    if head!=f"{n}  {title}": head=head+"…"
    d.text((M,16),head,font=FT,fill="white")
    d.text((M,58),"左：元写真（ベース採用）　／　右：事故事例イラスト（OpenAI・Google）— 物理破綻の緩和を対比",font=FS,fill=(255,235,230))
    top=156; bot=PH-86; gap=26
    # 左＝元写真（約45%幅・全高）／右＝イラスト2枚（上下に大きく）
    lw=int((PW-2*M-gap)*0.46); rx=M+lw+gap; rw=PW-2*M-gap-lw
    fh=bot-top
    draw_img(im,d,photo,(M,top,lw,fh),f"元写真（ベース）：{n}")
    rh=(fh-gap-32)//2  # ラベル帯ぶん控える
    draw_img(im,d,ill_o,(rx,top,rw,rh),"イラスト：OpenAI（gpt-image-2）")
    draw_img(im,d,ill_g,(rx,top+rh+32+gap,rw,rh),"イラスト：Google（gemini-3-pro-image-preview）")
    d.text((M,PH-66),"※イラストは base.png を参照に構図・事故の向き・接触点・機種・人数・PPE を保持し、画風のみKYT安全教育調へ変換。被災の瞬間を明確化（×印/矢印/衝撃線）。実在ロゴ無し・流血無し。",font=FS,fill=GRAY)
    pages.append(im)

if not pages: raise SystemExit("no cases")
pages[0].save(OUT,"PDF",save_all=True,append_images=pages[1:],resolution=150.0)
print("WROTE",OUT,"pages=",len(pages),"cases=",cnt)
