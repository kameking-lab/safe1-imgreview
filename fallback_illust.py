# -*- coding: utf-8 -*-
"""
fallback_illust.py
Geminiイラストが失敗/破綻した場合の保険となる、PIL製の線画スキマ図。
テンプレ準拠: 白背景・黒い細線・作業者は黒シルエット・文字なし。
ラベル/赤矢印/黄三角は pptx 側で重ねる(ここでは描かない)。
出力: images/fallback/genNN.png (1280x900)
"""
import os, math
from PIL import Image, ImageDraw

OUT = r"C:\Users\kanet\20260522\safe1\images\fallback"
os.makedirs(OUT, exist_ok=True)
W, H = 1280, 900
BLK = (17, 17, 17)
GRY = (110, 110, 110)
LW = 5

def newimg():
    im = Image.new("RGB", (W, H), "white")
    return im, ImageDraw.Draw(im)

def line(d, pts, w=LW, fill=BLK):
    d.line(pts, fill=fill, width=w, joint="curve")

def rect(d, box, w=LW, fill=None, outline=BLK):
    d.rectangle(box, outline=outline, width=w, fill=fill)

def poly(d, pts, w=LW, fill=None, outline=BLK):
    d.polygon(pts, fill=fill, outline=outline)
    if outline and w > 1:
        d.line(pts + [pts[0]], fill=outline, width=w, joint="curve")

def circle(d, cx, cy, r, w=LW, fill=None, outline=BLK):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=outline, width=w, fill=fill)

def worker(d, cx, cy, h=170, pose="stand", flip=False):
    """黒シルエットの作業者。cy=足元基準。h=全高。"""
    s = h/170.0
    def P(dx, dy):
        x = cx + (-dx if flip else dx)*s
        return (x, cy + dy*s)
    head_r = 16*s
    if pose == "stand":
        # 胴
        poly(d, [P(-13,-150),P(13,-150),P(11,-70),P(-11,-70)], w=1, fill=BLK, outline=BLK)
        # 脚
        poly(d, [P(-11,-72),P(-1,-72),P(-3,0),P(-13,0)], w=1, fill=BLK, outline=BLK)
        poly(d, [P(1,-72),P(11,-72),P(13,0),P(3,0)], w=1, fill=BLK, outline=BLK)
        # 腕
        poly(d, [P(-12,-145),P(-2,-145),P(-16,-95),P(-24,-98)], w=1, fill=BLK, outline=BLK)
        poly(d, [P(12,-145),P(2,-145),P(24,-98),P(16,-95)], w=1, fill=BLK, outline=BLK)
        circle(d, *P(0,-166), head_r, w=1, fill=BLK, outline=BLK)
    elif pose == "fall":
        # 頭から落下(水平気味)。胴を斜めに。
        cx2, cy2 = cx, cy
        ang = -35 if not flip else -145
        def R(dx,dy):
            a=math.radians(ang)
            return (cx2+(dx*math.cos(a)-dy*math.sin(a))*s, cy2+(dx*math.sin(a)+dy*math.cos(a))*s)
        poly(d, [R(-13,0),R(13,0),R(11,80),R(-11,80)], w=1, fill=BLK, outline=BLK)
        poly(d, [R(-11,78),R(-1,78),R(-3,150),R(-13,150)], w=1, fill=BLK, outline=BLK)
        poly(d, [R(1,78),R(11,78),R(13,150),R(3,150)], w=1, fill=BLK, outline=BLK)
        poly(d, [R(-12,8),R(-2,8),R(-30,40),R(-38,34)], w=1, fill=BLK, outline=BLK)
        poly(d, [R(12,8),R(2,8),R(30,40),R(22,46)], w=1, fill=BLK, outline=BLK)
        circle(d, *R(0,-18), head_r, w=1, fill=BLK, outline=BLK)
    elif pose == "crouch":
        poly(d, [P(-14,-95),P(12,-95),P(16,-45),P(-12,-45)], w=1, fill=BLK, outline=BLK)
        poly(d, [P(-12,-47),P(14,-47),P(26,-10),P(16,0),P(4,-8)], w=1, fill=BLK, outline=BLK)
        poly(d, [P(-14,-90),P(-6,-92),P(-30,-60),P(-38,-66)], w=1, fill=BLK, outline=BLK)
        circle(d, *P(-2,-110), head_r, w=1, fill=BLK, outline=BLK)
    elif pose == "lean":
        # 手すり越しに前傾
        poly(d, [P(-10,-150),P(14,-140),P(30,-80),P(8,-78)], w=1, fill=BLK, outline=BLK)
        poly(d, [P(-10,-80),P(0,-80),P(-2,0),P(-12,0)], w=1, fill=BLK, outline=BLK)
        poly(d, [P(2,-80),P(12,-80),P(16,0),P(6,0)], w=1, fill=BLK, outline=BLK)
        poly(d, [P(12,-142),P(22,-138),P(52,-110),P(46,-100)], w=1, fill=BLK, outline=BLK)
        circle(d, *P(26,-150), head_r, w=1, fill=BLK, outline=BLK)
    return

# ---- 共通パーツ ----
def truck_with_tailgate(d, platform_y, plat_x0, plat_x1, plat_tilt=0, bed_h=120, cab=True):
    """トラック後部＋テールゲート昇降板。platform_y=昇降板の高さ(画面y)。"""
    # 荷台ボディ(後部)
    bed_top = platform_y - bed_h
    body_x0 = plat_x1 + 10
    body_x1 = body_x0 + 360
    rect(d, [body_x0, bed_top-150, body_x1, platform_y+0], w=LW)
    # 荷台床ライン
    line(d, [(body_x0, platform_y), (body_x1, platform_y)], w=LW)
    # 車輪
    circle(d, body_x0+90, platform_y+55, 48, w=LW)
    circle(d, body_x0+90, platform_y+55, 20, w=LW)
    circle(d, body_x1-70, platform_y+55, 48, w=LW)
    circle(d, body_x1-70, platform_y+55, 20, w=LW)
    if cab:
        # 運転席(簡易)
        rect(d, [body_x1, bed_top-40, body_x1+120, platform_y], w=LW)
        line(d, [(body_x1+10, bed_top-40),(body_x1+10, bed_top+30),(body_x1+120, bed_top+30)], w=LW)
    # 昇降板(プラットフォーム)
    ty0 = platform_y + plat_tilt
    ty1 = platform_y - plat_tilt
    poly(d, [(plat_x0, ty0-8),(plat_x1, ty1-8),(plat_x1, ty1+8),(plat_x0, ty0+8)], w=LW, fill=(235,235,235))
    # アーム(荷台と昇降板を結ぶ)
    line(d, [(plat_x1, ty1),(body_x0, platform_y-30)], w=LW)
    # 地面
    line(d, [(40, platform_y+103),(W-40, platform_y+103)], w=LW, fill=GRY)

def ground(d, y):
    line(d, [(40, y),(W-40, y)], w=LW, fill=GRY)

def aerial_lift(d, base_x, ground_y, boom_angle=55, boom_len=360, tilt=0, basket_dx=0, basket_dy=0):
    """ブーム式高所作業車。戻り値: バケット中心(bx,by)。"""
    # 車体
    bx0, bx1 = base_x-150, base_x+150
    by1 = ground_y
    by0 = ground_y-90
    # tilt(転倒)考慮の簡易回転中心
    cx, cy = base_x, ground_y
    a = math.radians(tilt)
    def T(x,y):
        dx,dy = x-cx, y-cy
        return (cx+dx*math.cos(a)-dy*math.sin(a), cy+dx*math.sin(a)+dy*math.cos(a))
    poly(d, [T(bx0,by0),T(bx1,by0),T(bx1,by1),T(bx0,by1)], w=LW, fill=(238,238,238))
    # 車輪
    for wx in (bx0+55, bx1-55):
        c=T(wx,by1+18); circle(d, c[0], c[1], 34, w=LW)
    # 旋回台
    poly(d, [T(base_x-55,by0),T(base_x+55,by0),T(base_x+45,by0-45),T(base_x-45,by0-45)], w=LW, fill=(238,238,238))
    # ブーム
    ba = math.radians(boom_angle)
    p0 = T(base_x, by0-40)
    p1 = T(base_x + boom_len*math.cos(ba), by0-40 - boom_len*math.sin(ba))
    line(d, [p0, p1], w=10)
    # バケット
    bw, bh = 120, 90
    bx, by = p1[0]+basket_dx, p1[1]+basket_dy
    rect(d, [bx-bw/2, by-bh, bx+bw/2, by], w=LW, fill=(245,245,245))
    # 手すり上辺強調
    line(d, [(bx-bw/2, by-bh),(bx+bw/2, by-bh)], w=LW)
    return bx, by-bh, bw, bh

# ============ 各シーン ============
def scene1():  # 昇降板端部・後退踏み外し墜落＋ドラム缶
    im,d = newimg()
    py = 560
    truck_with_tailgate(d, py, 360, 720, plat_tilt=0)
    # ドラム缶(積荷)
    dx=560
    d.ellipse([dx-55, py-150, dx+55, py-118], outline=BLK, width=LW)
    rect(d, [dx-55, py-134, dx+55, py-26], w=LW)
    d.ellipse([dx-55, py-42, dx+55, py-10], outline=BLK, width=LW)
    line(d,[(dx-55,py-100),(dx+55,py-100)],w=3)
    line(d,[(dx-55,py-66),(dx+55,py-66)],w=3)
    # 端部で後退して落下する作業者(昇降板後端の左外側)
    worker(d, 300, py+95, h=150, pose="fall", flip=False)
    im.save(os.path.join(OUT,"gen01.png")); im.close()

def scene2():  # 昇降中・足はさまれ
    im,d = newimg()
    py = 470  # 昇降板が半分の高さ
    # 荷台床は上に
    bedy = py-150
    truck_with_tailgate(d, py, 360, 720, plat_tilt=0, bed_h=120)
    ground(d, 720)
    # 昇降板と荷台のすき間を強調(隙間の縦線)
    line(d, [(720, py-8),(740, py-8)], w=LW)
    # 作業者が側方に立ち、足がすき間に
    worker(d, 600, py-8, h=160, pose="stand")
    im.save(os.path.join(OUT,"gen02.png")); im.close()

def scene3():  # カゴ車が昇降板上で転倒・下敷き
    im,d = newimg()
    py = 560
    truck_with_tailgate(d, py, 340, 720, plat_tilt=26)  # 傾斜
    # カゴ車(ロールボックス)を傾けて転倒
    cgx, cgy = 470, py-10
    ang = 22
    a=math.radians(ang)
    def R(x,y):
        return (cgx+(x)*math.cos(a)-(y)*math.sin(a), cgy+(x)*math.sin(a)+(y)*math.cos(a))
    poly(d, [R(-70,-200),R(70,-200),R(70,0),R(-70,0)], w=LW, fill=(240,240,240))
    # メッシュ
    for yy in range(-170,-10,40):
        line(d,[R(-70,yy),R(70,yy)],w=2)
    for xx in range(-45,70,40):
        line(d,[R(xx,-200),R(xx,0)],w=2)
    # キャスター
    circle(d, *R(-55,12), 12, w=3); circle(d, *R(55,12), 12, w=3)
    # 下敷きになる作業者
    worker(d, 300, py+95, h=150, pose="crouch", flip=True)
    im.save(os.path.join(OUT,"gen03.png")); im.close()

def scene4():  # バケット身を乗り出し墜落・安全帯未掛け
    im,d = newimg()
    gy = 800
    bx,by,bw,bh = aerial_lift(d, 360, gy, boom_angle=58, boom_len=420, basket_dx=0, basket_dy=0)
    # 身を乗り出す作業者(手すり越し前傾)
    worker(d, bx+bw*0.32, by+bh*0.0, h=120, pose="lean")
    # ぶら下がる未接続ランヤード(フック未掛け)
    line(d, [(bx-bw*0.3, by+10),(bx-bw*0.3-10, by+70),(bx-bw*0.3+6, by+120)], w=3)
    im.save(os.path.join(OUT,"gen04.png")); im.close()

def scene5():  # 走行・旋回中の転倒(不整地・アウトリガー未設置)
    im,d = newimg()
    gy = 760
    # 傾斜地
    line(d, [(60, gy-30),(W-60, gy+70)], w=LW, fill=GRY)
    bx,by,bw,bh = aerial_lift(d, 470, gy+10, boom_angle=62, boom_len=360, tilt=20)
    worker(d, bx, by+bh*0.1, h=110, pose="stand")
    im.save(os.path.join(OUT,"gen05.png")); im.close()

def scene6():  # バケットと上方構造物のはさまれ
    im,d = newimg()
    gy = 820
    bx,by,bw,bh = aerial_lift(d, 380, gy, boom_angle=62, boom_len=470)
    # 上方の梁/トラス
    beam_y = by - 18
    rect(d, [120, beam_y-34, W-120, beam_y], w=LW, fill=(235,235,235))
    for xx in range(160, W-120, 120):
        line(d, [(xx, beam_y),(xx+60, beam_y-34)], w=2)
    # バケット内で頭上にはさまれる作業者
    worker(d, bx, by, h=78, pose="stand")
    im.save(os.path.join(OUT,"gen06.png")); im.close()

for fn in (scene1,scene2,scene3,scene4,scene5,scene6):
    fn()
print("fallback illustrations written to", OUT)
