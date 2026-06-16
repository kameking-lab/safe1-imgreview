# -*- coding: utf-8 -*-
"""M3: ハイブリッド。AIの“事故でない”素の素材(トラックA)を背景に置き、
人・荷・赤矢印・危険点・要因ラベルはコードで制御して上乗せ。向きはコードが担保。
出力: images/proto/m3_hybrid.png"""
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P=r"C:\Users\kanet\20260522\safe1\images\proto\parts"; OUT=r"C:\Users\kanet\20260522\safe1\images\proto"
BLK=(25,25,25); RED=(214,40,40); YEL=(255,214,0); GRY=(120,120,120); BLU=(40,90,160); DK=(70,80,95); SKIN=(60,60,60)
def font(sz,b=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if b else [r"C:\Windows\Fonts\YuGothR.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(40); FL=font(24,False); FB=font(26); FS=font(20,False)
def white_key(img,thr=240,f=1.2):
    a=np.asarray(img.convert("RGB")).astype(int); white=(a[:,:,0]>thr)&(a[:,:,1]>thr)&(a[:,:,2]>thr)
    out=Image.fromarray(np.dstack([np.asarray(img.convert("RGB")),np.where(white,0,255).astype(np.uint8)]),"RGBA")
    out.putalpha(out.split()[3].filter(ImageFilter.GaussianBlur(f))); return out
def arrow(d,x1,y1,x2,y2,col=RED,w=12,head=32):
    d.line([(x1,y1),(x2,y2)],fill=col,width=w); ang=math.atan2(y2-y1,x2-x1)
    for s in (0.4,-0.4): d.line([(x2,y2),(x2-head*math.cos(ang-s),y2-head*math.sin(ang-s))],fill=col,width=w)
def tri(d,cx,cy,r=34):
    pts=[(cx,cy-r),(cx-r*0.92,cy+r*0.7),(cx+r*0.92,cy+r*0.7)]; d.polygon(pts,fill=YEL,outline=BLK); d.line(pts+[pts[0]],fill=BLK,width=3); d.text((cx-6,cy-15),"!",font=FB,fill=BLK)
def label(d,x,y,t,lx=None,ly=None,col=BLK):
    w=d.textlength(t,font=FL)+16; d.rounded_rectangle([x,y,x+w,y+38],8,fill="white",outline=GRY,width=2); d.text((x+8,y+6),t,font=FL,fill=col)
    if lx is not None: d.line([(x,y+19),(lx,ly)],fill=GRY,width=2)
def machine(d,cx,cy,w,h,rot):
    a=math.radians(rot)
    def R(x,y): return (cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a))
    body=[R(-w/2,-h),R(w/2,-h),R(w/2,0),R(-w/2,0)]; d.polygon(body,fill=(150,160,175),outline=BLK); d.line(body+[body[0]],fill=BLK,width=4)
    for wx in (-w/2+18,w/2-18):
        c=R(wx,8); d.ellipse([c[0]-9,c[1]-9,c[0]+9,c[1]+9],fill=DK,outline=BLK)
    g=R(0,-h*0.62); d.ellipse([g[0]-6,g[1]-6,g[0]+6,g[1]+6],fill=BLK); d.line([g,(g[0],g[1]+38)],fill=BLK,width=2)
def worker(d,cx,gy,h=150,lean=26):
    s=h/120.0; a=math.radians(lean)
    def R(x,y): return (cx+(x*math.cos(a)-y*math.sin(a))*s,gy+(x*math.sin(a)+y*math.cos(a))*s)
    d.line([R(-2,0),R(-18,-46)],fill=DK,width=int(13*s)); d.line([R(10,0),R(2,-50)],fill=DK,width=int(13*s))
    d.line([R(-6,-48),R(-2,-92)],fill=BLU,width=int(20*s))
    d.line([R(-3,-86),R(18,-104)],fill=BLU,width=int(11*s)); d.line([R(18,-104),R(30,-86)],fill=BLU,width=int(11*s))
    d.line([R(-6,-58),R(-2,-84)],fill=YEL,width=int(5*s))
    hx,hy=R(0,-104); d.ellipse([hx-13*s,hy-13*s,hx+13*s,hy+13*s],fill=SKIN)
    d.pieslice([hx-15*s,hy-17*s,hx+15*s,hy+9*s],180,360,fill=(240,240,240),outline=BLK); d.line([R(-15,-104),R(15,-104)],fill=BLK,width=2)

W,H=1480,940
cv=Image.new("RGB",(W,H),(247,249,251)); d=ImageDraw.Draw(cv)
d.rectangle([0,0,W,70],fill=RED); d.text((30,14),"② 荷の落下・下敷き ｜ ハイブリッド（AI背景＋コードで人・荷・矢印）",font=FT,fill="white")
# 傾斜地
d.line([(70,560),(1410,650)],fill=GRY,width=6)
for x in range(70,1410,46):
    t=(x-70)/1340; y=560+90*t; d.line([(x,y),(x-12,y+16)],fill=GRY,width=2)
# AI背景：素のトラック(人も荷もない)。右上アイコン白塗り→白キー
A=Image.open(os.path.join(P,"A.png")).convert("RGB"); ad=ImageDraw.Draw(A); ad.rectangle([A.width-90,0,A.width,60],fill="white")
Ak=white_key(A); r=720/Ak.width; Ak=Ak.resize((720,int(Ak.height*r)),Image.LANCZOS)
cv.paste(Ak,(70,300),Ak)
plat_x=70+720-30; plat_y=300+Ak.height-78
d=ImageDraw.Draw(cv)
# コード：荷(機械)を昇降板上で右へ後傾→滑落
machine(d,plat_x+30,plat_y-8,150,150,rot=24)
# コード：作業者(右の地上・受け)
worker(d,plat_x+175,plat_y+150,h=150,lean=26)
# 赤矢印(右下＝人と同方向)
arrow(d,plat_x+70,plat_y-150,plat_x+150,plat_y+60,col=RED,w=12,head=32)
tri(d,plat_x+160,plat_y+86,r=34)
label(d,plat_x-150,180,"過積載 1.2t ＞ 定格1.0t（重心が高い）",lx=plat_x+10,ly=plat_y-120)
label(d,120,235,"入口へ下る傾斜→後方が沈み後傾",lx=420,ly=470)
label(d,plat_x+60,plat_y+175,"下敷き（はさまれ・激突）",lx=plat_x+160,ly=plat_y+115,col=RED)
d.text((30,H-44),"赤矢印＝荷重/滑落の向き（人と同方向）｜黄！＝危険点｜背景:AI(素のトラック)、人/荷/矢印/向き:コード｜出典 No.101281",font=FS,fill=GRY)
cv.save(os.path.join(OUT,"m3_hybrid.png")); print("m3 saved")
