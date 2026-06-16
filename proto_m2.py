# -*- coding: utf-8 -*-
"""M2: AIパーツ合成。A(トラック+昇降板)・B(機械)・C(作業者)を白キー切抜き→座標制御で配置し、
荷の倒れる向きと人の倒れる向き・接触点を一致させる。赤矢印/黄!/要因ラベルをコードで上乗せ。
出力: images/proto/m2_composite.png"""
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P=r"C:\Users\kanet\20260522\safe1\images\proto\parts"; OUT=r"C:\Users\kanet\20260522\safe1\images\proto"
BLK=(25,25,25); RED=(214,40,40); YEL=(255,214,0); GRY=(120,120,120)
def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(40); FL=font(24,False); FB=font(26); FS=font(20,False)

def white_key(img, thr=240, feather=1.2):
    im=img.convert("RGB"); a=np.asarray(im).astype(int)
    white=(a[:,:,0]>thr)&(a[:,:,1]>thr)&(a[:,:,2]>thr)
    alpha=np.where(white,0,255).astype(np.uint8)
    rgba=np.dstack([np.asarray(im),alpha])
    out=Image.fromarray(rgba,"RGBA")
    if feather:
        al=out.split()[3].filter(ImageFilter.GaussianBlur(feather)); out.putalpha(al)
    return out

def load(name, fallbackbox=False):
    p=os.path.join(P,name)
    if os.path.exists(p) and os.path.getsize(p)>3000:
        return Image.open(p).convert("RGB")
    return None

def scale_to_w(im,w):
    r=w/im.width; return im.resize((w,int(im.height*r)),Image.LANCZOS)
def scale_to_h(im,h):
    r=h/im.height; return im.resize((int(im.width*r),h),Image.LANCZOS)

def arrow(d,x1,y1,x2,y2,col=RED,w=11,head=30):
    d.line([(x1,y1),(x2,y2)],fill=col,width=w); ang=math.atan2(y2-y1,x2-x1)
    for s in (0.4,-0.4): d.line([(x2,y2),(x2-head*math.cos(ang-s),y2-head*math.sin(ang-s))],fill=col,width=w)
def tri(d,cx,cy,r=34):
    pts=[(cx,cy-r),(cx-r*0.92,cy+r*0.7),(cx+r*0.92,cy+r*0.7)]; d.polygon(pts,fill=YEL,outline=BLK); d.line(pts+[pts[0]],fill=BLK,width=3); d.text((cx-6,cy-15),"!",font=FB,fill=BLK)
def label(d,x,y,text,lx=None,ly=None,col=BLK):
    w=d.textlength(text,font=FL)+16; d.rounded_rectangle([x,y,x+w,y+38],8,fill="white",outline=GRY,width=2); d.text((x+8,y+6),text,font=FL,fill=col)
    if lx is not None: d.line([(x,y+19),(lx,ly)],fill=GRY,width=2)

W,H=1480,940
canvas=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(canvas)
d.rectangle([0,0,W,70],fill=RED); d.text((30,14),"② 荷の落下・下敷き ｜ パーツ合成（AI素材を座標制御で配置）",font=FT,fill="white")
# 傾斜地(右へ下る)
d.line([(70,560),(1410,650)],fill=GRY,width=5)
for x in range(70,1410,46):
    t=(x-70)/1340; y=560+90*t; d.line([(x,y),(x-12,y+16)],fill=GRY,width=2)
# A: トラック(右上アイコンを白塗りしてから白キー)
A=load("A.png")
if A is not None:
    A=A.copy(); ad=ImageDraw.Draw(A); ad.rectangle([A.width-90,0,A.width,60],fill="white")  # UIアイコン消し
    A=white_key(A); A=scale_to_w(A,760); canvas.paste(A,(60,300),A)
    plat_x=60+760-40; plat_y=300+A.height-70   # 昇降板付近(右下)
else:
    plat_x,plat_y=820,520
# B: 機械(右へ後傾＝滑落)。無ければコード箱
B=load("B.png")
if B is not None:
    B=white_key(B); B=scale_to_h(B,165); B=B.rotate(-24,expand=True,resample=Image.BICUBIC)
    canvas.paste(B,(plat_x-20,plat_y-185),B); bx,by=plat_x+B.width//2-20,plat_y-40
    used_B="AI"
else:
    a=math.radians(24); cx,cy=plat_x+70,plat_y-70
    def R(x,y): return (cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a))
    body=[R(-70,-140),R(70,-140),R(70,0),R(-70,0)]; d.polygon(body,fill=(150,160,175),outline=BLK); d.line(body+[body[0]],fill=BLK,width=4)
    bx,by=cx+30,cy-20; used_B="code"
# C: 作業者(右の地上・左向き=機械側を向く・押される)
C=load("C.png")
if C is not None:
    C=white_key(C); C=scale_to_h(C,210); canvas.paste(C,(plat_x+150,plat_y+10-C.height+150),C)
    wx,wy=plat_x+150+C.width//2,plat_y+150
else:
    wx,wy=plat_x+250,plat_y+120
d=ImageDraw.Draw(canvas)
# 赤矢印：機械の滑落・荷重(右下=人と同方向)
arrow(d,plat_x+60,plat_y-150,plat_x+150,plat_y+70,col=RED,w=12,head=32)
# 黄!：接触=危険点
tri(d,plat_x+160,plat_y+95,r=34)
# 要因ラベル
label(d,plat_x-120,170,"過積載 1.2t ＞ 定格1.0t（重心が高い）",lx=plat_x+30,ly=plat_y-120)
label(d,120,230,"入口へ下る傾斜→後方が沈み後傾",lx=400,ly=470)
label(d,plat_x+60,plat_y+170,"下敷き（はさまれ・激突）",lx=plat_x+160,ly=plat_y+120,col=RED)
mat = "AI(トラック/機械/作業者)" if used_B=="AI" else "AI(トラック/作業者)＋機械はコード"
d.text((30,H-44),"赤矢印＝荷重/滑落の向き（人と同方向）｜黄！＝危険点｜素材:"+mat+"、配置/向き/矢印:コード｜出典 No.101281",font=FS,fill=GRY)
canvas.save(os.path.join(OUT,"m2_composite.png")); print(f"m2 saved (machine={used_B})")
