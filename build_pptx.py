# -*- coding: utf-8 -*-
"""
build_pptx.py  —  (株)博展向け テールゲートリフター・高所作業車 重大事故事例集
テンプレ実測値に忠実に再現。游ゴシック / 16:9 / 博展フッター(ドット列+HAKUTENロゴ)。
出力: hakuten_jirei_v{N}.pptx (引数 N、既定は自動採番)
"""
import sys, os, json
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from copy import deepcopy
from PIL import Image

BASE = r"C:\Users\kanet\20260522\safe1"
GEN = os.path.join(BASE, "images", "gen")
FB  = os.path.join(BASE, "images", "fallback")
REF = os.path.join(BASE, "images", "ref")

# 版ごとに main() が設定（画像ディレクトリ・画像比・オーバーレイ座標）
IMGDIR = GEN
IMG_RATIO = 1.49          # 概要スライドの画像ボックス比（横/縦）= Gemini出力 1024x687 に一致
ACTIVE_OVR = None
FITDIR = os.path.join(BASE, "images", "_fit"); os.makedirs(FITDIR, exist_ok=True)

# ---- 配色 ----
BLACK = RGBColor(0x00,0x00,0x00)
RED   = RGBColor(0xFF,0x00,0x00)
YELLOW= RGBColor(0xFF,0xFF,0x00)
GRAYL = RGBColor(0xD9,0xD9,0xD9)   # 表ラベル列
FOOT  = RGBColor(0x5E,0x5E,0x5E)   # フッター文字
WHITE = RGBColor(0xFF,0xFF,0xFF)
DARK  = RGBColor(0x22,0x22,0x22)
REDDK = RGBColor(0xC0,0x00,0x00)

JP = "游ゴシック"
JPM = "游ゴシック Medium"
EMU_IN = 914400
SW, SH = Inches(13.333), Inches(7.5)

def set_font(run, name=JP, size=14, bold=False, color=BLACK):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    # 日本語として認識させ、禁則処理(句読点・閉じ括弧の行頭禁止等)を有効化
    rPr.set("lang", "ja-JP")
    rPr.set("altLang", "en-US")
    for tag in ("a:latin","a:ea","a:cs"):
        e = rPr.find(qn(tag))
        if e is None:
            e = rPr.makeelement(qn(tag), {}); rPr.append(e)
        e.set("typeface", name)

def add_text(slide, l, t, w, h, lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             fill=None, line_color=None, line_w=None, wrap=True):
    """lines: list of dict {runs:[(text,opts)], space_after, align, line_spacing}"""
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(4); tf.margin_right = Pt(4)
    tf.margin_top = Pt(2); tf.margin_bottom = Pt(2)
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = ln.get("align", align)
        if ln.get("space_after") is not None: p.space_after = Pt(ln["space_after"])
        if ln.get("space_before") is not None: p.space_before = Pt(ln["space_before"])
        if ln.get("line_spacing"): p.line_spacing = ln["line_spacing"]
        for (txt, opts) in ln["runs"]:
            r = p.add_run(); r.text = txt
            set_font(r, **opts)
    if fill is not None:
        tb.fill.solid(); tb.fill.fore_color.rgb = fill
    else:
        tb.fill.background()
    if line_color is not None:
        tb.line.color.rgb = line_color; tb.line.width = Pt(line_w or 0.75)
    else:
        tb.line.fill.background()
    return tb

def add_footer(slide, page_no):
    # 左下 copyright
    add_text(slide, Inches(0.33), Inches(7.06), Inches(5.5), Inches(0.34),
             [{"runs":[("©Hakuten Corporation All Rights Reserved.",
                        dict(name=JP,size=9,color=FOOT))]}], anchor=MSO_ANCHOR.MIDDLE)
    # 右下 ドット列+ロゴ画像
    strip = os.path.join(REF, "footer_strip_raw.png")
    if os.path.exists(strip):
        w = Inches(3.15); h = Inches(3.15*52/520)
        slide.shapes.add_picture(strip, Inches(8.95), Inches(7.04), width=w, height=h)
    # 右端 ページ番号
    add_text(slide, Inches(12.55), Inches(7.02), Inches(0.55), Inches(0.34),
             [{"runs":[(str(page_no), dict(name=JP,size=10,color=FOOT))]}],
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def blank_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    return s

def title_block(slide, text, sub=None):
    add_text(slide, Inches(0.5), Inches(0.30), Inches(12.3), Inches(0.95),
             [{"runs":[(text, dict(name=JP,size=27,bold=True,color=BLACK))],"line_spacing":1.0}])
    if sub:
        add_text(slide, Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.4),
                 [{"runs":[(sub, dict(name=JP,size=12.5,color=FOOT))]}])

def add_arrow(slide, x1,y1,x2,y2, color=RED, width=3.2):
    cn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1,y1,x2,y2)
    cn.line.color.rgb = color; cn.line.width = Pt(width)
    ln = cn.line._get_or_add_ln()
    tail = ln.makeelement(qn("a:tailEnd"), {"type":"triangle","w":"lg","len":"lg"})
    ln.append(tail)
    return cn

def add_triangle(slide, x, y, size, mark="!"):
    sh = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, x, y, size, size)
    sh.fill.solid(); sh.fill.fore_color.rgb = YELLOW
    sh.line.color.rgb = BLACK; sh.line.width = Pt(1.5)
    sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap=False
    p = tf.paragraphs[0]; p.alignment=PP_ALIGN.CENTER
    r=p.add_run(); r.text=mark; set_font(r, name=JP, size=13, bold=True, color=BLACK)
    tf.margin_top=Pt(6); tf.margin_bottom=Pt(0)
    return sh

def add_label(slide, x, y, text, w=None, size=10.5, color=BLACK, bold=False):
    w = w or Inches(0.24+0.172*len(text))
    add_text(slide, x, y, w, Inches(0.32), [{"runs":[(text, dict(name=JP,size=size,bold=bold,color=color))]}],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=WHITE, line_color=RGBColor(0x99,0x99,0x99), line_w=0.75, wrap=False)

def pick_illust(n):
    g = os.path.join(IMGDIR, f"gen{n:02d}.png")
    f = os.path.join(FB, f"gen{n:02d}.png")
    if os.path.exists(g) and os.path.getsize(g) > 6000:
        return g
    return f

def fit_cover(src, ratio):
    """画像を指定比(横/縦)に中央クロップ(cover)してFITDIRに保存しパスを返す。歪み無し。"""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    cur = w / h
    if abs(cur - ratio) < 0.003:
        return src
    if cur > ratio:  # 横長すぎ→左右を削る
        nw = int(round(h * ratio)); x = (w - nw) // 2
        im = im.crop((x, 0, x + nw, h))
    else:            # 縦長すぎ→上下を削る（やや上寄りに残す＝頭を切らない）
        nh = int(round(w / ratio)); y = int((h - nh) * 0.40)
        im = im.crop((0, y, w, y + nh))
    base = os.path.splitext(os.path.basename(src))[0]
    outp = os.path.join(FITDIR, f"{os.path.basename(os.path.dirname(src))}_{base}_{ratio:.3f}.png")
    im.save(outp)
    return outp

# ============ コンテンツ定義 ============
TODAY = "2026年6月13日"

CASES = [
 dict(no="①", grp="TGL", short="昇降板端部からの墜落・転落",
   title="重大事故概要　① テールゲートリフター 昇降板からの墜落",
   hazard="縁・柵のない昇降板の端で後退し、足を踏み外して地面へ墜落（人の墜落）。",
   result="想定される結果：死亡・重篤",
   reveal="—（JNIOSH 公表分析事例／2011〜2012年）",
   proj="運輸業（貨物自動車運送）／TGL昇降板上での荷の取卸し作業",
   event="後ろ向きで作業していた作業者が、縁・柵のない昇降板の後端を踏み外し、頭部から地面へ墜落して被災した。",
   cause="後ろ向き姿勢で足元の視界・確認が不十分／昇降板に縁（柵）がなく踏み外しを防げない構造／端部での不安定な作業姿勢。",
   resp="—",
   meas=["昇降板上は前向き作業とし、端部・縁に立たない（中央寄りで作業）",
         "安全柵付きTGLの採用、端部の表示・滑り止めを徹底",
         "墜落制止用器具（フルハーネス）等で端部作業の墜落を防止"],
   src="JNIOSH 公表事例（報告 houkoku_2018_01／コラム No.118）",
   site="設営搬入でブース資材を降ろす際、昇降板の端に立たず前向き・中央で扱う。"),
 dict(no="②", grp="TGL", short="昇降中の足のはさまれ",
   title="重大事故概要　② テールゲートリフター 昇降中のはさまれ",
   hazard="人が乗ったまま昇降板を動かし、足が荷台・地面との隙間に挟まれる。",
   result="想定される結果：骨折・重篤",
   reveal="—（JNIOSH 分析／あんぜんサイト ヒヤリ・ハット hiy_0448）",
   proj="一般貨物自動車運送業／TGL昇降板の昇降操作中の荷役作業",
   event="昇降板に乗って移動した際、足が荷台と昇降板の間に挟まれた。TGL災害の約2割が昇降動作中に発生している。",
   cause="人が乗ったまま昇降板を動かす不適正使用／昇降板と荷台・地面の隙間に身体が入る位置取り／はさまれ危険の認識不足。",
   resp="—",
   meas=["昇降板の昇降中は人を乗せない・隙間付近に手足を置かない",
         "TGLは「荷専用」と認識し、人の昇降に使わない",
         "動作中の立ち位置ルールと相互の声掛けを徹底"],
   src="JNIOSH コラム No.118 ／ あんぜんサイト hiy_0448",
   site="撤去時、作業者は昇降板に乗って降りない。荷だけを載せ、操作者は地上から行う。"),
 dict(no="③", grp="TGL", short="カゴ車の転倒・下敷き",
   title="重大事故概要　③ テールゲートリフター カゴ車の転倒・下敷き",
   hazard="段差・傾斜・固定不良でカゴ車が昇降板上で転倒し、作業者が下敷きに。",
   result="想定される結果：下敷き・重篤",
   reveal="—（あんぜんサイト 労働災害事例 No.55）",
   proj="陸上貨物運送業／トラック荷台からロールボックスパレット（カゴ車）を取卸す作業",
   event="荷台と昇降板・渡り板の段差や傾斜でカゴ車がバランスを崩して転倒し、作業者が下敷き・激突した。",
   cause="渡り板の急勾配・段差／カゴ車のキャスターロック等の固定不良／単独作業・危険認識不足。",
   resp="—",
   meas=["カゴ車のキャスターストッパーと昇降板上での固定を確実に行う",
         "段差・傾斜を解消し、平坦な状態で移動させる",
         "重量カゴ車は複数人で扱い、転倒側に立たない"],
   src="あんぜんサイト 労働災害事例 No.55",
   site="1t台車・カゴ台車での資材搬出入は、ロック確認・段差解消・転倒側に立たないを徹底。"),
 dict(no="④", grp="AWP", short="バケットからの墜落",
   title="重大事故概要　④ 高所作業車 バケットからの墜落",
   hazard="手すりから身を乗り出し、安全帯（フック）未使用でバケットから墜落。",
   result="想定される結果：死亡・重篤",
   reveal="—（あんぜんサイト 労働災害事例 No.549）",
   proj="建設業／高所作業車のバケットで柱間に部材を取付ける高所作業",
   event="バケット内で身を乗り出した不安定姿勢で作業中、墜落・はさまれにより被災した。",
   cause="手すり越し・身を乗り出しの不安定姿勢／墜落制止用器具（安全帯）の確実な使用・フック掛けの不徹底／作業計画の不備。",
   resp="—",
   meas=["手すりから身を乗り出さず、作業対象にバケットを正対・接近させる",
         "墜落制止用器具をバケット内の堅固な設備に常時フック掛け",
         "作業計画書を作成・周知し、安全な作業半径を確保"],
   src="あんぜんサイト 労働災害事例 No.549（安全帯論点 No.507）",
   site="高所のトラス・サイン取付けはバケットを対象へ寄せ、フルハーネスを常時フック掛け。"),
 dict(no="⑤", grp="AWP", short="走行・旋回中の車両転倒",
   title="重大事故概要　⑤ 高所作業車 走行・旋回中の転倒",
   hazard="傾斜・不整地・アウトリガー未設置で車両ごと転倒、搭乗者が激突。",
   result="想定される結果：死亡",
   reveal="—（あんぜんサイト 労働災害事例 No.101377）",
   proj="建設業／最大作業高さ約12mの高所作業車を用いた約10m高所での作業",
   event="作業中に高所作業車が後方へ転倒し、バケット搭乗者が地面に激突。転倒前に警告音（予兆）があったが作業を継続していた。",
   cause="傾斜・軟弱地盤など設置場所の不適切／アウトリガー未設置／転倒のおそれがある状況での作業継続。",
   resp="—",
   meas=["平坦・堅固な地盤に設置し、アウトリガーを確実に張り出す",
         "異常音・傾き等の予兆があれば直ちに作業を中止する",
         "事前に作業計画を策定し、設置面の状態を点検する"],
   src="あんぜんサイト 労働災害事例 No.101377（被災程度：死亡）",
   site="屋外イベント・搬入路の不整地や養生段差では、設置面を点検しアウトリガーを必ず展開。"),
 dict(no="⑥", grp="AWP", short="上方構造物とのはさまれ",
   title="重大事故概要　⑥ 高所作業車 上方構造物とのはさまれ",
   hazard="旋回・操作中にバケットと梁・天井トラス等の間に挟まれる。",
   result="想定される結果：はさまれ・重篤",
   reveal="—（あんぜんサイト 労働災害事例 No.401）",
   proj="化学工場等／地上約6mのパイプラックを高所作業車のバケットで配管・塗装する作業",
   event="ブームを縮めながら旋回させた際、バケットと構造物（パイプラック）の間に挟まれた。",
   cause="バケットと構造物との離隔確保不足／旋回・操作時の安全確認不足／合図・連携不足。",
   resp="—",
   meas=["旋回・移動前に上方・側方構造物との離隔を確認し、構造物際で旋回させない",
         "操作は資格者が行い、合図・誘導者を配置して連携する",
         "作業計画書で動線と離隔距離を定め、関係者へ周知する"],
   src="あんぜんサイト 労働災害事例 No.401（類似 No.507／No.606）",
   site="天井トラス・リギング・電線下でのバケット操作は誘導者を付け、旋回前に頭上クリアランス確認。"),
]

# 概要スライドのオーバーレイ（画像ボックス内の正規化座標 0-1）— Geminiイラスト(1024x559)レイアウトに合わせ調整
OVR = {
 1:{"arrow":(0.80,0.26,0.90,0.55),"tri":(0.70,0.60),
    "labels":[(0.44,0.10,"積荷（ドラム缶）"),(0.58,0.74,"縁・柵なし")]},
 2:{"arrow":(0.60,0.50,0.625,0.80),"tri":(0.50,0.74),
    "labels":[(0.16,0.80,"昇降板と地面のすき間に足")]},
 3:{"arrow":(0.60,0.34,0.78,0.58),"tri":(0.49,0.50),
    "labels":[(0.42,0.04,"カゴ車（ロールボックス）"),(0.20,0.60,"段差・傾斜")]},
 4:{"arrow":(0.80,0.20,0.90,0.44),"tri":(0.64,0.16),
    "labels":[(0.46,0.02,"手すりから身を乗り出し"),(0.78,0.42,"安全帯フック未掛け")]},
 5:{"arrow":(0.30,0.66,0.17,0.82),"tri":(0.32,0.78),
    "labels":[(0.16,0.88,"アウトリガー未設置／傾斜地")]},
 6:{"arrow":(0.58,0.36,0.58,0.20),"tri":(0.62,0.15),
    "labels":[(0.10,0.04,"天井トラス・梁"),(0.66,0.30,"頭上クリアランス不足")]},
}

# v5 イラスト版オーバーレイ（images/illust_v5 の構図に合わせ調整）
OVR_ILLUST = {
 1:{"arrow":(0.72,0.34,0.85,0.60),"tri":(0.60,0.56),
    "labels":[(0.28,0.12,"積荷（ドラム缶）"),(0.44,0.80,"縁・柵なし")]},
 2:{"arrow":(0.54,0.40,0.40,0.58),"tri":(0.33,0.62),
    "labels":[(0.24,0.84,"昇降板のすき間に足")]},
 3:{"arrow":(0.50,0.40,0.66,0.55),"tri":(0.40,0.66),
    "labels":[(0.14,0.08,"カゴ車（ロールボックス）"),(0.28,0.80,"段差・傾斜")]},
 4:{"arrow":(0.70,0.30,0.84,0.52),"tri":(0.60,0.34),
    "labels":[(0.30,0.05,"手すりから身を乗り出し"),(0.26,0.82,"安全帯フック未掛け")]},
 5:{"arrow":(0.50,0.46,0.68,0.60),"tri":(0.40,0.74),
    "labels":[(0.26,0.88,"アウトリガー未設置／不整地")]},
 6:{"arrow":(0.50,0.40,0.50,0.22),"tri":(0.58,0.16),
    "labels":[(0.10,0.06,"天井トラス・梁"),(0.60,0.30,"頭上クリアランス不足")]},
}
# v10 イラスト版オーバーレイ（images/illust_v10 構図に精密調整）
OVR_ILLUST_V10 = {
 1:{"arrow":(0.46,0.40,0.30,0.62),"tri":(0.29,0.58),
    "labels":[(0.40,0.07,"後退で踏み外し"),(0.12,0.74,"縁・柵なし")]},
 2:{"arrow":(0.56,0.50,0.45,0.62),"tri":(0.40,0.62),
    "labels":[(0.18,0.80,"昇降板のすき間に足")]},
 3:{"arrow":(0.50,0.34,0.68,0.55),"tri":(0.55,0.58),
    "labels":[(0.24,0.06,"カゴ車（ロールボックス）"),(0.12,0.62,"段差・固定不良")]},
 4:{"arrow":(0.45,0.45,0.30,0.68),"tri":(0.43,0.40),
    "labels":[(0.33,0.05,"手すりから身を乗り出し"),(0.48,0.80,"フック未掛け")]},
 5:{"arrow":(0.45,0.45,0.60,0.65),"tri":(0.31,0.74),
    "labels":[(0.18,0.88,"アウトリガー未設置／不整地")]},
 6:{"arrow":(0.75,0.45,0.75,0.28),"tri":(0.83,0.24),
    "labels":[(0.16,0.07,"天井トラス・梁"),(0.42,0.40,"頭上クリアランス不足")]},
}
# v10 写真版オーバーレイ（images/photo_v10 構図に精密調整）
OVR_PHOTO_V10 = {
 1:{"arrow":(0.46,0.42,0.30,0.62),"tri":(0.27,0.55),
    "labels":[(0.38,0.07,"後退で踏み外し"),(0.10,0.72,"縁・柵なし")]},
 2:{"arrow":(0.56,0.50,0.44,0.68),"tri":(0.39,0.70),
    "labels":[(0.16,0.82,"昇降板のすき間に足")]},
 3:{"arrow":(0.52,0.36,0.68,0.52),"tri":(0.55,0.58),
    "labels":[(0.24,0.06,"カゴ車（ロールボックス）"),(0.16,0.66,"段差・固定不良")]},
 4:{"arrow":(0.38,0.38,0.22,0.58),"tri":(0.49,0.42),
    "labels":[(0.33,0.05,"手すりから身を乗り出し"),(0.52,0.80,"フック未掛け")]},
 5:{"arrow":(0.45,0.40,0.62,0.62),"tri":(0.34,0.72),
    "labels":[(0.18,0.88,"アウトリガー未設置／不整地")]},
 6:{"arrow":(0.50,0.48,0.50,0.28),"tri":(0.60,0.24),
    "labels":[(0.14,0.09,"天井トラス・梁"),(0.56,0.36,"頭上クリアランス不足")]},
}

# v5 写真版オーバーレイ（images/photo_v5 の構図に合わせ調整）
OVR_PHOTO = {
 1:{"arrow":(0.50,0.34,0.63,0.58),"tri":(0.46,0.60),
    "labels":[(0.58,0.14,"積荷（ドラム缶）"),(0.38,0.80,"縁・柵なし")]},
 2:{"arrow":(0.58,0.50,0.46,0.66),"tri":(0.41,0.68),
    "labels":[(0.22,0.84,"昇降板のすき間に足")]},
 3:{"arrow":(0.52,0.40,0.66,0.55),"tri":(0.42,0.62),
    "labels":[(0.12,0.08,"カゴ車（ロールボックス）"),(0.28,0.82,"段差・傾斜")]},
 4:{"arrow":(0.40,0.34,0.22,0.58),"tri":(0.50,0.44),
    "labels":[(0.36,0.05,"手すりから身を乗り出し"),(0.58,0.80,"安全帯フック未掛け")]},
 5:{"arrow":(0.40,0.34,0.55,0.55),"tri":(0.33,0.66),
    "labels":[(0.18,0.88,"アウトリガー未設置／不整地")]},
 6:{"arrow":(0.50,0.42,0.50,0.24),"tri":(0.59,0.17),
    "labels":[(0.10,0.06,"天井トラス・梁"),(0.60,0.30,"頭上クリアランス不足")]},
}

CHECK_TGL = [
 "TGL操作の特別教育を修了しているか（2024年2月〜義務化）",
 "昇降板の端・縁に立たず、中央・前向きで作業しているか",
 "昇降板の昇降中は人を乗せない／すき間に手足を入れていないか",
 "カゴ車・台車はキャスターロックで固定し、段差・傾斜を解消したか",
 "重量物は複数人で扱い、転倒側に立たず低重心で積載しているか",
]
CHECK_AWP = [
 "設置面は平坦・堅固か、アウトリガーを確実に張り出したか",
 "フルハーネス型墜落制止用器具を堅固な設備に常時フック掛けしたか",
 "手すりから身を乗り出していないか／作業対象にバケットを寄せたか",
 "旋回・移動前に上方（トラス・電線）と側方の離隔を確認し誘導者を置いたか",
 "異常音・傾き等の予兆で直ちに作業中止し、作業計画書を周知しているか",
]

# ============ スライド生成 ============
def main():
    global IMGDIR, ACTIVE_OVR
    # 使い方: py build_pptx.py <出力タグ> [画像セット名]
    #   例: py build_pptx.py illust_v5 illust_v5  → hakuten_jirei_illust_v5.pptx / images/illust_v5
    ver = sys.argv[1] if len(sys.argv) > 1 else None
    imgkind = sys.argv[2] if len(sys.argv) > 2 else None
    if ver is None:
        n = 1
        while os.path.exists(os.path.join(BASE, f"hakuten_jirei_v{n}.pptx")): n += 1
        ver = str(n)
    if imgkind:
        IMGDIR = os.path.join(BASE, "images", imgkind)
        key = imgkind.replace("_clean", "")
        reg = {"illust_v10": OVR_ILLUST_V10, "photo_v10": OVR_PHOTO_V10}
        ACTIVE_OVR = reg.get(key, OVR_PHOTO if "photo" in key else OVR_ILLUST)
    out = os.path.join(BASE, f"hakuten_jirei_{ver}.pptx")

    prs = Presentation()
    prs.slide_width = SW; prs.slide_height = SH
    page = 0
    def newpage():
        nonlocal page; page += 1; return page

    # ---- 1. 表紙 ----
    s = blank_slide(prs)
    add_text(s, Inches(0.9), Inches(2.05), Inches(11.5), Inches(2.0),
      [{"runs":[("テールゲートリフター・高所作業車", dict(name=JP,size=36,bold=True,color=BLACK))],"space_after":6},
       {"runs":[("重大事故事例集", dict(name=JP,size=44,bold=True,color=BLACK))]}], align=PP_ALIGN.LEFT)
    # 赤いアクセントは新規装飾を足さない方針 → テキストのみ
    add_text(s, Inches(0.95), Inches(4.05), Inches(11.0), Inches(0.5),
      [{"runs":[("設営・搬入・撤去・会場高所作業の現場で起きる重大災害と対策", dict(name=JP,size=15,color=DARK))]}])
    add_text(s, Inches(0.95), Inches(5.15), Inches(7.0), Inches(0.5),
      [{"runs":[("株式会社 博展　御中", dict(name=JP,size=17,bold=True,color=BLACK))]}])
    add_text(s, Inches(0.95), Inches(5.75), Inches(7.0), Inches(0.4),
      [{"runs":[("作成日：" + TODAY, dict(name=JP,size=12,color=FOOT))]}])
    add_text(s, Inches(0.95), Inches(6.18), Inches(10.5), Inches(0.4),
      [{"runs":[("監修：労働安全コンサルタント（土木）　金田 義太（登録第4840号）", dict(name=JP,size=10.5,color=FOOT))]}])
    add_footer(s, newpage())

    # ---- 2. 統計サマリー① TGL ----
    s = blank_slide(prs)
    title_block(s, "統計で見る　テールゲートリフター（TGL）災害", "出典：JNIOSH／厚生労働省 職場のあんぜんサイト")
    big_stats(s, [
      ("558〜632", "件／年", "TGL起因の労働災害（推計・休業4日以上）", RED),
      ("42.3", "%", "作業者が昇降板上で転倒・転落して死傷", BLACK),
      ("運輸業", "中心", "TGL災害が多い業種（設営の荷役も同じリスク）", BLACK),
    ], top=1.85, val_sizes=[44,62,44])
    # 法改正カラム
    add_text(s, Inches(0.6), Inches(4.35), Inches(12.1), Inches(2.1),
      [{"runs":[("【法改正】2024年（令和6年）2月1日 施行　", dict(name=JP,size=16,bold=True,color=REDDK)),
                ("テールゲートリフターで荷を積み卸す作業に「特別教育」が義務化", dict(name=JP,size=16,bold=True,color=BLACK))],"space_after":7},
       {"runs":[("　根拠：労働安全衛生法 第59条第3項／労働安全衛生規則 第36条の改正（第五号の四）。教育は学科4時間＋実技2時間（計6時間）。", dict(name=JP,size=12.5,color=DARK))],"space_after":5},
       {"runs":[("　設営搬入・撤去でTGLを用いて資材を積み卸す作業も対象。未修了者の従事は法令違反となる。", dict(name=JP,size=12.5,color=DARK))]}],
      fill=RGBColor(0xF5,0xF5,0xF5), line_color=GRAYL, line_w=1.0)
    add_footer(s, newpage())

    # ---- 3. 統計サマリー② 高所作業車 ----
    s = blank_slide(prs)
    title_block(s, "統計で見る　高所作業車 災害", "出典：建荷協（建設荷役車両安全技術協会）／厚生労働省")
    big_stats(s, [
      ("6", "名", "高所作業車を起因物とする死亡者数（令和2年）", RED),
      ("墜落・転落", "が最多", "次いで はさまれ → 転倒 → 激突され", BLACK),
      ("700", "人", "令和7年 労働災害死亡者（全産業・過去最少／2026.5.27公表）", BLACK),
    ], top=1.85, val_sizes=[60,30,60])
    add_text(s, Inches(0.6), Inches(4.35), Inches(12.1), Inches(2.1),
      [{"runs":[("【傾向】", dict(name=JP,size=15,bold=True,color=REDDK)),
                ("死亡6名の内訳は建設業5名・運輸交通業1名。事故の型は「墜落・転落」が最多。業種は建設業中心だが、製造業・ビルメンテ・樹木剪定・イベント設営等でも発生。", dict(name=JP,size=13,color=BLACK))],"space_after":7},
       {"runs":[("　会場設営の高所作業（トラス・サイン・照明の取付け／撤去）も同じ災害リスクを負う。", dict(name=JP,size=12.5,color=DARK))],"space_after":5},
       {"runs":[("　※高所作業車「単独」の年間死傷者総数を示す公的確定統計は数表として未公表（本資料では「未確認」と表記）。", dict(name=JP,size=11,color=FOOT))]}],
      fill=RGBColor(0xF5,0xF5,0xF5), line_color=GRAYL, line_w=1.0)
    add_footer(s, newpage())

    # ---- 4〜. 各事例（概要＋表）----
    for idx, c in enumerate(CASES, start=1):
        # 概要スライド
        s = blank_slide(prs)
        title_block(s, c["title"])
        # 画像（版ごとの画像を IMG_RATIO に cover-fit）
        img = fit_cover(pick_illust(idx), IMG_RATIO)
        ibx_w_in = 7.62; ibx_h_in = ibx_w_in / IMG_RATIO
        ibx_l, ibx_t = Inches(0.45), Inches(1.5)
        ibx_w, ibx_h = Inches(ibx_w_in), Inches(ibx_h_in)
        pic = s.shapes.add_picture(img, ibx_l, ibx_t, width=ibx_w, height=ibx_h)
        # 画像に細い枠線で締める
        pic.line.color.rgb = GRAYL; pic.line.width = Pt(0.75)
        # オーバーレイ
        ov = (ACTIVE_OVR or OVR)[idx]
        def NX(fx): return Emu(int(ibx_l) + int(ibx_w*fx))
        def NY(fy): return Emu(int(ibx_t) + int(ibx_h*fy))
        ax1,ay1,ax2,ay2 = ov["arrow"]
        add_arrow(s, NX(ax1),NY(ay1),NX(ax2),NY(ay2), color=RED, width=3.4)
        tx,ty = ov["tri"]
        add_triangle(s, NX(tx),NY(ty), Inches(0.5))
        for (lx,ly,lt) in ov["labels"]:
            add_label(s, NX(lx),NY(ly), lt)
        # 右カラム：危険ワンライナー
        rcx = Inches(8.32); rcw = Inches(4.55)
        add_text(s, rcx, Inches(2.0), rcw, Inches(0.5),
          [{"runs":[("⚠ ここが危険", dict(name=JP,size=18,bold=True,color=REDDK))]}])
        add_text(s, rcx, Inches(2.7), rcw, Inches(1.7),
          [{"runs":[(c["hazard"], dict(name=JP,size=15,bold=True,color=BLACK))],"line_spacing":1.22}],
          line_color=GRAYL, line_w=1.0, fill=RGBColor(0xFC,0xF3,0xF3), anchor=MSO_ANCHOR.MIDDLE)
        add_text(s, rcx, Inches(4.6), rcw, Inches(0.45),
          [{"runs":[(c["result"], dict(name=JP,size=13.5,bold=True,color=REDDK))]}])
        add_text(s, rcx, Inches(5.7), rcw, Inches(0.5),
          [{"runs":[("▶ 詳細・対策は次ページ", dict(name=JP,size=11.5,color=FOOT))]}])
        add_footer(s, newpage())

        # 表スライド
        s = blank_slide(prs)
        title_block(s, c["title"])
        build_table(s, c)
        # 下部注記
        add_text(s, Inches(0.6), Inches(6.30), Inches(12.1), Inches(0.6),
          [{"runs":[("出典：" + c["src"] + "（厚生労働省 職場のあんぜんサイト 等）", dict(name=JP,size=10,color=FOOT))],"space_after":2},
           {"runs":[("博展の現場では：", dict(name=JP,size=10.5,bold=True,color=REDDK)),
                    (c["site"], dict(name=JP,size=10.5,color=DARK))]}])
        add_footer(s, newpage())

    # ---- チェックリスト ----
    s = blank_slide(prs)
    title_block(s, "現場チェックリスト　設営・搬入・撤去・会場高所作業", "作業前に指差し確認。1項目でも×があれば作業を中止し是正する。")
    checklist_cols(s, "テールゲートリフター（荷役）", CHECK_TGL, "高所作業車（会場高所作業）", CHECK_AWP)
    add_footer(s, newpage())

    # ---- 出典 ----
    s = blank_slide(prs)
    title_block(s, "出典・参考資料")
    add_text(s, Inches(0.65), Inches(1.5), Inches(12.0), Inches(5.2),
      [{"runs":[("■ 統計・法令", dict(name=JP,size=14,bold=True,color=BLACK))],"space_after":4},
       {"runs":[("・厚生労働省 職場のあんぜんサイト：労働災害統計確定値（令和7年確定値 2026年5月27日公表）", dict(name=JP,size=12,color=DARK))],"space_after":3},
       {"runs":[("　https://anzeninfo.mhlw.go.jp/user/anzen/tok/anst00.html", dict(name=JP,size=10.5,color=FOOT))],"space_after":3},
       {"runs":[("・JNIOSH（労働安全衛生総合研究所）コラム No.118／研究報告 SRR-No.50／TGL安全リーフレット（6基本＆11場面別ルール）", dict(name=JP,size=12,color=DARK))],"space_after":3},
       {"runs":[("・TGL特別教育 義務化：施行通達 基発0328第5号（労働安全衛生規則 第36条 改正）", dict(name=JP,size=12,color=DARK))],"space_after":3},
       {"runs":[("・建荷協（建設荷役車両安全技術協会）死亡災害統計［資料提供：厚生労働省］", dict(name=JP,size=12,color=DARK))],"space_after":10},
       {"runs":[("■ 労働災害事例（厚生労働省 職場のあんぜんサイト 事例No.）", dict(name=JP,size=14,bold=True,color=BLACK))],"space_after":4},
       {"runs":[("・No.55（カゴ車転倒）／No.549・No.507（バケット墜落・はさまれ）／No.101377（車両転倒）／No.401・No.606（上方構造物はさまれ）", dict(name=JP,size=12,color=DARK))],"space_after":3},
       {"runs":[("・JNIOSH 公表事例（TGL昇降板からの墜落）／あんぜんサイト ヒヤリ・ハット hiy_0448", dict(name=JP,size=12,color=DARK))],"space_after":3},
       {"runs":[("　労働災害事例検索 https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_FND.aspx", dict(name=JP,size=10.5,color=FOOT))],"space_after":10},
       {"runs":[("※本資料の数値は令和7年確定値（2026年5月27日公表）時点。原典で確認できない項目は「—」または「未確認」と表記している。", dict(name=JP,size=10.5,color=FOOT))]}])
    add_footer(s, newpage())

    prs.save(out)
    print("SAVED", out, "slides=", len(prs.slides._sldIdLst))

def big_stats(s, items, top=1.9, val_sizes=None):
    n = len(items); gap = 0.35; total_w = 12.1
    cw = (total_w - gap*(n-1))/n
    x0 = 0.6
    for i,(val,unit,desc,color) in enumerate(items):
        x = x0 + i*(cw+gap)
        vs = (val_sizes or [66]*n)[i]
        add_text(s, Inches(x), Inches(top), Inches(cw), Inches(1.35),
          [{"runs":[(val, dict(name=JP,size=vs,bold=True,color=color)),
                    (unit, dict(name=JP,size=20,bold=True,color=color))]}],
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(s, Inches(x), Inches(top+1.5), Inches(cw), Inches(0.85),
          [{"runs":[(desc, dict(name=JP,size=12,color=DARK))]}],
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)

def build_table(s, c):
    rows = [
      ("発覚日時", c["reveal"], False),
      ("プロジェクト名", c["proj"], False),
      ("発生事象", c["event"], False),
      ("原因概要", c["cause"], False),
      ("対応", c["resp"], False),
      ("対策概要", c["meas"], True),
    ]
    L = Inches(0.6); T = Inches(1.4); W = Inches(12.13)
    label_w = Inches(2.25)
    heights = [0.55, 0.6, 1.05, 1.0, 0.5, 1.25]
    tbl_h = Inches(sum(heights))
    gtbl = s.shapes.add_table(len(rows), 2, L, T, W, tbl_h).table
    gtbl.first_row = False; gtbl.horz_banding = False
    gtbl.columns[0].width = label_w
    gtbl.columns[1].width = Emu(int(W)-int(label_w))
    for ri,(lab,val,is_list) in enumerate(rows):
        gtbl.rows[ri].height = Inches(heights[ri])
        # ラベルセル
        lc = gtbl.cell(ri,0)
        lc.fill.solid(); lc.fill.fore_color.rgb = GRAYL
        lc.vertical_anchor = MSO_ANCHOR.MIDDLE
        lc.margin_left=Pt(8); lc.margin_top=Pt(3); lc.margin_bottom=Pt(3)
        p=lc.text_frame.paragraphs[0]; r=p.add_run(); r.text=lab
        set_font(r, name=JP, size=13, bold=True, color=BLACK)
        # 値セル
        vc = gtbl.cell(ri,1)
        vc.fill.solid(); vc.fill.fore_color.rgb = WHITE
        vc.vertical_anchor = MSO_ANCHOR.MIDDLE
        vc.margin_left=Pt(10); vc.margin_top=Pt(4); vc.margin_bottom=Pt(4)
        tf=vc.text_frame; tf.word_wrap=True
        if is_list:
            for i,item in enumerate(val):
                p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
                p.space_after=Pt(2)
                r=p.add_run(); r.text="・"+item
                set_font(r, name=JP, size=12.5, color=BLACK)
        else:
            p=tf.paragraphs[0]; r=p.add_run(); r.text=val
            emph = (val.strip()=="—")
            set_font(r, name=JP, size=12.5, color=(FOOT if emph else BLACK))

def checklist_cols(s, t1, items1, t2, items2):
    cols = [(0.6, t1, items1, RGBColor(0xBF,0x9000,0x00) if False else REDDK),
            (6.95, t2, items2, REDDK)]
    for (x, title, items, col) in cols:
        add_text(s, Inches(x), Inches(1.55), Inches(5.8), Inches(0.5),
          [{"runs":[(title, dict(name=JP,size=15,bold=True,color=BLACK))]}],
          fill=RGBColor(0xEF,0xEF,0xEF), line_color=GRAYL, line_w=1.0, anchor=MSO_ANCHOR.MIDDLE)
        y = 2.3
        for it in items:
            # チェックボックスと本文を分離（折返し時に本文が□下へ回り込まない＝吊りインデント）
            add_text(s, Inches(x), Inches(y), Inches(0.4), Inches(0.8),
              [{"runs":[("□", dict(name=JP,size=15,bold=True,color=BLACK))]}], anchor=MSO_ANCHOR.TOP)
            add_text(s, Inches(x+0.42), Inches(y), Inches(5.7), Inches(0.8),
              [{"runs":[(it, dict(name=JP,size=12,color=DARK))],"line_spacing":1.14}], anchor=MSO_ANCHOR.TOP)
            y += 0.88

if __name__ == "__main__":
    main()
