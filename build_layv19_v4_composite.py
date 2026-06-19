# -*- coding: utf-8 -*-
"""
build_layv19_v4_composite.py — V4: 合成見本スライドを既存 sample_layers_v19.pptx に追記。
視点固定方式(LAYV19)の検証・たたき台。TGL(視点A)1セットで合成見本を作る。
・背景 bg_tgl を全面に敷く（カバー配置）
・同じ視点Aで生成した 崩れカゴ車(obj_rollcage_collapsing_c) と 下敷き作業員(worker_pinned_c) を
  回転は最小限（無回転）でそのまま重ねて事故シーンを1つ作る。
・各パーツは個別の画像オブジェクト（焼き込まない＝移動・回転・拡縮可能）。
既存ファイル(layers_v19/・sample_layers_v19.pptx)は破壊しない（追記のみ・新ファイル名スクリプト）。
Googleのみ生成素材(gemini-3-pro-image-preview)・OpenAI不使用・非破壊。
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
GRAY = RGBColor(0x44, 0x44, 0x44)
NAVY = RGBColor(0x1F, 0x3A, 0x5F)

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


def add_caption(slide, l, t, w, h, runs):
    """半透明ぎみの濃色帯にキャプション（背景写真の上で読めるように）。"""
    sp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sp.line.fill.background()
    sp.fill.solid(); sp.fill.fore_color.rgb = NAVY
    sp.shadow.inherit = False
    # 透明度 ~22%
    sppr = sp.fill._xPr.find(qn("a:solidFill"))
    srgb = sppr.find(qn("a:srgbClr"))
    a = srgb.makeelement(qn("a:alpha"), {"val": "78000"})
    srgb.append(a)
    tf = sp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(8); tf.margin_right = Pt(8)
    tf.margin_top = Pt(4); tf.margin_bottom = Pt(4)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    for txt, opt in runs:
        r = p.add_run(); r.text = txt
        set_font(r, **opt)
    return sp


def aspect_of(path):
    with Image.open(path) as im:
        return im.width / im.height


def cover_bg(slide, path, aspect):
    """背景をスライド全面にカバー配置（はみ出しは許容・中央寄せ）。"""
    slide_ar = SW_IN / SH_IN
    if aspect > slide_ar:
        # 画像が横長 → 高さを合わせ横はみ出し
        ih = SH_IN; iw = ih * aspect
    else:
        iw = SW_IN; ih = iw / aspect
    ix = (SW_IN - iw) / 2
    iy = (SH_IN - ih) / 2
    return slide.shapes.add_picture(path, Inches(ix), Inches(iy), Inches(iw), Inches(ih))


def place(slide, path, aspect, cx, by, w):
    """中心x=cx・底辺y=by・幅w でアスペクト維持配置（個別オブジェクト）。左上座標を返す。"""
    h = w / aspect
    l = cx - w / 2
    t = by - h
    pic = slide.shapes.add_picture(path, Inches(l), Inches(t), Inches(w), Inches(h))
    return pic


def main():
    tgl = os.path.join(LV, "tgl")
    bg = os.path.join(tgl, "bg_tgl.png")
    obj = os.path.join(tgl, "obj_rollcage_collapsing_c.png")
    wk = os.path.join(tgl, "worker_pinned_c.png")

    a_bg = aspect_of(bg)
    a_obj = aspect_of(obj)
    a_wk = aspect_of(wk)

    if os.path.exists(OUT):
        prs = Presentation(OUT)
    else:
        prs = Presentation()
        prs.slide_width = Inches(SW_IN)
        prs.slide_height = Inches(SH_IN)

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # (1) 背景を全面に敷く（個別オブジェクト・焼き込まない）
    cover_bg(slide, bg, a_bg)

    # (2) 同視点パーツを最小回転（無回転）でそのまま重ねる
    #     ・崩れカゴ車：荷台脇の地面に立てる（中央やや右）
    #     ・下敷き作業員：カゴ車の足元に横たわる（カゴ車の前に重ね＝下敷き表現）
    # 作業員を先に（奥）→カゴ車を後に(手前)で重ねると「カゴ車に潰される」読みになる
    place(slide, wk, a_wk, cx=6.7, by=6.95, w=5.0)        # 下敷き作業員（地面）
    place(slide, obj, a_obj, cx=6.9, by=6.55, w=3.1)      # 崩れカゴ車（手前に倒れ込む）

    # 視点バッジ（無回転で角度が合うことの明示）
    add_caption(slide, 0.35, 0.32, 4.1, 0.5,
                [("合成見本（TGL）／全パーツ＝視点A・無回転", dict(size=14, bold=True, color=WHITE))])

    # 下部注記
    add_caption(slide, 0.35, 6.35, 9.4, 0.85,
                [("視点固定方式の検証・たたき台：", dict(size=12, bold=True, color=WHITE)),
                 ("背景／崩れカゴ車／下敷き作業員を同一視点A（同じ目線高さ・パース・光源）で生成し、回転0°でそのまま重ねただけ。各パーツは個別の画像オブジェクト（焼き込み無し＝移動・回転・拡縮可）。",
                  dict(size=11, color=WHITE))])

    slide.notes_slide.notes_text_frame.text = (
        "V4 合成見本（LAYV19）。視点固定方式の検証・たたき台。"
        "TGL（視点A）の bg_tgl を全面に敷き、同じ視点Aで生成した "
        "obj_rollcage_collapsing（崩れカゴ車）と worker_pinned（下敷き作業員）を"
        "回転は最小限（無回転）でそのまま重ねて事故シーンを1つ作成。"
        "各パーツは個別の画像オブジェクト（焼き込まない＝移動・回転・拡縮が可能）。"
        "生成時点で角度を揃える方式のため、パワポ側での回転合わせはほぼ不要。"
        "Googleのみ生成素材（gemini-3-pro-image-preview）・OpenAI不使用・非破壊。"
    )

    prs.save(OUT)
    print("SAVED", OUT, "slides:", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    main()
