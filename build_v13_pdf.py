# -*- coding: utf-8 -*-
"""candidates_v13photo.pdf : 事例ごとに[タイトル+出典URL+参照見本]→生成写真3枚を大判。"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
BASE=r"C:\Users\kanet\20260522\safe1"; CLEAN=os.path.join(BASE,"images","v13photo_clean"); REFS=os.path.join(BASE,"refs","anzen")
PW,PH=1240,1754; M=55
CASES=[
 ("①","TGL 昇降板と荷台の間に頭部をはさまれ（操作起因）","事例No.38","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=38"),
 ("②","TGL テールゲートから荷が落下し下敷き（過積載＋傾斜）","事例No.101281","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101281"),
 ("③","TGL テールゲート昇降装置で台車が倒れ激突","事例No.101534","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101534"),
 ("④","高所作業車 不安定な地盤で後方に転倒し激突","事例No.101377","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101377"),
 ("⑤","高所作業車 作業床手すりと上方構造物の間にはさまれ","事例No.101270","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101270"),
 ("⑥","高所作業車 坂道で逸走し車体と側溝にはさまれ","事例No.101412","https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=101412"),
]
APPROACH=["真横/標準","斜め後方/曇天光","ローアングル/広角"]
def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(42); FH=font(32); FM=font(26,False); FS=font(22,False); FU=font(20,False)
pages=[]
def wrap(d,t,f,mw):
    o=[];c=""
    for ch in t:
        if d.textlength(c+ch,font=f)<=mw:c+=ch
        else:o.append(c);c=ch
    if c:o.append(c)
    return o
def cover():
    im=Image.new("RGB",(PW,PH),"white");d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,140],fill=(192,57,43)); d.text((M,40),"参照写真 候補集（v13・見本準拠）",font=FT,fill="white")
    y=190
    d.text((M,y),"公式事故図(厚労省あんぜんサイト)を“構図・向き・接触点の見本”として参照し、",font=FM,fill=(30,30,30));y+=42
    d.text((M,y),"その構図を崩さずに写実写真化（AIに因果を発明させない狙い）。6事例×3枚＝18枚。",font=FM,fill=(30,30,30));y+=64
    for n,t,no,url in CASES:
        d.text((M,y),f"{n} {t}",font=FM,fill=(20,20,20));y+=42
        d.text((M+36,y),f"{no}　{url}",font=FU,fill=(11,102,195));y+=54
    d.text((M,PH-70),"各事例：参照見本(公式図)→生成写真3枚。最終採用は人間が選定。",font=FS,fill=(110,110,110))
    pages.append(im)
def case_head(n,t,no,url,refpath):
    im=Image.new("RGB",(PW,PH),"white");d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,12],fill=(192,57,43))
    y=70; d.text((M,y),f"事例 {n}",font=font(90),fill=(192,57,43));y+=130
    for ln in wrap(d,t,FH,PW-2*M): d.text((M,y),ln,font=FH,fill=(20,20,20));y+=46
    y+=8; d.text((M,y),no,font=FM,fill=(60,60,60));y+=46
    for ln in wrap(d,"出典(原典)："+url,FS,PW-2*M): d.text((M,y),ln,font=FS,fill=(11,102,195));y+=34
    y+=20; d.text((M,y),"▼ 参照した公式事故図（構図・向き・接触点の見本）",font=FM,fill=(40,40,40));y+=44
    if refpath and os.path.exists(refpath):
        r=Image.open(refpath).convert("RGB"); mw=PW-2*M; mh=PH-y-60
        rr=min(mw/r.width,mh/r.height); r=r.resize((int(r.width*rr),int(r.height*rr)),Image.LANCZOS)
        im.paste(r,(M,y)); d.rectangle([M,y,M+r.width,y+r.height],outline=(150,150,150),width=2)
    pages.append(im)
def photo_page(p,cap):
    im=Image.new("RGB",(PW,PH),"white");d=ImageDraw.Draw(im)
    d.rectangle([0,0,PW,58],fill=(35,35,35)); d.text((M,12),cap,font=FM,fill="white")
    if os.path.exists(p):
        pic=Image.open(p).convert("RGB"); mw,mh=PW-2*M,PH-150
        r=min(mw/pic.width,mh/pic.height); pic=pic.resize((int(pic.width*r),int(pic.height*r)),Image.LANCZOS)
        im.paste(pic,((PW-pic.width)//2,90+(mh-pic.height)//2))
    pages.append(im)
cover()
for (n,t,no,url) in CASES:
    cn="①②③④⑤⑥".index(n)+1
    rs=glob.glob(os.path.join(REFS,f"case{cn}_*"))
    case_head(n,t,no,url, rs[0] if rs else None)
    for i in range(1,4):
        p=os.path.join(CLEAN,f"case{cn}",f"0{i}.png")
        photo_page(p, f"事例{n} 写真 {i}/3 ｜ {APPROACH[i-1]}")
out=os.path.join(BASE,"candidates_v13photo.pdf")
pages[0].save(out,save_all=True,append_images=pages[1:],resolution=150.0)
print(f"saved {out} ({len(pages)} pages)")
