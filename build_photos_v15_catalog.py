# -*- coding: utf-8 -*-
"""photos_v15_catalog.pdf — 選定17元絵 × 4枚(実写A/B + イベントC/D) の最終カタログ。
元絵ごとに 元絵→A/B/C/D を並べ、番号・モデル名・実写/イベント版を明記。既存読むだけ・破壊なし。"""
import os, json, csv
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
OUT = os.path.join(BASE, "photos_v15_catalog.pdf")
PV15 = os.path.join(BASE, "photos_v15")
IDX = os.path.join(BASE, "collect2", "img_index.csv")

PW, PH = 1240, 1754
M = 50
RED = (192, 57, 43); INK = (25, 25, 25); GRAY = (110, 110, 110); BLUE = (11, 102, 195); GREEN = (0, 120, 60)

REFS = ["0001","0002","0003","0017","0019","0040","0041","0042","0043","0044","0046","0050","0052","0054","0057","0060","0071"]
TGL = {"0001","0002","0003","0017","0019"}
SLOTS = [("source_ref.png","元絵"),("A_openai.png","A 実写化/OpenAI"),("B_google.png","B 実写化/Google"),
         ("C_openai_event.png","C ｲﾍﾞﾝﾄ設営/OpenAI"),("D_google_event.png","D ｲﾍﾞﾝﾄ設営/Google")]


def font(sz, b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()


FT=font(40); FH=font(28); FL=font(23); FM=font(21,False); FS=font(18,False); FU=font(16,False)

# 元絵の説明を index から
DESC={}
if os.path.exists(IDX):
    with open(IDX, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            DESC[r["通し番号"]] = r.get("説明","")

pages=[]
def new_page():
    im=Image.new("RGB",(PW,PH),"white"); return im, ImageDraw.Draw(im)

def gen_count(n):
    return sum(1 for fn,_ in SLOTS[1:] if os.path.exists(os.path.join(PV15,n,fn)))

def models(n):
    p=os.path.join(PV15,n,"gen_meta.json")
    if os.path.exists(p):
        try:
            m=json.load(open(p,encoding="utf-8")); return m.get("openai_model"),m.get("google_model")
        except Exception: pass
    return None,None

def fit(d,t,f,mw):
    if d.textlength(t,font=f)<=mw: return t
    while t and d.textlength(t+"…",font=f)>mw: t=t[:-1]
    return t+"…"

done=[n for n in REFS if gen_count(n)==4]
total_imgs=sum(gen_count(n) for n in REFS)
oai_m,ggl_m=None,None
for n in REFS:
    a,b=models(n)
    oai_m=oai_m or a; ggl_m=ggl_m or b

def cover():
    im,d=new_page()
    d.rectangle([0,0,PW,140],fill=RED)
    d.text((M,30),"写真カタログ photos_v15",font=FT,fill="white")
    d.text((M,92),"選定17元絵 × 4枚（実写化A/B + イベント設営C/D・OpenAI/Google）",font=FU,fill="white")
    y=185
    d.text((M,y),f"収録: {len(done)}/17 元絵・生成画像 {total_imgs}/68 枚",font=FH,fill=GREEN); y+=52
    rows=[("使用モデル(OpenAI)",oai_m or "—"),("使用モデル(Google)",ggl_m or "—"),
          ("A/B 実写化","元絵の構図・力の向き・接触点・機種を厳守し日本の現場を写真化"),
          ("C/D イベント設営版","同一事故機序のまま文脈を展示会・イベント設営の現場へ"),
          ("生成方式","Images/参照入力→base64直保存（ブラウザDL不使用）"),
          ("共通要件","日本の現場/PPE・あごひも・(高所は)フルハーネス・実在ロゴ無し・流血無し")]
    for k,v in rows:
        d.text((M,y),"● "+k,font=FL,fill=INK)
        d.text((M+360,y),fit(d,v,FM,PW-M-(M+360)),font=FM,fill=(50,50,50)); y+=42
    y+=14
    d.text((M,y),"凡例（各元絵の並び）",font=FL,fill=INK); y+=40
    leg=["元絵：collect2/img の元絵（ヒヤリ事例）",
         "A：実写化（OpenAI gpt-image-2）",
         "B：実写化（Google gemini-3-pro-image-preview）",
         "C：イベント設営版（OpenAI）",
         "D：イベント設営版（Google）"]
    for t in leg:
        d.text((M+10,y),"・"+t,font=FM,fill=(50,50,50)); y+=34
    d.text((M,PH-60),"限定共有・noindex。元絵を参照入力に生成。実在ロゴ無し・流血無し・危険の瞬間。",font=FU,fill=GRAY)
    pages.append(im)

def ref_band(d,im,n,y):
    typ="TGL" if n in TGL else "高所"
    a,b=models(n); cnt=gen_count(n)
    d.rectangle([M,y,PW-M,y+34],fill=(238,240,244))
    d.text((M+8,y+5),f"#{n}  [{typ}]  {cnt}/4枚",font=FL,fill=INK)
    mt=f"OpenAI:{a or '-'} / Google:{b or '-'}"
    d.text((PW-M-d.textlength(mt,font=FU)-8,y+8),mt,font=FU,fill=GRAY)
    y+=40
    desc=DESC.get(n,"")
    if desc:
        d.text((M+8,y),fit(d,"機序: "+desc,FU,PW-2*M-16),font=FU,fill=(70,70,70)); y+=26
    cw=(PW-2*M-4*10)//5; ih=int(cw*0.74)
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
    per=3
    for i in range(0,len(REFS),per):
        im,d=new_page()
        d.rectangle([0,0,PW,70],fill=GREEN); d.text((M,18),"写真カタログ（元絵→A/B/C/D）",font=FH,fill="white")
        y=100
        for n in REFS[i:i+per]:
            y=ref_band(d,im,n,y)+20
        d.text((M,PH-40),"photos_v15_catalog",font=FU,fill=GRAY)
        pages.append(im)

cover()
gallery()
pages[0].save(OUT,"PDF",save_all=True,append_images=pages[1:],resolution=150.0)
print("WROTE",OUT,"pages=",len(pages),"refs=",len(REFS),"done=",len(done),"imgs=",total_imgs)
