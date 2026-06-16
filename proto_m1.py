# -*- coding: utf-8 -*-
"""M1: 純・模式図（コード作画）。事例②=過積載+傾斜→後傾→機械滑落→下敷き。
向き/接触点/危険点/要因を作者が完全制御。出力: images/proto/m1_scene.png, m1_chain.png"""
import os, math
from PIL import Image, ImageDraw, ImageFont
OUT = r"C:\Users\kanet\20260522\safe1\images\proto"; os.makedirs(OUT, exist_ok=True)
BLK=(25,25,25); RED=(214,40,40); YEL=(255,214,0); GRY=(120,120,120); BLU=(40,90,160)
STEEL=(205,212,220); DK=(70,80,95); SKIN=(60,60,60)

def font(sz,bold=True):
    for p in ([r"C:\Windows\Fonts\YuGothB.ttc",r"C:\Windows\Fonts\meiryob.ttc"] if bold else [r"C:\Windows\Fonts\YuGothR.ttc",r"C:\Windows\Fonts\meiryo.ttc"]):
        if os.path.exists(p):
            try: return ImageFont.truetype(p,sz)
            except: pass
    return ImageFont.load_default()
FT=font(40); FH=font(30); FL=font(24,False); FS=font(20,False); FB=font(26)

def arrow(d,x1,y1,x2,y2,col=RED,w=9,head=26):
    d.line([(x1,y1),(x2,y2)],fill=col,width=w)
    ang=math.atan2(y2-y1,x2-x1)
    for s in (0.4,-0.4):
        d.line([(x2,y2),(x2-head*math.cos(ang-s),y2-head*math.sin(ang-s))],fill=col,width=w)

def tri(d,cx,cy,r=30):
    pts=[(cx,cy-r),(cx-r*0.92,cy+r*0.7),(cx+r*0.92,cy+r*0.7)]
    d.polygon(pts,fill=YEL,outline=BLK); d.line(pts+[pts[0]],fill=BLK,width=3)
    d.text((cx-5,cy-14),"!",font=FB,fill=BLK)

def label(d,x,y,text,lx=None,ly=None,col=BLK,box=(255,255,255)):
    w=d.textlength(text,font=FL)+16
    d.rounded_rectangle([x,y,x+w,y+38],8,fill=box,outline=GRY,width=2)
    d.text((x+8,y+6),text,font=FL,fill=col)
    if lx is not None: d.line([(x,y+19),(lx,ly)],fill=GRY,width=2)

def worker(d,cx,gy,h=120,lean=20,flip=False):
    """簡潔な作業者(横向き・後方へ押される)。gy=足元。lean=後傾角(右下へ)."""
    s=h/120.0; a=math.radians(lean*(1 if not flip else -1))
    def R(x,y):
        return (cx+(x*math.cos(a)-y*math.sin(a))*s,(gy)+(x*math.sin(a)+y*math.cos(a))*s)
    # 脚(踏ん張り)
    d.line([R(-2,0),R(-18,-46)],fill=DK,width=int(13*s)); d.line([R(10,0),R(2,-50)],fill=DK,width=int(13*s))
    # 胴
    d.line([R(-6,-48),R(-2,-92)],fill=BLU,width=int(20*s))
    # 腕(頭を守る)
    d.line([R(-3,-86),R(18,-104)],fill=BLU,width=int(11*s)); d.line([R(18,-104),R(30,-86)],fill=BLU,width=int(11*s))
    # 反射ベスト線
    d.line([R(-6,-58),R(-2,-84)],fill=YEL,width=int(5*s))
    # 頭+ヘルメット
    hx,hy=R(0,-104); d.ellipse([hx-13*s,hy-13*s,hx+13*s,hy+13*s],fill=SKIN)
    d.pieslice([hx-15*s,hy-17*s,hx+15*s,hy+9*s],180,360,fill=(240,240,240),outline=BLK)
    d.line([R(-15,-104),R(15,-104)],fill=BLK,width=2)

def platform(d,x0,y0,x1,y1,th=12):
    d.line([(x0,y0),(x1,y1)],fill=BLK,width=th)  # 上面
    d.polygon([(x0,y0),(x1,y1),(x1,y1+th),(x0,y0+th)],fill=STEEL,outline=BLK)

def machine(d,cx,cy,w,h,rot=0,label_overload=False):
    a=math.radians(rot)
    def R(x,y): return (cx+x*math.cos(a)-y*math.sin(a), cy+x*math.sin(a)+y*math.cos(a))
    body=[R(-w/2,-h),R(w/2,-h),R(w/2,0),R(-w/2,0)]
    d.polygon(body,fill=(150,160,175),outline=BLK); d.line(body+[body[0]],fill=BLK,width=4)
    # 車輪(低い台座)
    for wx in (-w/2+18,w/2-18):
        c=R(wx,8); d.ellipse([c[0]-9,c[1]-9,c[0]+9,c[1]+9],fill=DK,outline=BLK)
    # 重心マーク
    g=R(0,-h*0.62); d.ellipse([g[0]-6,g[1]-6,g[0]+6,g[1]+6],fill=BLK)
    d.line([g,(g[0],g[1]+40)],fill=BLK,width=2)

def truck(d,cabx,beery,scale=1.0,tilt=0):
    """簡易トラック(横向き・キャブ左)。beery=荷台床の右端y."""
    # 荷台
    bx0,bx1=cabx+170,cabx+620
    d.line([(bx0,beery-150),(bx1,beery-150+tilt)],fill=BLK,width=3)
    d.polygon([(bx0,beery-150),(bx1,beery-150+tilt),(bx1,beery+tilt),(bx0,beery)],fill=(245,245,245),outline=BLK)
    # キャブ
    d.polygon([(cabx,beery-120),(cabx+150,beery-120),(cabx+150,beery),(cabx,beery)],fill=(235,235,235),outline=BLK)
    d.rectangle([cabx+12,beery-110,cabx+90,beery-60],outline=BLK,width=2)
    # 車輪
    for wx in (cabx+70,bx0+90,bx1-70):
        d.ellipse([wx-30,beery+tilt-6,wx+30,beery+tilt+54],fill=DK,outline=BLK)
        d.ellipse([wx-12,beery+tilt+16,wx+12,beery+tilt+40],fill=(180,180,180))
    return bx1  # 荷台後端x

def ground_slope(d,x0,y0,x1,y1):
    d.line([(x0,y0),(x1,y1)],fill=GRY,width=5)
    for x in range(int(x0),int(x1),46):
        t=(x-x0)/(x1-x0); y=y0+(y1-y0)*t
        d.line([(x,y),(x-12,y+16)],fill=GRY,width=2)

# ===== 単一シーン図 =====
def scene():
    W,H=1480,940; im=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,70],fill=RED); d.text((30,14),"② 荷の落下・下敷き ｜ 過積載＋傾斜地での後傾 → 機械が滑落",font=FT,fill="white")
    # 地面(入口へ下る傾斜：右へ下る)
    ground_slope(d,70,560,1410,650)
    label_small(d,95,672,"入口へ下る傾斜（修正治具なし）")
    # トラック(後方=右が沈む tilt)
    rear=truck(d,150,540,tilt=26)
    # テールゲート昇降板(後端=右、下げて傾斜)
    px0,py0=rear+6,470; px1,py1=rear+250,560
    platform(d,px0,py0,px1,py1)
    # 機械(過積載・重心高い)を昇降板上で右へ後傾(滑落しかけ)
    machine(d,(px0+px1)//2+40,py0-10,150,150,rot=24)
    # 作業者(後端右の地上で、右下へ押されて下敷き)
    worker(d,px1+165,712,h=150,lean=26)
    # 赤矢印：機械の滑落・荷重の向き(右下へ＝人と同方向)。危険点で止める
    arrow(d,(px0+px1)//2+95,py0-150,px1+80,600,col=RED,w=11,head=30)
    # 黄！：はさまれ/激突の危険点(機械下端と人の接触)
    tri(d,px1+95,636,r=34)
    # 要因ラベル
    label(d,px0-40,300,"過積載 1.2t ＞ 定格1.0t（重心が高い）",lx=(px0+px1)//2+10,ly=py0-90)
    label(d,150,250,"後方が沈み後傾（修正治具なし）",lx=rear-40,ly=420,col=BLK)
    label(d,px1+30,760,"下敷き（はさまれ・激突）",lx=px1+90,ly=665,col=RED)
    # 注記
    d.text((30,H-46),"赤矢印＝荷重/滑落の向き（人と同方向）｜黄！＝危険点｜出典: 厚労省 あんぜんサイト No.101281",font=FS,fill=GRY)
    im.save(os.path.join(OUT,"m1_scene.png")); print("m1_scene saved")

# ===== 因果連鎖図(4コマ) =====
def chain():
    W,H=1480,560; im=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,64],fill=(40,40,40)); d.text((30,12),"因果の連鎖：① 過積載 → ② 傾斜で後傾 → ③ 滑落 → ④ 下敷き",font=FH,fill="white")
    titles=["① 過積載（定格超過）","② 傾斜で後傾","③ 機械が滑落","④ 下敷き・激突"]
    pw=350; x0=20; y0=110
    for i,t in enumerate(titles):
        x=x0+i*(pw+10)
        d.rounded_rectangle([x,y0,x+pw,y0+370],10,outline=GRY,width=2)
        d.text((x+12,y0+8),t,font=FL,fill=BLK)
        cx=x+pw//2; gy=y0+330
        if i==0:
            d.line([(x+30,gy),(x+pw-30,gy)],fill=GRY,width=4)  # 平ら
            platform(d,x+60,gy-70,x+pw-60,gy-70)
            machine(d,cx,gy-72,90,90,rot=0)
            label_small(d,x+40,y0+300,"重心が高い")
        elif i==1:
            d.line([(x+30,gy-30),(x+pw-30,gy+30)],fill=GRY,width=4)  # 右下がり
            platform(d,x+60,gy-90,x+pw-60,gy-50)
            machine(d,cx,gy-78,90,90,rot=14)
            arrow(d,cx+10,gy-150,cx+45,gy-90,col=RED,w=7,head=18)
        elif i==2:
            d.line([(x+30,gy-30),(x+pw-30,gy+30)],fill=GRY,width=4)
            platform(d,x+60,gy-90,x+pw-60,gy-50)
            machine(d,cx+40,gy-50,90,90,rot=40)
            arrow(d,cx,gy-120,x+pw-50,gy+5,col=RED,w=8,head=22)
        else:
            d.line([(x+30,gy+10),(x+pw-30,gy+10)],fill=GRY,width=4)
            machine(d,cx-10,gy-20,90,90,rot=70)
            worker(d,cx+70,gy+8,h=95,lean=30)
            tri(d,cx+35,gy-20,r=26)
        if i<3: arrow(d,x+pw-6,y0+185,x+pw+8,y0+185,col=(40,40,40),w=6,head=16)
    im.save(os.path.join(OUT,"m1_chain.png")); print("m1_chain saved")

def label_small(d,x,y,text):
    w=d.textlength(text,font=FS)+12
    d.rounded_rectangle([x,y,x+w,y+28],6,fill="white",outline=GRY,width=1); d.text((x+6,y+4),text,font=FS,fill=BLK)

scene(); chain()
print("M1 DONE")
