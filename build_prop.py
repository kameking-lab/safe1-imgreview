# -*- coding: utf-8 -*-
"""
build_prop.py — 商談用 提案資料 proposal_hakuten.pptx 生成（メラビアン重視・ビジュアル7割）

非破壊：既存ファイルは読むだけ。出力先は引数で指定（既定 proposal_hakuten.pptx）。
スライド構成は SLIDES に builder 関数を登録して積み上げる（P2〜P6 で順次追加）。
日本語フォントは游ゴシック（pptx 側で typeface 指定・禁則有効）。16:9。
数値・法令は RULES_PROP.md の確定素材のみ（捏造なし）。新規 AI 画像生成なし。
"""
import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from PIL import Image

BASE = r"C:\Users\kanet\20260522\safe1"
FIGS = os.path.join(BASE, "figs")

# ---- 配色（安全色＋ブランド）------------------------------------------------
NAVY   = RGBColor(0x1F, 0x3A, 0x60)   # データ・ブランド基調
INK    = RGBColor(0x1A, 0x1A, 0x1A)   # 本文黒
GRAY   = RGBColor(0x5E, 0x5E, 0x5E)   # 補助・出典
LGRAY  = RGBColor(0x8A, 0x8A, 0x8A)
RED    = RGBColor(0xE2, 0x23, 0x1A)   # 危険
YELLOW = RGBColor(0xF2, 0xB7, 0x05)   # 注意
GREEN  = RGBColor(0x2E, 0x9E, 0x5B)   # 対策
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
PALE   = RGBColor(0xF3, 0xF5, 0xF8)   # 薄地カード

JP  = "游ゴシック"
JPM = "游ゴシック Medium"
SW, SH = Inches(13.333), Inches(7.5)

# 確定素材（オーナー検証済・改変禁止）
SUP = "監修：金田 義太（労働安全コンサルタント 登録第4840号）"
CLIENT = "株式会社 博展　御中"
TODAY = "2026年6月21日"


# ---- 低レベル描画ヘルパ ------------------------------------------------------
def set_font(run, name=JP, size=14, bold=False, color=INK):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rPr.set("lang", "ja-JP"); rPr.set("altLang", "en-US")
    for tag in ("a:latin", "a:ea", "a:cs"):
        e = rPr.find(qn(tag))
        if e is None:
            e = rPr.makeelement(qn(tag), {}); rPr.append(e)
        e.set("typeface", name)


def add_text(slide, l, t, w, h, lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             fill=None, line_color=None, line_w=None, wrap=True):
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


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def rect(slide, l, t, w, h, fill, line=None, line_w=0.0, shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is not None:
        sh.line.color.rgb = line; sh.line.width = Pt(line_w or 1.0)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def circle_glyph(slide, cx, cy, d, fill, glyph, gsize, gcolor=WHITE):
    sh = slide.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int(cx - d / 2)), Emu(int(cy - d / 2)), Emu(int(d)), Emu(int(d)))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = False
    tf.margin_top = Pt(0); tf.margin_bottom = Pt(0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = glyph
    set_font(r, name=JP, size=gsize, bold=True, color=gcolor)
    return sh


def add_arrow(slide, x1, y1, x2, y2, color=RED, width=3.2):
    cn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    cn.line.color.rgb = color; cn.line.width = Pt(width)
    ln = cn.line._get_or_add_ln()
    ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "lg", "len": "lg"}))
    return cn


def add_triangle(slide, l, t, size, mark="！"):
    sh = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, l, t, size, size)
    sh.fill.solid(); sh.fill.fore_color.rgb = YELLOW
    sh.line.color.rgb = INK; sh.line.width = Pt(1.5); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = False
    tf.margin_top = Pt(7); tf.margin_bottom = Pt(0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = mark
    set_font(r, name=JP, size=14, bold=True, color=INK)
    return sh


def img_ratio(path):
    im = Image.open(path); w, h = im.size; return w / h


def place_fig(slide, path, box_l, box_t, box_w, box_h, line=None):
    """box(EMU) 内に縦横比維持で中央配置。歪みなし。枠線オプション。"""
    r = img_ratio(path)
    bw, bh = int(box_w), int(box_h)
    if bw / bh > r:
        nh = bh; nw = int(bh * r)
    else:
        nw = bw; nh = int(bw / r)
    l = int(box_l) + (bw - nw) // 2
    t = int(box_t) + (bh - nh) // 2
    pic = slide.shapes.add_picture(path, Emu(l), Emu(t), Emu(nw), Emu(nh))
    if line is not None:
        pic.line.color.rgb = line; pic.line.width = Pt(0.75)
    return pic


def tricolor_rule(slide, l, t, w, h=Inches(0.07)):
    """安全色（赤・黄・緑）の3分割細バー。"""
    seg = int(w) // 3
    for i, c in enumerate((RED, YELLOW, GREEN)):
        rect(slide, Emu(int(l) + i * seg), t, Emu(seg), h, c)


def footer(slide, page_no, note=None):
    add_text(slide, Inches(0.4), Inches(7.04), Inches(9.5), Inches(0.34),
             [{"runs": [(note or SUP, dict(name=JP, size=9, color=LGRAY))]}],
             anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(12.55), Inches(7.04), Inches(0.55), Inches(0.34),
             [{"runs": [(str(page_no), dict(name=JP, size=10, color=LGRAY))]}],
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def kicker(slide, text, color):
    """左上の小さな色タグ見出し。"""
    w = Inches(0.5 + 0.16 * len(text))
    add_text(slide, Inches(0.6), Inches(0.42), w, Inches(0.42),
             [{"runs": [(text, dict(name=JP, size=13, bold=True, color=WHITE))]}],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=color)
    return Inches(0.6) + int(w)


# ============================ スライド ========================================
def slide_cover(prs, page):
    s = blank_slide(prs)
    # 左の縦帯（ネイビー）＋上部トライカラー
    rect(s, 0, 0, Inches(0.22), SH, NAVY)
    tricolor_rule(s, Inches(0.22), 0, Emu(int(SW) - int(Inches(0.22))), Inches(0.10))
    # タイトル（2行・大）
    add_text(s, Inches(1.05), Inches(1.55), Inches(11.4), Inches(1.1),
             [{"runs": [("データに基づく安全管理", dict(name=JP, size=46, bold=True, color=NAVY))]}])
    add_text(s, Inches(1.05), Inches(2.62), Inches(11.4), Inches(1.1),
             [{"runs": [("＋ ", dict(name=JP, size=46, bold=True, color=RED)),
                        ("AIによる自動化", dict(name=JP, size=46, bold=True, color=NAVY))]}])
    # サブ（価値1行）
    add_text(s, Inches(1.08), Inches(3.92), Inches(11.0), Inches(0.6),
             [{"runs": [("経験と勘に頼らない、科学的な安全教育を、速く・安く。",
                         dict(name=JP, size=18, color=GRAY))]}])
    # 区切り線
    rect(s, Inches(1.08), Inches(4.78), Inches(4.4), Inches(0.04), NAVY)
    # 宛先・監修
    add_text(s, Inches(1.05), Inches(5.30), Inches(9.0), Inches(0.6),
             [{"runs": [(CLIENT, dict(name=JP, size=22, bold=True, color=INK))]}])
    add_text(s, Inches(1.08), Inches(6.10), Inches(10.5), Inches(0.4),
             [{"runs": [(SUP, dict(name=JP, size=12, color=GRAY))]}])
    add_text(s, Inches(1.08), Inches(6.55), Inches(10.5), Inches(0.4),
             [{"runs": [("作成日：" + TODAY, dict(name=JP, size=11, color=LGRAY))]}])
    return page  # 表紙はページ番号なし


def slide_problem(prs, page):
    s = blank_slide(prs)
    kicker(s, "課題", RED)
    add_text(s, Inches(1.7), Inches(0.40), Inches(11.0), Inches(0.5),
             [{"runs": [("従来の安全教育は、ベテランの“経験頼み”",
                         dict(name=JP, size=26, bold=True, color=INK))]}],
             anchor=MSO_ANCHOR.MIDDLE)
    # 左：大きな円（勘）
    cx, cy = int(Inches(3.2)), int(Inches(3.9))
    circle_glyph(s, cx, cy, int(Inches(2.6)), NAVY, "勘", 96)
    add_text(s, Inches(1.6), Inches(5.45), Inches(3.2), Inches(0.5),
             [{"runs": [("経験・勘に依存", dict(name=JP, size=18, bold=True, color=NAVY))]}],
             align=PP_ALIGN.CENTER)
    # 注意三角
    add_triangle(s, Inches(4.55), Inches(3.35), Inches(0.95))
    # 矢印（赤）→ 右の課題チップ3つ
    add_arrow(s, Inches(4.7), Inches(3.9), Inches(6.0), Inches(3.9), color=RED, width=4.0)
    chips = [("属人的", "教える人で内容が変わる"),
             ("再現性がない", "同じ品質を保てない"),
             ("更新が遅い", "最新の事故に追いつけない")]
    cx0, cy0, cw, ch, gap = Inches(6.25), Inches(2.05), Inches(6.5), Inches(1.05), Inches(0.30)
    for i, (head, sub) in enumerate(chips):
        ty = int(cy0) + i * (int(ch) + int(gap))
        rect(s, cx0, Emu(ty), cw, ch, PALE, line=YELLOW, line_w=2.0)
        rect(s, cx0, Emu(ty), Inches(0.14), ch, YELLOW)
        add_text(s, Emu(int(cx0) + int(Inches(0.34))), Emu(ty + int(Inches(0.12))),
                 Emu(int(cw) - int(Inches(0.5))), Inches(0.5),
                 [{"runs": [(head, dict(name=JP, size=20, bold=True, color=INK))]}])
        add_text(s, Emu(int(cx0) + int(Inches(0.34))), Emu(ty + int(Inches(0.58))),
                 Emu(int(cw) - int(Inches(0.5))), Inches(0.4),
                 [{"runs": [(sub, dict(name=JP, size=13, color=GRAY))]}])
    add_text(s, Inches(0.6), Inches(6.30), Inches(12.1), Inches(0.5),
             [{"runs": [("→ 仕組みで支える、科学的な安全教育へ。",
                         dict(name=JP, size=15, bold=True, color=NAVY))]}])
    footer(s, page)
    return page + 1


def slide_approach(prs, page):
    s = blank_slide(prs)
    kicker(s, "解決アプローチ", NAVY)
    # 矢印フロー図（P1生成・既存図を流用。図に見出しを内蔵するため大見出しは置かない）
    fig = os.path.join(FIGS, "prop_approach_flow.png")
    place_fig(s, fig, Inches(0.6), Inches(1.35), Inches(12.13), Inches(4.6))
    add_text(s, Inches(0.6), Inches(6.30), Inches(12.1), Inches(0.5),
             [{"runs": [("分析 → 危険の科学的特定 → 教材化 → AIで量産。属人化せず、速く・安く。",
                         dict(name=JP, size=14, color=GRAY))]}])
    footer(s, page)
    return page + 1


# 登録順＝スライド順（P3〜P6 でここに追記）
SLIDES = [slide_cover, slide_problem, slide_approach]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "proposal_hakuten.pptx")
    prs = Presentation()
    prs.slide_width = SW; prs.slide_height = SH
    page = 1
    for fn in SLIDES:
        page = fn(prs, page)
    prs.save(out)
    print("SAVED", out, "slides=", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    main()
