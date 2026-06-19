# -*- coding: utf-8 -*-
"""
build_layv19_v3_catalog.py — V3: 素材一覧スライドを新規 sample_layers_v19.pptx に作成。
視点固定方式(LAYV19)で生成した素材を一覧化し、各パーツに「視点A/視点B」を明記する。
TGL(視点A)：bg_tgl・obj_rollcage_collapsing・worker_pinned
高所(視点B)：bg_aerial・worker_basket
パーツのサムネは透明余白をアルファ境界で切り出した新ファイル(*_c.png)を使う（非破壊）。
既存ファイル(layers_v19/等)は破壊しない。Googleのみ生成素材(gemini-3-pro-image-preview)・OpenAI不使用。
合成見本スライド(V4)は別タスクで同 pptx に追記する。
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

BASE = r"C:\Users\kanet\20260522\safe1"
LV = os.path.join(BASE, "layers_v19")
OUT = os.path.join(BASE, "sample_layers_v19.pptx")

JP = "游ゴシック"
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xC0, 0x00, 0x00)
GRAY = RGBColor(0x44, 0x44, 0x44)
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
TEAL = RGBColor(0x0E, 0x6E, 0x6E)
FRAME = RGBColor(0xD0, 0xD0, 0xD0)

SW_IN, SH_IN = 13.333, 7.5


def set_font(run, name=JP, size=14, bold=False, color=BLACK):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rPr.set("lang", "ja-JP")
    rPr.set("altLang", "en-US")
    for tag in ("a:latin", "a:ea", "a:cs"):
        e = rPr.find(qn(tag))
        if e is None:
            e = rPr.makeelement(qn(tag), {}); rPr.append(e)
        e.set("typeface", name)


def add_text(slide, l, t, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, wrap=True):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(4); tf.margin_right = Pt(4)
    tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
    p = tf.paragraphs[0]
    p.alignment = align
    for txt, opt in runs:
        r = p.add_run(); r.text = txt
        set_font(r, **opt)
    return tb


def badge(slide, l, t, w, h, text, fill):
    sp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sp.line.fill.background()
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    sp.shadow.inherit = False
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(2); tf.margin_right = Pt(2)
    tf.margin_top = Pt(0); tf.margin_bottom = Pt(0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    set_font(r, size=10, bold=True, color=WHITE)
    return sp


def crop_to_alpha(src, dst, pad=6):
    """透明余白を切り落とした新PNGを作成（非破壊・新ファイル名）。アスペクト比を返す。"""
    with Image.open(src) as im:
        im = im.convert("RGBA")
        w, h = im.size
        bb = im.split()[3].getbbox() or (0, 0, w, h)
        l = max(0, bb[0] - pad); t = max(0, bb[1] - pad)
        r = min(w, bb[2] + pad); b = min(h, bb[3] + pad)
        cr = im.crop((l, t, r, b))
        if not os.path.exists(dst):
            cr.save(dst)
        return cr.width / cr.height


def aspect_of(path):
    with Image.open(path) as im:
        return im.width / im.height


def thumb(slide, path, aspect, cell_l, cell_t, cell_w, cell_h, label, sub, view, view_fill):
    """セル内にサムネ＋枠＋ラベル＋視点バッジを配置。"""
    # フレーム（背景の薄い箱）
    fr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cell_l), Inches(cell_t),
                                Inches(cell_w), Inches(cell_h))
    fr.fill.solid(); fr.fill.fore_color.rgb = RGBColor(0xF6, 0xF6, 0xF6)
    fr.line.color.rgb = FRAME; fr.line.width = Pt(0.75)
    fr.shadow.inherit = False

    img_area_h = cell_h - 0.62  # 下にラベル領域
    pad = 0.08
    aw = cell_w - 2 * pad
    ah = img_area_h - 2 * pad
    # アスペクト維持でフィット
    if aw / ah > aspect:
        ih = ah; iw = ih * aspect
    else:
        iw = aw; ih = iw / aspect
    ix = cell_l + (cell_w - iw) / 2
    iy = cell_t + pad + (ah - ih) / 2
    slide.shapes.add_picture(path, Inches(ix), Inches(iy), Inches(iw), Inches(ih))

    # 視点バッジ（右上）
    badge(slide, cell_l + cell_w - 1.0, cell_t + 0.08, 0.92, 0.3, view, view_fill)

    # ラベル
    add_text(slide, cell_l + 0.06, cell_t + cell_h - 0.58, cell_w - 0.12, 0.3,
             [(label, dict(size=12, bold=True, color=BLACK))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, cell_l + 0.06, cell_t + cell_h - 0.30, cell_w - 0.12, 0.26,
             [(sub, dict(size=9, color=GRAY))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


def section_label(slide, l, t, text, fill):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(0.16), Inches(0.34))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill; sp.line.fill.background(); sp.shadow.inherit = False
    add_text(slide, l + 0.24, t - 0.02, 9.0, 0.38,
             [(text, dict(size=14, bold=True, color=fill))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


def main():
    tgl = os.path.join(LV, "tgl")
    aer = os.path.join(LV, "aerial")

    # アルファ境界で切り出したパーツのサムネ（新ファイル *_c.png）
    a_obj = crop_to_alpha(os.path.join(tgl, "obj_rollcage_collapsing.png"),
                          os.path.join(tgl, "obj_rollcage_collapsing_c.png"))
    a_wk = crop_to_alpha(os.path.join(tgl, "worker_pinned.png"),
                         os.path.join(tgl, "worker_pinned_c.png"))
    a_wb = crop_to_alpha(os.path.join(aer, "worker_basket.png"),
                         os.path.join(aer, "worker_basket_c.png"))
    a_bgt = aspect_of(os.path.join(tgl, "bg_tgl.png"))
    a_bga = aspect_of(os.path.join(aer, "bg_aerial.png"))

    # 既存があれば開いて先頭スライドとして使い回し、無ければ新規（再開安全）
    if os.path.exists(OUT):
        prs = Presentation(OUT)
    else:
        prs = Presentation()
        prs.slide_width = Inches(SW_IN)
        prs.slide_height = Inches(SH_IN)

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # タイトル
    add_text(slide, 0.4, 0.18, SW_IN - 0.8, 0.5,
             [("素材一覧 — 視点固定レイヤー合成（LAYV19）", dict(size=22, bold=True, color=NAVY))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, 0.4, 0.66, SW_IN - 0.8, 0.34,
             [("各シチュでカメラ視点を1つ決め打ちし、背景・荷物・作業員を同じ視点/目線高さ/パース/光源で生成（角度を生成時点で一致）。Googleのみ＝gemini-3-pro-image-preview・OpenAI不使用。",
               dict(size=10, color=GRAY))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

    # 視点凡例
    badge(slide, 9.55, 0.2, 1.7, 0.32, "視点A = TGL", NAVY)
    badge(slide, 11.35, 0.2, 1.7, 0.32, "視点B = 高所", TEAL)

    # ── セクション1：TGL（視点A） 3パーツ
    section_label(slide, 0.4, 1.18, "シチュ1：TGL（荷崩れ・下敷き）／全パーツ＝視点A", NAVY)
    row1_t = 1.62
    cw, ch = 4.0, 2.6
    gap = 0.27
    xs = 0.4
    cells = [
        (os.path.join(tgl, "bg_tgl.png"), a_bgt, "bg_tgl（背景）", "TGL付きトラック後部・人物なし・不透過", "視点A", NAVY),
        (os.path.join(tgl, "obj_rollcage_collapsing_c.png"), a_obj, "obj_rollcage_collapsing", "崩れたカゴ車・透過RGBA", "視点A", NAVY),
        (os.path.join(tgl, "worker_pinned_c.png"), a_wk, "worker_pinned", "下敷き作業員・フルハーネス・透過・流血なし", "視点A", NAVY),
    ]
    for i, (p, a, lab, sub, vw, vf) in enumerate(cells):
        thumb(slide, p, a, xs + i * (cw + gap), row1_t, cw, ch, lab, sub, vw, vf)

    # ── セクション2：高所（視点B） 2パーツ
    section_label(slide, 0.4, 4.42, "シチュ2：高所作業車（バスケットでの被災）／全パーツ＝視点B", TEAL)
    row2_t = 4.86
    cells2 = [
        (os.path.join(aer, "bg_aerial.png"), a_bga, "bg_aerial（背景）", "ブーム式高所作業車・立上・人物なし・不透過", "視点B", TEAL),
        (os.path.join(aer, "worker_basket_c.png"), a_wb, "worker_basket", "バスケット内被災・フルハーネス・透過・流血なし", "視点B", TEAL),
    ]
    for i, (p, a, lab, sub, vw, vf) in enumerate(cells2):
        thumb(slide, p, a, xs + i * (cw + gap), row2_t, cw, ch, lab, sub, vw, vf)

    # 右下メモ
    add_text(slide, 8.6, 4.86, 4.3, 2.6,
             [("視点固定方式：\n・背景／荷物／作業員を同一視点で生成\n・後からの回転合わせを最小化\n・各パーツは透過PNG（rembg/Pillowで白背景を除去）\n・合成見本は次スライド参照",
               dict(size=11, color=GRAY))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)

    slide.notes_slide.notes_text_frame.text = (
        "V3 素材一覧（LAYV19）。視点固定レイヤー合成のための素材カタログ。"
        "TGL=視点A（bg_tgl・obj_rollcage_collapsing・worker_pinned）、"
        "高所=視点B（bg_aerial・worker_basket）。各パーツに視点A/Bを明記。"
        "Googleのみ生成素材（gemini-3-pro-image-preview）・OpenAI不使用・非破壊。"
    )

    prs.save(OUT)
    print("SAVED", OUT, "slides:", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    main()
