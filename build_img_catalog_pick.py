# -*- coding: utf-8 -*-
"""img_catalog_pick.pdf — イラスト選抜用の通し番号付き一覧。
6枚/ページのグリッド、各サムネ直下に【通し番号】【カテゴリ】【事故種類】【出所ドメイン】。
TGLセクション→高所セクションの順、通し番号順で全73枚。GIFは1フレーム目。表示不可は明示。
既存(collect2/img/・img_index.csv)を読むだけ。新規生成・破壊なし。"""
import os, csv
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
IMGDIR = os.path.join(BASE, "collect2", "img")
CSVP = os.path.join(BASE, "collect2", "img_index.csv")
OUT = os.path.join(BASE, "img_catalog_pick.pdf")
DATE = "2026-06-14"

PW, PH = 1240, 1754
M = 60
RED = (192, 57, 43); INK = (25, 25, 25); GRAY = (110, 110, 110)
BLUE = (11, 102, 195); GREEN = (0, 120, 60); TGLC = (30, 90, 170); AERC = (200, 110, 0)


def font(sz, b=True):
    cands = ([r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc"]
             if b else [r"C:\Windows\Fonts\YuGothR.ttc", r"C:\Windows\Fonts\meiryo.ttc"])
    for p in cands:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


FT = font(44); FH = font(30); FL = font(26); FM = font(23, False)
FS = font(21, False); FU = font(19, False); FN = font(24)


def wrap(d, t, f, mw):
    out, c = [], ""
    for ch in t:
        if d.textlength(c + ch, font=f) <= mw:
            c += ch
        else:
            out.append(c); c = ch
    if c:
        out.append(c)
    return out


# ---- load rows ----
rows = list(csv.reader(open(CSVP, encoding="utf-8-sig")))
hdr = rows[0]
data = [r for r in rows[1:] if len(r) >= 5 and r[0].strip()]
# columns: 0=num 1=file 2=cat 3=type 4=url 5=md5 6=desc
data.sort(key=lambda r: r[0])
tgl = [r for r in data if r[2].strip() == "TGL"]
aer = [r for r in data if r[2].strip() != "TGL"]

pages = []


def new_page():
    im = Image.new("RGB", (PW, PH), "white")
    return im, ImageDraw.Draw(im)


def domain(url):
    try:
        n = urlparse(url.strip()).netloc
        return n or url.strip()[:40]
    except Exception:
        return url.strip()[:40]


def load_thumb(fn):
    p = os.path.join(IMGDIR, fn)
    if not os.path.exists(p):
        return None
    try:
        im = Image.open(p)
        if getattr(im, "is_animated", False):
            im.seek(0)
        return im.convert("RGB")
    except Exception:
        return None


# ---------- COVER ----------
def cover():
    im, d = new_page()
    d.rectangle([0, 0, PW, 150], fill=RED)
    d.text((M, 44), "事故イラスト 選抜用 一覧（通し番号付き）", font=FT, fill="white")
    y = 200
    d.text((M, y), f"{DATE} ／ 全 {len(data)} 点（TGL {len(tgl)} ・ 高所 {len(aer)}）", font=FH, fill=INK)
    y += 64
    # 使い方
    d.rectangle([M, y, PW - M, y + 200], fill=(248, 246, 240), outline=(214, 200, 175))
    d.text((M + 24, y + 20), "■ 使い方", font=FL, fill=RED)
    uses = [
        "1. 各サムネイル直下の【4桁の通し番号】が画像のID（collect2/img/0001.jpg …）です。",
        "2. 採用したい番号を控えてください（例：0007, 0041 …）。番号でそのまま指定できます。",
        "3. 各サムネには 通し番号／カテゴリ(TGL・高所)／事故種類／出所ドメイン を併記しています。",
        "4. 並び順＝TGLセクション→高所セクション、いずれも通し番号順で全点掲載。",
    ]
    yy = y + 64
    for t in uses:
        for ln in wrap(d, t, FM, PW - 2 * M - 48):
            d.text((M + 24, yy), ln, font=FM, fill=INK); yy += 32
    y += 230
    d.text((M, y), "■ カテゴリ別", font=FL, fill=INK); y += 44
    d.text((M + 20, y), f"● TGL（テールゲートリフター付きトラック）: {len(tgl)} 点（0001〜）", font=FS, fill=TGLC)
    y += 36
    d.text((M + 20, y), f"● 高所作業車: {len(aer)} 点（{aer[0][0] if aer else '----'}〜）", font=FS, fill=AERC)
    y += 60
    d.text((M, y), "GIFは1フレーム目を描画。読み込めない画像は「#番号 表示不可」と明示します。", font=FS, fill=GRAY)
    d.text((M, PH - 70), "限定共有・noindex・非公開。画像生成なし（収集物の表示のみ）。出所URL全文は collect2/img_index.csv。",
           font=FU, fill=GRAY)
    pages.append(im)


# ---------- GRID ----------
COLS, ROWS = 2, 3              # 6 per page
PERPAGE = COLS * ROWS
GAP = 30
CELL_W = (PW - 2 * M - GAP * (COLS - 1)) // COLS
TOP = 130
CELL_H = (PH - TOP - 60 - GAP * (ROWS - 1)) // ROWS
CAP_H = 132
IMG_H = CELL_H - CAP_H


def grid_section(label, items, catcol):
    for pi in range(0, len(items), PERPAGE):
        chunk = items[pi:pi + PERPAGE]
        im, d = new_page()
        d.rectangle([0, 0, PW, 96], fill=catcol)
        rng = f"{chunk[0][0]}〜{chunk[-1][0]}"
        d.text((M, 26), f"{label}（{rng}） 通し番号付き・選抜用", font=FH, fill="white")
        for idx, r in enumerate(chunk):
            cx = M + (idx % COLS) * (CELL_W + GAP)
            cy = TOP + (idx // COLS) * (CELL_H + GAP)
            num, fn, cat, typ, url = r[0], r[1], r[2].strip(), r[3].strip(), r[4]
            catj = "TGL" if cat == "TGL" else "高所"
            # image frame
            d.rectangle([cx, cy, cx + CELL_W, cy + IMG_H], fill=(244, 244, 244), outline=(205, 205, 205))
            th = load_thumb(fn)
            if th is None:
                d.text((cx + 16, cy + IMG_H // 2 - 14), f"#{num} 表示不可", font=FL, fill=RED)
            else:
                iw, ih = th.size
                s = min((CELL_W - 12) / iw, (IMG_H - 12) / ih)
                nw, nh = max(1, int(iw * s)), max(1, int(ih * s))
                th = th.resize((nw, nh), Image.LANCZOS)
                im.paste(th, (cx + (CELL_W - nw) // 2, cy + (IMG_H - nh) // 2))
            # caption
            ty = cy + IMG_H + 8
            # number badge + category
            d.rectangle([cx, ty, cx + 132, ty + 34], fill=catcol)
            d.text((cx + 8, ty + 4), f"No.{num}", font=FN, fill="white")
            d.text((cx + 144, ty + 4), f"[{catj}]", font=FL, fill=catcol)
            ty += 42
            for ln in wrap(d, f"事故種類: {typ}", FS, CELL_W - 8)[:1]:
                d.text((cx + 2, ty), ln, font=FS, fill=INK); ty += 28
            for ln in wrap(d, f"出所: {domain(url)}", FU, CELL_W - 8)[:1]:
                d.text((cx + 2, ty), ln, font=FU, fill=BLUE); ty += 26
        d.text((M, PH - 44), f"選抜用一覧 {DATE} ／ {label}", font=FU, fill=GRAY)
        pages.append(im)


cover()
grid_section("TGLセクション", tgl, TGLC)
grid_section("高所作業車セクション", aer, AERC)

pages[0].save(OUT, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
print("WROTE", OUT, "pages=", len(pages), "imgs=", len(data), "TGL=", len(tgl), "AER=", len(aer))
