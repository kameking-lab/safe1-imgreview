# -*- coding: utf-8 -*-
"""build_compare_3way.py — 元イラスト vs 写真 vs 生成イラスト(OpenAI/Google) の4枚対比。
map_3way.md と compare_3way_v17.pdf を出力。既存は読むだけ・非破壊・新名。A4横。"""
import os, csv
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
OUTPDF = os.path.join(BASE, "compare_3way_v17.pdf")
MAPMD = os.path.join(BASE, "map_3way.md")

# 新No -> 旧番号 (from img_index_v16.csv)
v16 = {r[0].strip(): r[1].strip() for r in csv.reader(open(os.path.join(BASE,"img_index_v16.csv"),encoding="utf-8-sig")) if r and r[0].strip().startswith("N")}
titles = {r[0].strip(): r[2].strip() for r in csv.reader(open(os.path.join(BASE,"img_index_v16.csv"),encoding="utf-8-sig")) if r and r[0].strip().startswith("N")}
# 旧番号 -> (file,url) from collect2/img_index.csv
c2 = {}
for r in csv.reader(open(os.path.join(BASE,"collect2","img_index.csv"),encoding="utf-8-sig")):
    if r and r[0].strip() and r[0].strip()[0].isdigit():
        c2[r[0].strip()] = (r[1].strip(), r[4].strip() if len(r)>4 else "")

ORDER = [f"N{ i:02d}" for i in range(1,16)]

def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(30); FL=font(21); FS=font(17,False); FU=font(15,False)
INK=(25,25,25); GRAY=(110,110,110); RED=(192,57,43); BLUE=(11,102,195)
PW,PH=1754,1240; M=44

def dom(u):
    try: return urlparse(u).netloc or ""
    except: return ""

# ---- build map_3way.md ----
mlines=["# map_3way.md — 元イラスト / 写真 / 生成イラスト 対応表","",
        "| 新No | 旧番号 | 元イラスト(collect2) | 出所 | 写真(base) | 生成イラスト |","|---|---|---|---|---|---|"]
rows=[]
for n in ORDER:
    old=v16.get(n,"")
    src=c2.get(old,("",""))
    srcfile=src[0]; srcurl=src[1]
    srcpath=os.path.join(BASE,"collect2","img",srcfile) if srcfile else ""
    has_src = bool(srcfile) and os.path.exists(srcpath)
    base=os.path.join(BASE,"photos_v16",n,"base.png")
    oai=os.path.join(BASE,"illust_v17",n,"openai_illust.png")
    ggl=os.path.join(BASE,"illust_v17",n,"google_illust.png")
    rows.append(dict(n=n,old=old,srcfile=srcfile,srcurl=srcurl,srcpath=srcpath,has_src=has_src,base=base,oai=oai,ggl=ggl,title=titles.get(n,"")))
    mlines.append(f"| {n} | #{old} | {srcfile or '該当なし'} | {dom(srcurl)} | photos_v16/{n}/base.png | openai_illust/google_illust |")
mlines.append("")
mlines.append("※元イラスト＝collect2 で収集した本物の事故イラスト/図（出所URL付）。旧番号は img_index_v16.csv の対応。")
open(MAPMD,"w",encoding="utf-8").write("\n".join(mlines))

# ---- build PDF ----
def load(p):
    try:
        im=Image.open(p)
        if getattr(im,"is_animated",False): im.seek(0)
        return im.convert("RGB")
    except Exception: return None

def cell(im,d,path,box,label,sub=""):
    x,y,w,h=box
    d.rectangle([x,y-28,x+w,y-4],fill=(238,240,244)); d.text((x+6,y-26),label,font=FL,fill=INK)
    if sub: d.text((x+6,y+h+4),sub,font=FU,fill=BLUE)
    d.rectangle([x,y,x+w,y+h],fill=(245,245,245),outline=(205,205,205))
    pic=load(path) if path else None
    if pic is None:
        d.text((x+10,y+h//2-10),"元イラスト該当なし" if "元" in label else "(未生成)",font=FS,fill=GRAY); return
    iw,ih=pic.size; s=min((w-8)/iw,(h-8)/ih); nw,nh=max(1,int(iw*s)),max(1,int(ih*s))
    im.paste(pic.resize((nw,nh),Image.LANCZOS),(x+(w-nw)//2,y+(h-nh)//2))

pages=[]
for r in rows:
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,76],fill=RED)
    head=f"{r['n']}  {r['title']}  （元#{r['old']}）"
    d.text((M,12),head if d.textlength(head,font=FT)<PW-2*M else head[:42]+"…",font=FT,fill="white")
    d.text((M,50),"①元イラスト(収集・本物の事故図) vs ②写真(ベース) vs ③④生成イラスト — 模倣になっていないか対比",font=FS,fill=(255,235,230))
    gap=20; cw=(PW-2*M-3*gap)//4; top=140; ih=PH-top-90; x=M
    cell(im,d,r["srcpath"] if r["has_src"] else "",(x,top,cw,ih),"①元イラスト",("出所:"+dom(r["srcurl"]) if r["has_src"] else "")); x+=cw+gap
    cell(im,d,r["base"],(x,top,cw,ih),"②写真(ベース)"); x+=cw+gap
    cell(im,d,r["oai"],(x,top,cw,ih),"③イラスト:OpenAI"); x+=cw+gap
    cell(im,d,r["ggl"],(x,top,cw,ih),"④イラスト:Google")
    d.text((M,PH-58),"①は collect2 収集の実在事故イラスト（出所URL付）。③④は②写真を参照に再生成したイラスト。①と③④を見比べ“似すぎ(模倣)”でないか確認用。実在ロゴ無し・流血無し。",font=FU,fill=GRAY)
    pages.append(im)

pages[0].save(OUTPDF,"PDF",save_all=True,append_images=pages[1:],resolution=150.0)
nsrc=sum(1 for r in rows if r["has_src"])
print("WROTE",OUTPDF,"pages=",len(pages),"with_src=",nsrc,"/",len(rows))
