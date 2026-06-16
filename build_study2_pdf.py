# build_study2_pdf.py — BUILD: study_tgl_aerial_v2.pdf を生成（非破壊・新名）
# ------------------------------------------------------------------------------
# content_study2.PAGES（構成データ）と figs/ のPNGを PIL で A4縦ページ画像に合成し、
# 1テーマ1ページ・図表中心・流し読み版面の PDF を出力する。
#   - 既存 study_tgl_aerial.pdf は無改変。出力は study_tgl_aerial_v2.pdf（別名）。
#   - 日本語フォントは C:\Windows\Fonts\YuGoth*.ttc を登録（文字化け回避）。
#   - 文章/数値/法令は content_study2.py が保持する確定値のみ（捏造・改変なし）。
# ------------------------------------------------------------------------------
import os
from PIL import Image, ImageDraw, ImageFont

import content_study2 as C

# ---- 版面（A4縦 150dpi）------------------------------------------------------
W, H = 1240, 1754
MARGIN = 80
BG = "#ffffff"
INK = "#1c1c1c"
SUBINK = "#555555"
LIGHT = "#f2f4f7"

FONT_B = r"C:\Windows\Fonts\YuGothB.ttc"
FONT_R = r"C:\Windows\Fonts\YuGothR.ttc"


def font(bold, size):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def text_w(draw, s, f):
    return draw.textbbox((0, 0), s, font=f)[2]


def wrap(draw, s, f, max_w):
    """日本語向け：max_w幅で折返し（文字単位）。改行は尊重。"""
    out = []
    for raw in s.split("\n"):
        line = ""
        for ch in raw:
            if text_w(draw, line + ch, f) <= max_w:
                line += ch
            else:
                out.append(line)
                line = ch
        out.append(line)
    return out


def draw_wrapped(draw, xy, s, f, fill, max_w, lh):
    x, y = xy
    for ln in wrap(draw, s, f, max_w):
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def header(draw, title, accent):
    """ページ上部の見出しバー（左に色帯）。複数行可。"""
    draw.rectangle([0, 0, W, 8], fill=accent)
    tf = font(True, 52)
    lines = title.split("\n")
    y = 56
    draw.rectangle([MARGIN - 24, y + 4, MARGIN - 12, y + 4 + len(lines) * 64], fill=accent)
    for ln in lines:
        draw.text((MARGIN, y), ln, font=tf, fill=INK)
        y += 64
    return y + 20


def footer(draw, s, accent):
    f = font(False, 22)
    y = H - 70
    draw.line([MARGIN, y - 12, W - MARGIN, y - 12], fill="#dddddd", width=2)
    draw_wrapped(draw, (MARGIN, y), s, f, SUBINK, W - 2 * MARGIN, 28)


def paste_fit(img, fig_path, box):
    """box=(x,y,w,h) に縦横比維持で中央配置。"""
    x, y, bw, bh = box
    fig = Image.open(fig_path).convert("RGB")
    fw, fh = fig.size
    scale = min(bw / fw, bh / fh)
    nw, nh = int(fw * scale), int(fh * scale)
    fig = fig.resize((nw, nh), Image.LANCZOS)
    img.paste(fig, (x + (bw - nw) // 2, y + (bh - nh) // 2))


# ---- ページ種別ごとの描画 ----------------------------------------------------
def render_cover(p):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill=p["accent"])
    # タイトル
    tf = font(True, 60)
    y = 90
    for ln in p["title"].split("\n"):
        d.text((MARGIN, y), ln, font=tf, fill=INK)
        y += 78
    # サブタイトル
    sf = font(True, 38)
    y += 6
    d.text((MARGIN, y), p["subtitle"], font=sf, fill=p["accent"])
    y += 70
    # 6カード（2列×3行）
    cols, gap = 2, 30
    cw = (W - 2 * MARGIN - gap) // cols
    ch = 250
    cap_f = font(True, 30)
    val_f = font(True, 38)
    for i, (cap, val, col) in enumerate(p["cards"]):
        r, c = divmod(i, cols)
        cx = MARGIN + c * (cw + gap)
        cy = y + r * (ch + gap)
        rounded(d, [cx, cy, cx + cw, cy + ch], 24, fill=LIGHT)
        d.rectangle([cx, cy, cx + 14, cy + ch], fill=col)
        d.text((cx + 36, cy + 26), cap, font=cap_f, fill=col)
        draw_wrapped(d, (cx + 36, cy + 76), val, val_f, INK, cw - 60, 50)
    footer(d, p["footer"], p["accent"])
    return img


def render_fig(p):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, p["title"], p["accent"])
    # 要点3つ（番号バッジ）
    pf = font(False, 30)
    bf = font(True, 28)
    y += 10
    for i, pt in enumerate(p["points"], 1):
        by = y
        d.ellipse([MARGIN, by, MARGIN + 40, by + 40], fill=p["accent"])
        bw = text_w(d, str(i), bf)
        d.text((MARGIN + 20 - bw // 2, by + 5), str(i), font=bf, fill="#ffffff")
        y = draw_wrapped(d, (MARGIN + 60, by + 2), pt, pf, INK, W - 2 * MARGIN - 60, 40)
        y += 18
    # 図（残り領域に収める）
    fig_top = y + 10
    fig_bottom = H - 110
    paste_fit(img, p["fig"], (MARGIN, fig_top, W - 2 * MARGIN, fig_bottom - fig_top))
    footer(d, p["source"], p["accent"])
    return img


def render_qa(p):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, p["title"], p["accent"])
    qf = font(True, 28)
    af = font(False, 27)
    y += 8
    for q, a in p["qa"]:
        rounded(d, [MARGIN, y, W - MARGIN, y + 4], 2, fill=LIGHT)
        y += 14
        y = draw_wrapped(d, (MARGIN, y), q, qf, p["accent"], W - 2 * MARGIN, 36)
        y = draw_wrapped(d, (MARGIN + 24, y + 2), a, af, INK, W - 2 * MARGIN - 24, 34)
        y += 18
    footer(d, p["footer"], p["accent"])
    return img


def render_sources(p):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = header(d, p["title"], p["accent"])
    y += 10

    def section(label, lines, col):
        nonlocal y
        d.text((MARGIN, y), label, font=font(True, 32), fill=col)
        y += 48
        f = font(False, 24)
        for ln in lines:
            y = draw_wrapped(d, (MARGIN + 12, y), ln, f, INK, W - 2 * MARGIN - 12, 32)
            y += 8
        y += 18

    section("■ 統計データ（実カウント）", p["stats_sources"], C.BLUE)
    section("■ 法令・経緯（厚労省 確定素材）", p["law_sources"], C.RED)
    section("■ 推定（マクロ統計・補助）", p["estimate_note"], C.GRAY)
    footer(d, p["footer"], p["accent"])
    return img


RENDER = {
    "cover": render_cover,
    "fig": render_fig,
    "qa": render_qa,
    "sources": render_sources,
}


def main():
    out = "study_tgl_aerial_v2.pdf"
    assert not os.path.exists(out), f"{out} が既に存在（上書き禁止）。手動確認のこと。"
    pages = []
    for i, p in enumerate(PAGES_OR := C.PAGES, 1):
        fig = p.get("fig")
        if fig:
            assert os.path.exists(fig), f"fig MISSING: {fig}"
        pages.append(RENDER[p["kind"]](p))
        print(f"  p{i:>2} [{p['kind']}] rendered")
    pages[0].save(out, "PDF", resolution=150.0, save_all=True, append_images=pages[1:])
    print(f"OK -> {out}  ({len(pages)} pages, {os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
