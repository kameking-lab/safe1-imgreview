# -*- coding: utf-8 -*-
"""compare_event_v22.pdf — 展示会場 設営中 高所作業車「危険姿勢→事故の流れを矢印で図示」KYT対比PDF
（新ファイル・非破壊）。1元絵1ページ・A4横。
見出し＝元番号＋事故の型。帯＝「危険姿勢の内容」＋「矢印が示す事故への流れ」。
左＝元イラスト（collect_aerial2 収集・出所付）、
右＝生成2枚（Google-1/Google-2／gemini-3-pro-image-preview・危険姿勢＋予測矢印版）を大きくラベル付きで対比。
gen_event_v22/event_index_v22.csv と collect_aerial2/ を読むだけ。既存PDFは上書きしない。"""
import os, csv
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
GENDIR = os.path.join(BASE, "gen_event_v22")
IDXP = os.path.join(GENDIR, "event_index_v22.csv")
AERP = os.path.join(BASE, "collect_aerial2", "aerial2_index.csv")
IMGDIR = os.path.join(BASE, "collect_aerial2", "img")
OUT = os.path.join(BASE, "compare_event_v22.pdf")
PW, PH = 1754, 1240          # A4横 @150dpi
M = 50
INK=(25,25,25); GRAY=(110,110,110); RED=(192,57,43)
POSEBG=(252,246,236); ARROWBG=(247,237,233)

def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b
              else [r"C:\Windows\Fonts\YuGothR.ttc",r"C:\Windows\Fonts\meiryo.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(34); FL=font(23); FS=font(19,False); FC=font(21,False); FCB=font(21)

def wrap(text, ft, maxw):
    """日本語（空白区切り無し）対応の幅基準の折返し。"""
    lines=[]; cur=""
    for ch in text:
        if ch=="\n":
            lines.append(cur); cur=""; continue
        t=cur+ch
        if ft.getlength(t)<=maxw: cur=t
        else: lines.append(cur); cur=ch
    if cur: lines.append(cur)
    return lines

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

def cause_band(im,d,cx,cy,cw,head,body,headcol,bg,outl):
    """見出し付きの折返し帯を描き、次のyを返す。"""
    lines=wrap(head+body, FC, cw-24)
    clh=29; bh=18+len(lines)*clh+10
    d.rectangle([cx,cy,cx+cw,cy+bh],fill=bg,outline=outl)
    ty=cy+10
    for i,ln in enumerate(lines):
        d.text((cx+12,ty),ln,font=(FCB if i==0 else FC),fill=headcol if i==0 else INK)
        ty+=clh
    return cy+bh

# 出所ドメイン・元ファイル名（番号→）を aerial2_index.csv から
domain={}; srcname={}
for r in csv.reader(open(AERP,encoding="utf-8-sig")):
    if r and r[0].strip().isdigit():
        n=r[0].strip()
        srcname[n]=r[1].strip() if len(r)>1 else ""
        domain[n]=r[5].strip() if len(r)>5 else ""

rows=list(csv.reader(open(IDXP,encoding="utf-8-sig")))
data=[r for r in rows[1:] if r and r[0].strip()]
pages=[]
for r in data:
    n=r[0].strip(); atype=r[1].strip(); pose=r[2].strip(); arrow=r[3].strip()
    g1=r[4].strip(); g2=r[5].strip()
    dom=domain.get(n,""); srcfile=srcname.get(n,"")
    srcfp=os.path.join(IMGDIR,srcfile) if srcfile else ""
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    # 見出し帯：番号＋事故の型
    d.rectangle([0,0,PW,84],fill=RED)
    d.text((M,16),f"番号{n}  事故の型：{atype}",font=FT,fill="white")
    d.text((M,58),"危険姿勢→事故の流れを赤橙の予測矢印で図示（KYT）　左：元イラスト（aerial2 収集・出所付）　／　右：生成2枚（展示会場ブース設営版・Google×2）",font=FS,fill=(255,235,230))
    # 危険姿勢の帯 → 矢印が示す流れの帯
    cx=M; cw=PW-2*M; cy=96
    cy=cause_band(im,d,cx,cy,cw,"【危険姿勢の内容】",pose,(120,60,20),POSEBG,(220,200,170))
    cy+=10
    cy=cause_band(im,d,cx,cy,cw,"【矢印が示す事故への流れ】",arrow,(150,40,20),ARROWBG,(225,180,165))
    # 画像領域
    top=cy+44; bot=PH-66; gap=24
    lw=int((PW-2*M-gap)*0.46); rx=M+lw+gap; rw=PW-2*M-gap-lw
    fh=bot-top
    draw_img(im,d,srcfp,(M,top,lw,fh),f"元イラスト：{srcfile}　出所：{dom}")
    cellw=(rw-gap)//2
    draw_img(im,d,os.path.join(GENDIR,n,g1),(rx,top,cellw,fh),"Google-1（gemini-3-pro-image-preview）")
    draw_img(im,d,os.path.join(GENDIR,n,g2),(rx+cellw+gap,top,cellw,fh),"Google-2（gemini-3-pro-image-preview）")
    d.text((M,PH-52),"※元絵の事故の型を踏襲し、舞台を展示会場ブース設営現場へ置換。高所作業車はシザース型に統一。危険姿勢＋事故への遷移を示す赤橙の湾曲予測矢印を同一画面に描写。矢印以外の文字/キャプション/吹き出し無し・流血無し・実在ロゴ無し・PPE適切。",font=FS,fill=GRAY)
    pages.append(im)

if not pages: raise SystemExit("no data")
pages[0].save(OUT,"PDF",save_all=True,append_images=pages[1:],resolution=150.0)
print("WROTE",OUT,"pages=",len(pages))

if os.environ.get("V22_QA"):
    nums=[r[0].strip() for r in data]
    for tgt in ("1","91","497","914"):
        if tgt in nums:
            pages[nums.index(tgt)].save(os.path.join(BASE,f"_v22qa_{tgt}.png"))
    print("QA PNGs written")
