# -*- coding: utf-8 -*-
"""build_img_catalog_c1.py : img_catalog.pdf を作成（C1）。
collect2/img_index.csv と collect2/img/ の既存イラストだけで作成（新規画像生成なし・既存を読むだけ）。
全イラストを「通し番号付き一覧」のグリッドで掲載＝後から番号で選べるカタログ。
表紙＋カテゴリ別件数＋グリッド（各セル：サムネ・通し番号・カテゴリ・事故種類・1行説明・出所ドメイン）。
出力先 img_catalog.pdf が既存なら上書きしない（別名で退避して中断＝破壊しない）。"""
import os, csv, sys
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
IMGDIR = os.path.join(BASE, "collect2", "img")
INDEX = os.path.join(BASE, "collect2", "img_index.csv")
OUT_PDF = os.path.join(BASE, "img_catalog.pdf")
DATE = "2026-06-14"

PW, PH = 1240, 1754
M = 54
RED = (192, 57, 43)
INK = (25, 25, 25)
GRAY = (110, 110, 110)
BLUE = (11, 102, 195)
GREEN = (0, 120, 60)
TGLC = (30, 90, 170)
AERC = (200, 110, 0)

COLS, ROWS = 3, 4          # 12 per page
PER = COLS * ROWS


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


FT = font(46); FH = font(32); FL = font(27); FM = font(24, False)
FS = font(20, False); FU = font(17, False); FNUM = font(30)


def wrap(d, t, f, mw):
    out, c = [], ""
    for ch in t:
        if ch == "\n":
            out.append(c); c = ""; continue
        if d.textlength(c + ch, font=f) <= mw:
            c += ch
        else:
            out.append(c); c = ch
    if c:
        out.append(c)
    return out


def new_page():
    im = Image.new("RGB", (PW, PH), "white")
    return im, ImageDraw.Draw(im)


def paste_fit(page, src, box):
    x, y, w, h = box
    d = ImageDraw.Draw(page)
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 245), outline=(214, 214, 214))
    try:
        im = Image.open(src)
        if getattr(im, "is_animated", False):
            im.seek(0)
        im = im.convert("RGB")
    except Exception:
        d.text((x + 10, y + 10), "(画像読込不可)", font=FU, fill=GRAY); return
    iw, ih = im.size
    s = min((w - 8) / iw, (h - 8) / ih)
    nw, nh = max(1, int(iw * s)), max(1, int(ih * s))
    page.paste(im.resize((nw, nh), Image.LANCZOS), (x + (w - nw) // 2, y + (h - nh) // 2))


def load_rows():
    rows = []
    with open(INDEX, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r = {k.strip(): (v or "").strip() for k, v in r.items()}
            if r.get("ファイル名"):
                rows.append(r)
    rows.sort(key=lambda r: r.get("通し番号", ""))
    return rows


def domain(url):
    try:
        return urlparse(url).netloc or ""
    except Exception:
        return ""


pages = []


def cover(rows):
    n = len(rows)
    cats = {}
    kinds = {}
    for r in rows:
        cats[r.get("カテゴリ", "?")] = cats.get(r.get("カテゴリ", "?"), 0) + 1
        kinds[r.get("事故種類", "?")] = kinds.get(r.get("事故種類", "?"), 0) + 1
    im, d = new_page()
    d.rectangle([0, 0, PW, 150], fill=RED)
    d.text((M, 46), "事故イラスト カタログ（通し番号付き一覧）", font=FT, fill="white")
    y = 205
    lines = [
        (f"{DATE}　/　全 {n} 点（後から通し番号で選べる一覧）", FH, INK),
        ("", FS, INK),
        ("TGL付きトラック／高所作業車の『事故イラスト・事故が写った図/写真』を収集。", FM, INK),
        ("墜落・転落／はさまれ・巻き込まれ／激突／崩壊・倒壊／感電 等、事故種類は不問。", FM, INK),
        ("通常作業のみ・構造/部品名称図・無関係な単体写真は除外。md5(＋実目視)で重複排除済み。", FS, GRAY),
        ("画像生成は一切なし。各イラストの出所URLは collect2/img_index.csv に全件記録。", FS, GRAY),
    ]
    for t, f, c in lines:
        if t == "":
            y += 16; continue
        for ln in wrap(d, t, f, PW - 2 * M):
            d.text((M, y), ln, font=f, fill=c); y += int(f.size * 1.5)
        y += 6
    y += 18
    d.text((M, y), "■ カテゴリ別", font=FL, fill=INK); y += 46
    for k in ("TGL", "高所"):
        if k in cats:
            col = TGLC if k == "TGL" else AERC
            label = "TGL（テールゲートリフター付きトラック）" if k == "TGL" else "高所作業車"
            d.text((M + 20, y), f"● {label}： {cats[k]} 点", font=FM, fill=col); y += 40
    for k, v in sorted(cats.items()):
        if k not in ("TGL", "高所"):
            d.text((M + 20, y), f"● {k}： {v} 点", font=FM, fill=INK); y += 40
    y += 18
    d.text((M, y), "■ 事故種類別", font=FL, fill=INK); y += 46
    for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]):
        d.text((M + 20, y), f"・{k}： {v} 点", font=FS, fill=INK); y += 32
    d.text((M, PH - 60), "限定共有用・noindex・非公開。詳細(出所URL/md5/説明)は collect2/img_index.csv。",
           font=FS, fill=GRAY)
    pages.append(im)


def grid_pages(rows):
    cell_w = (PW - 2 * M - (COLS - 1) * 24) // COLS
    cell_h = (PH - 150 - 60 - (ROWS - 1) * 22) // ROWS
    img_h = cell_h - 132
    total_pages = (len(rows) + PER - 1) // PER
    for pi in range(total_pages):
        im, d = new_page()
        d.rectangle([0, 0, PW, 110], fill=RED)
        d.text((M, 30), "事故イラスト 一覧（通し番号で選択）", font=FH, fill="white")
        d.text((PW - M - 220, 60), f"page {pi+1}/{total_pages}", font=FU, fill="white")
        for idx in range(PER):
            gi = pi * PER + idx
            if gi >= len(rows):
                break
            r = rows[gi]
            cr, cc = divmod(idx, COLS)
            x = M + cc * (cell_w + 24)
            y = 140 + cr * (cell_h + 22)
            # number badge
            no = r.get("通し番号", "")
            cat = r.get("カテゴリ", "")
            catcol = TGLC if cat == "TGL" else (AERC if cat == "高所" else GRAY)
            d.rectangle([x, y, x + cell_w, y + img_h + 4],
                        outline=(214, 214, 214))
            paste_fit(im, os.path.join(IMGDIR, r["ファイル名"]),
                      (x, y, cell_w, img_h))
            # number tag (top-left)
            tw = d.textlength(f"No.{no}", font=FNUM) + 18
            d.rectangle([x, y, x + tw, y + 40], fill=catcol)
            d.text((x + 9, y + 4), f"No.{no}", font=FNUM, fill="white")
            ty = y + img_h + 12
            badge = f"[{cat}] {r.get('事故種類','')}"
            for ln in wrap(d, badge, FS, cell_w)[:1]:
                d.text((x + 2, ty), ln, font=FS, fill=catcol); ty += 28
            desc = r.get("説明", "")
            for ln in wrap(d, desc, FU, cell_w)[:2]:
                d.text((x + 2, ty), ln, font=FU, fill=INK); ty += 24
            dm = domain(r.get("出所URL", ""))
            if dm:
                for ln in wrap(d, "出所: " + dm, FU, cell_w)[:1]:
                    d.text((x + 2, ty), ln, font=FU, fill=BLUE)
        d.text((M, PH - 44), f"事故イラストカタログ {DATE}　|　全{len(rows)}点",
               font=FU, fill=GRAY)
        pages.append(im)


def main():
    if not os.path.exists(INDEX):
        print("ERROR: index not found", INDEX); sys.exit(1)
    if os.path.exists(OUT_PDF):
        print("EXISTS: img_catalog.pdf already present; not overwriting. Abort.")
        sys.exit(0)
    rows = load_rows()
    print("rows=", len(rows))
    cover(rows)
    grid_pages(rows)
    pages[0].save(OUT_PDF, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
    print("WROTE", OUT_PDF, "pages=", len(pages), "imgs=", len(rows))


if __name__ == "__main__":
    main()
