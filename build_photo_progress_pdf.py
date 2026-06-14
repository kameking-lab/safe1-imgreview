# -*- coding: utf-8 -*-
"""photo_progress PDF — 写真生成の進捗＋生成画像プレビュー。既存読むだけ・破壊なし。"""
import os, sys, json, csv
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
STAMP = sys.argv[1] if len(sys.argv) > 1 else "20260614_2236"
NOW = sys.argv[2] if len(sys.argv) > 2 else "2026-06-14 22:36 JST"
OUT = os.path.join(BASE, f"photo_progress_{STAMP}.pdf")
PV15 = os.path.join(BASE, "photos_v15")

PW, PH = 1240, 1754
M = 50
RED = (192, 57, 43); INK = (25, 25, 25); GRAY = (110, 110, 110); BLUE = (11, 102, 195); GREEN = (0, 120, 60)

REFS = ["0001","0002","0003","0017","0019","0040","0041","0042","0043","0044","0046","0050","0052","0054","0057","0060","0071"]
TGL = {"0001","0002","0003","0017","0019"}
SLOTS = [("source_ref.png","元絵"),("A_openai.png","A 実写/OpenAI"),("B_google.png","B 実写/Google"),
         ("C_openai_event.png","C ｲﾍﾞﾝﾄ/OpenAI"),("D_google_event.png","D ｲﾍﾞﾝﾄ/Google")]


def font(sz, b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()


FT=font(40); FH=font(28); FL=font(23); FM=font(21,False); FS=font(18,False); FU=font(16,False)
pages=[]
def new_page():
    im=Image.new("RGB",(PW,PH),"white"); return im, ImageDraw.Draw(im)
def wrap(d,t,f,mw):
    o,c=[],""
    for ch in t:
        if d.textlength(c+ch,font=f)<=mw: c+=ch
        else: o.append(c); c=ch
    if c: o.append(c)
    return o

def gen_count(n):
    return sum(1 for fn,_ in SLOTS[1:] if os.path.exists(os.path.join(PV15,n,fn)))
def models(n):
    p=os.path.join(PV15,n,"gen_meta.json")
    if os.path.exists(p):
        try:
            m=json.load(open(p,encoding="utf-8")); return m.get("openai_model"),m.get("google_model")
        except Exception: pass
    return None,None

done=[n for n in REFS if gen_count(n)==4]
partial=[n for n in REFS if 0<gen_count(n)<4]
total_imgs=sum(gen_count(n) for n in REFS)
oai_m,ggl_m=None,None
for n in REFS:
    a,b=models(n)
    oai_m=oai_m or a; ggl_m=ggl_m or b

def cover():
    im,d=new_page()
    d.rectangle([0,0,PW,140],fill=RED)
    d.text((M,32),"写真生成 進捗レポート（画像プレビュー付）",font=FT,fill="white")
    d.text((M,92),"選定17元絵 × 4枚（実写A/B＋イベントC/D・OpenAI/Google）",font=FU,fill="white")
    y=185
    d.text((M,y),f"現在時刻: {NOW}",font=FH,fill=INK); y+=52
    pct=round(len(done)/17*100)
    d.text((M,y),f"完了: {len(done)}/17 元絵（{pct}%）・生成画像 {total_imgs}/68 枚",font=FH,fill=GREEN); y+=48
    d.text((M,y),f"着手中: {partial[0] if partial else 'なし'}（{gen_count(partial[0]) if partial else 0}/4枚）",font=FM,fill=INK); y+=46
    bw=PW-2*M
    d.rectangle([M,y,M+bw,y+34],outline=(180,180,180)); d.rectangle([M,y,M+int(bw*len(done)/17),y+34],fill=GREEN)
    d.text((M+10,y+5),f"{pct}%",font=FL,fill="white"); y+=70
    rows=[("使用モデル(OpenAI)",oai_m or "—"),("使用モデル(Google)",ggl_m or "—"),
          ("生成方式","Images/参照入力→base64直保存（ブラウザDL不使用）"),
          ("自己点検","構図/機種/PPE/AI破綻/ロゴ/自然さ、破綻のみ再生成"),
          ("ランナー","稼働中（無人継続）")]
    for k,v in rows:
        d.text((M,y),"● "+k,font=FL,fill=INK); d.text((M+340,y),v,font=FM,fill=(50,50,50)); y+=40
    y+=10
    d.text((M,y),"※以降のページに 元絵→A/B/C/D の生成画像を掲載（完成分）。",font=FS,fill=GRAY)
    d.text((M,PH-60),"限定共有・noindex。画像は collect2/img の元絵を参照入力に生成。実在ロゴ無し・流血無し。",font=FU,fill=GRAY)
    pages.append(im)

def ref_band(d,im,n,y):
    typ="TGL" if n in TGL else "高所"
    a,b=models(n); cnt=gen_count(n)
    tag="完成" if cnt==4 else f"生成中 {cnt}/4"
    d.rectangle([M,y,PW-M,y+34],fill=(238,240,244))
    d.text((M+8,y+5),f"#{n}  [{typ}]  {tag}",font=FL,fill=INK)
    mt=f"OpenAI:{a or '-'} / Google:{b or '-'}"
    d.text((PW-M-d.textlength(mt,font=FU)-8,y+8),mt,font=FU,fill=GRAY)
    y+=42
    cw=(PW-2*M-4*10)//5; ih=int(cw*0.72)
    x=M
    for fn,label in SLOTS:
        p=os.path.join(PV15,n,fn)
        d.rectangle([x,y,x+cw,y+ih],fill=(245,245,245),outline=(210,210,210))
        if os.path.exists(p):
            try:
                pic=Image.open(p).convert("RGB"); iw,ih0=pic.size
                s=min((cw-6)/iw,(ih-6)/ih0); nw,nh=max(1,int(iw*s)),max(1,int(ih0*s))
                im.paste(pic.resize((nw,nh),Image.LANCZOS),(x+(cw-nw)//2,y+(ih-nh)//2))
            except Exception:
                d.text((x+6,y+ih//2),"読込不可",font=FS,fill=RED)
        else:
            d.text((x+6,y+ih//2-8),"未生成",font=FS,fill=GRAY)
        d.text((x+2,y+ih+4),label,font=FU,fill=INK)
        x+=cw+10
    return y+ih+34

def gallery():
    shown=done+partial
    per=3
    for i in range(0,len(shown),per):
        im,d=new_page()
        d.rectangle([0,0,PW,70],fill=GREEN); d.text((M,18),"生成画像プレビュー（元絵→A/B/C/D）",font=FH,fill="white")
        y=100
        for n in shown[i:i+per]:
            y=ref_band(d,im,n,y)+18
        d.text((M,PH-40),f"写真生成 進捗 {NOW}",font=FU,fill=GRAY)
        pages.append(im)

cover()
if done or partial: gallery()
pages[0].save(OUT,"PDF",save_all=True,append_images=pages[1:],resolution=150.0)
print("WROTE",OUT,"pages=",len(pages),"done=",len(done),"partial=",len(partial),"imgs=",total_imgs)
