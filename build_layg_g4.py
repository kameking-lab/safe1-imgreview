# -*- coding: utf-8 -*-
"""
build_layg_g4.py — G4: 素材一覧スライドを sample_layers_v18.pptx に作成（新規）。
レイヤー合成用パーツ（背景/荷物/作業員）のサムネ＋ラベルを1枚に一覧表示。
Googleのみ生成・透過RGBA。各パーツは個別オブジェクト（焼き込まない）。
合成見本(G5)・PDF(BUILD)は後段で追加する想定。既存ファイルは破壊しない。
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from PIL import Image

BASE = r"C:\Users\kanet\20260522\safe1"
LV = os.path.join(BASE, "layers_v18")
OUT = os.path.join(BASE, "sample_layers_v18.pptx")

JP = "游ゴシック"
BLACK = RGBColor(0x00, 0x00, 0x00)
RED = RGBColor(0xC0, 0x00, 0x00)
GRAY = RGBColor(0x5E, 0x5E, 0x5E)
HDR = RGBColor(0x1F, 0x3B, 0x57)

SW, SH = Inches(13.333), Inches(7.5)


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


def add_text(slide, l, t, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(2); tf.margin_right = Pt(2)
    tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
    p = tf.paragraphs[0]
    p.alignment = align
    for txt, opt in runs:
        r = p.add_run(); r.text = txt
        set_font(r, **opt)
    return tb


def place_row(slide, items, x0, row_w, y_top, max_h, label_h=0.3, lblsize=10.5):
    """items: list of (path, label). 個別の画像オブジェクトとして等間隔セルに中央配置。"""
    n = len(items)
    cell_w = row_w / n
    for i, (path, label) in enumerate(items):
        with Image.open(path) as im:
            iw, ih = im.size
        avail_w = cell_w - 0.18
        bw = avail_w
        bh = bw * ih / iw
        if bh > max_h:
            bh = max_h
            bw = bh * iw / ih
        cx = x0 + cell_w * i + cell_w / 2
        l = cx - bw / 2
        t = y_top + (max_h - bh) / 2
        slide.shapes.add_picture(path, Inches(l), Inches(t), Inches(bw), Inches(bh))
        add_text(slide, x0 + cell_w * i, y_top + max_h + 0.02, cell_w, label_h,
                 [(label, dict(size=lblsize, color=GRAY))], align=PP_ALIGN.CENTER,
                 anchor=MSO_ANCHOR.TOP)


def section_header(slide, l, t, w, text, count):
    add_text(slide, l, t, w, 0.3,
             [(text, dict(size=13, bold=True, color=HDR)),
              (f"  （{count}点・" + ("不透過" if "背景" in text else "透過RGBA") + "）",
               dict(size=10.5, color=GRAY))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


def main():
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    M = 0.45
    W = 13.333 - 2 * M

    # タイトル
    add_text(slide, M, 0.22, W, 0.5,
             [("素材一覧（レイヤー合成用パーツ）", dict(size=22, bold=True, color=BLACK))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, M, 0.74, W, 0.3,
             [("Google（Nano Banana Pro = gemini-3-pro-image-preview）のみで生成。"
               "背景=不透過写真／荷物・作業員=純白背景から透過化したRGBAパーツ。", dict(size=10.5, color=GRAY))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

    bg = os.path.join(LV, "bg")
    obj = os.path.join(LV, "obj")
    wk = os.path.join(LV, "worker")

    bg_items = [
        (os.path.join(bg, "bg_warehouse1.png"), "倉庫TGL① bg_warehouse1"),
        (os.path.join(bg, "bg_warehouse2.png"), "倉庫TGL② bg_warehouse2"),
        (os.path.join(bg, "bg_venue_dock.png"), "会場搬入口 bg_venue_dock"),
    ]
    obj_items = [
        (os.path.join(obj, "obj_rollcage_collapsing.png"), "カゴ車 崩れ collapsing"),
        (os.path.join(obj, "obj_rollcage_tipping.png"), "カゴ車 転倒 tipping"),
        (os.path.join(obj, "obj_rollcage_normal.png"), "カゴ車 正常 normal"),
        (os.path.join(obj, "obj_panelcart_sliding.png"), "パネル台車 滑落 sliding"),
    ]
    wk_items = [
        (os.path.join(wk, "worker_hand_pain.png"), "手を痛がる hand_pain"),
        (os.path.join(wk, "worker_foot_crouch.png"), "足を押さえしゃがむ foot_crouch"),
        (os.path.join(wk, "worker_fallen_back.png"), "仰向け転倒 fallen_back"),
        (os.path.join(wk, "worker_startled.png"), "驚き後傾 startled"),
        (os.path.join(wk, "worker_stand.png"), "通常立ち stand"),
    ]

    # 背景
    section_header(slide, M, 1.12, W, "■ 背景  layers_v18/bg", len(bg_items))
    place_row(slide, bg_items, M, W, 1.48, 1.5)

    # 荷物
    section_header(slide, M, 3.18, W, "■ 荷物パーツ  layers_v18/obj", len(obj_items))
    place_row(slide, obj_items, M, W, 3.52, 1.4)

    # 作業員
    section_header(slide, M, 5.18, W, "■ 作業員パーツ  layers_v18/worker", len(wk_items))
    place_row(slide, wk_items, M, W, 5.5, 1.45)

    # 注記（たたき台）
    add_text(slide, M, 7.12, W, 0.32,
             [("※ これはレイヤー合成のたたき台。各部品は移動・回転・拡縮可能な個別画像オブジェクト。最終調整はPowerPoint上で。",
               dict(size=9.5, color=GRAY))],
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

    # ノートにも明記
    notes = slide.notes_slide.notes_text_frame
    notes.text = ("素材一覧（G4）。Googleのみ生成（gemini-3-pro-image-preview）・OpenAI不使用。"
                  "各パーツは個別の移動・回転・拡縮可能な画像オブジェクト。"
                  "合成見本(TGL墜落/荷崩れ)は後続スライドで配置。")

    prs.save(OUT)
    print("SAVED", OUT, "slides=", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    main()
