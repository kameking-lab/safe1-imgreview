# -*- coding: utf-8 -*-
"""build_candidates_pdf.py : 60候補を事例ごとに並べた candidates_v12.pdf を作成（スマホ縦・大きく表示）。"""
import os
from PIL import Image, ImageDraw, ImageFont
BASE = r"C:\Users\kanet\20260522\safe1"
CLEAN = os.path.join(BASE, "images", "cand_v12_clean")
PW, PH = 1240, 1754  # A4 portrait @150dpi
M = 50

CASES = [
 ("①","TGL 昇降板と荷台の間に頭部をはさまれ（操作起因）","事例No.38","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=38"),
 ("②","TGL テールゲートから荷が落下し下敷き","事例No.101281","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101281"),
 ("③","TGL テールゲート昇降装置で台車が倒れ激突","事例No.101534","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101534"),
 ("④","高所作業車 不安定な地盤で後方に転倒し激突","事例No.101377","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101377"),
 ("⑤","高所作業車 作業床手すりと上方構造物の間にはさまれ","事例No.101270","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101270"),
 ("⑥","高所作業車 坂道で逸走し車体と側溝にはさまれ","事例No.101412","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101412"),
]
APPROACH = ["真横(力学)","斜め後方の俯瞰","被災者ローアングル","発生直前(予兆)","発生の瞬間"]

def font(sz, bold=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc"] if bold else [r"C:\Windows\Fonts\YuGothR.ttc", r"C:\Windows\Fonts\meiryo.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()
F_T=font(46); F_H=font(40); F_M=font(28,False); F_S=font(24,False); F_U=font(20,False)

def wrap(draw, text, fnt, maxw):
    out=[]; cur=""
    for ch in text:
        if draw.textlength(cur+ch, font=fnt) <= maxw: cur+=ch
        else: out.append(cur); cur=ch
    if cur: out.append(cur)
    return out

pages=[]

def cover():
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,150],fill=(192,57,43))
    d.text((M,45),"事故イラスト・写真 候補集（v12）",font=F_T,fill="white")
    y=210
    d.text((M,y),"テールゲートリフター・高所作業車／6事例 × イラスト5・写真5（計60枚）",font=F_M,fill=(30,30,30)); y+=56
    d.text((M,y),"出典：厚生労働省 職場のあんぜんサイト 労働災害事例（全件 原典確認済）",font=F_S,fill=(90,90,90)); y+=70
    for n,t,no,url in CASES:
        d.text((M,y),f"{n} {t}",font=F_M,fill=(20,20,20)); y+=44
        d.text((M+40,y),f"{no}　{url}",font=F_U,fill=(11,102,195)); y+=58
    d.text((M,PH-80),"各事例：イラスト5枚→写真5枚。5枚は視点/タイミングを変えた候補。良い1枚を選定する用。",font=F_S,fill=(90,90,90))
    pages.append(im)

def title_page(n,t,no,url):
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,12],fill=(192,57,43))
    y=PH//2-220
    d.text((M,y),f"事例 {n}",font=font(120),fill=(192,57,43)); y+=170
    for ln in wrap(d,t,F_H,PW-2*M): d.text((M,y),ln,font=F_H,fill=(20,20,20)); y+=54
    y+=30; d.text((M,y),no,font=F_M,fill=(60,60,60)); y+=52
    for ln in wrap(d,"出典："+url,F_S,PW-2*M): d.text((M,y),ln,font=F_S,fill=(11,102,195)); y+=36
    pages.append(im)

def img_page(path, caption):
    im=Image.new("RGB",(PW,PH),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,58],fill=(35,35,35)); d.text((M,12),caption,font=F_M,fill="white")
    if os.path.exists(path):
        pic=Image.open(path).convert("RGB")
        maxw, maxh = PW-2*M, PH-160
        r=min(maxw/pic.width, maxh/pic.height); nw,nh=int(pic.width*r),int(pic.height*r)
        pic=pic.resize((nw,nh),Image.LANCZOS)
        im.paste(pic,((PW-nw)//2, 90+(maxh-nh)//2))
    else:
        d.text((M,PH//2),"(画像なし)",font=F_M,fill=(150,150,150))
    pages.append(im)

cover()
for (n,t,no,url) in CASES:
    cnum = "①②③④⑤⑥".index(n)+1
    title_page(n,t,no,url)
    for kind,label in [("illust","イラスト"),("photo","写真")]:
        for i in range(1,6):
            p=os.path.join(CLEAN,f"case{cnum}",kind,f"{i:02d}.png")
            cap=f"事例{n} {label} {i}/5 ｜ {APPROACH[i-1]}"
            img_page(p,cap)

out=os.path.join(BASE,"candidates_v12.pdf")
pages[0].save(out,save_all=True,append_images=pages[1:],resolution=150.0)
print(f"PDF saved: {out}  ({len(pages)} pages)")
