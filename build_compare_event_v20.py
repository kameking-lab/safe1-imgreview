# -*- coding: utf-8 -*-
"""compare_event_v20.pdf — 展示会場 設営中の事故事例イラスト 対比PDF（新ファイル・非破壊）。
1元絵1ページ・A4横。見出し＝元番号＋事故の型。
左＝元イラスト（collect_aerial2 収集・出所ドメイン付）、
右＝生成4枚（OpenAI-1/OpenAI-2/Google-1/Google-2）を大きくラベル付きで2x2に対比。
gen_event_v20/event_index_v20.csv と collect_aerial2/ を読むだけ。既存PDFは上書きしない。"""
import os, csv
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
GENDIR = os.path.join(BASE, "gen_event_v20")
IDXP = os.path.join(GENDIR, "event_index_v20.csv")
AERP = os.path.join(BASE, "collect_aerial2", "aerial2_index.csv")
IMGDIR = os.path.join(BASE, "collect_aerial2", "img")
OUT = os.path.join(BASE, "compare_event_v20.pdf")
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
FT=font(34); FL=font(23); FS=font(19,False)

def draw_img(im,d,fp,box,label):
    x,y,w,h=box
    d.rectangle([x,y-32,x+w,y-4],fill=(238,240,244)); d.text((x+8,y-30),label,font=FL,fill=INK)
    d.rectangle([x,y,x+w,y+h],fill=(245,245,245),outline=(205,205,205))
    if fp and os.path.exists(fp):
        try:
            pic=Image.open(fp).convert("RGB"); iw,ih=pic.size; s=min((w-10)/iw,(h-10)/ih)
            nw,nh=max(1,int(iw*s)),max(1,int(ih*s))
            im.paste(pic.resize((nw,nh),Image.LANCZOS),(x+(w-nw)//2,y+(h-nh)//2))
        except Exception: d.text((x+10,y+h//2),"(読込不可)",font=FS,fill=RED)
    else: d.text((x+10,y+h//2),"(未生成)",font=FS,fill=GRAY)

# 出所ドメイン（番号→domain）を aerial2_index.csv から
domain={}
for r in csv.reader(open(AERP,encoding="utf-8-sig")):
    if r and r[0].strip().isdigit(): domain[r[0].strip()]=r[5].strip() if len(r)>5 else ""

rows=list(csv.reader(open(IDXP,encoding="utf-8-sig")))
data=[r for r in rows[1:] if r and r[0].strip()]
pages=[]
for r in data:
    n=r[0].strip(); srcfile=r[1].strip(); atype=r[2].strip()
    o1,o2,g1,g2=r[4].strip(),r[5].strip(),r[6].strip(),r[7].strip()
    dom=domain.get(n,"")
    srcfp=os.path.join(IMGDIR,srcfile)
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,84],fill=RED)
    head=f"番号{n}  事故の型：{atype}"
    d.text((M,16),head,font=FT,fill="white")
    d.text((M,58),"左：元イラスト（aerial2 収集）　／　右：生成4枚（展示会場ブース設営版・OpenAI×2／Google×2）",font=FS,fill=(255,235,230))
    top=156; bot=PH-86; gap=24
    lw=int((PW-2*M-gap)*0.46); rx=M+lw+gap; rw=PW-2*M-gap-lw
    fh=bot-top
    draw_img(im,d,srcfp,(M,top,lw,fh),f"元イラスト：{srcfile}　出所：{dom}")
    cellw=(rw-gap)//2; cellh=(fh-gap-32)//2
    draw_img(im,d,os.path.join(GENDIR,n,o1),(rx,top,cellw,cellh),"OpenAI-1（gpt-image-2 high）")
    draw_img(im,d,os.path.join(GENDIR,n,o2),(rx+cellw+gap,top,cellw,cellh),"OpenAI-2（gpt-image-2 high）")
    draw_img(im,d,os.path.join(GENDIR,n,g1),(rx,top+cellh+32+gap,cellw,cellh),"Google-1（gemini-3-pro-image）")
    draw_img(im,d,os.path.join(GENDIR,n,g2),(rx+cellw+gap,top+cellh+32+gap,cellw,cellh),"Google-2（gemini-3-pro-image）")
    d.text((M,PH-66),"※元絵の事故の型・構図・被災状況を引継ぎ、舞台を展示会場ブース設営現場へ置換。高所作業車はシザース型に統一。事故の瞬間を明確化。文字/矢印/キャプション無し・流血無し・実在ロゴ無し。",font=FS,fill=GRAY)
    pages.append(im)

if not pages: raise SystemExit("no data")
pages[0].save(OUT,"PDF",save_all=True,append_images=pages[1:],resolution=150.0)
print("WROTE",OUT,"pages=",len(pages))
