# -*- coding: utf-8 -*-
"""build_aerial2_catalog.py : aerial2_catalog.pdf を作成（BUILD）。
collect_aerial2/aerial2_index.csv と collect_aerial2/img/ の既存画像だけで作成
（新規画像生成なし・既存を読むだけ・非破壊）。
高所作業車の「事故・危険」イメージ画像を「通し番号付き一覧」のグリッドで掲載＝
後から番号で選べるカタログ。表紙（全件数・事故の型別・種別別）＋グリッド（1ページ6枚）。
各セル：サムネ・通し番号バッジ・[事故の型] 種別・状況メモ・出所ドメイン。
出力先 aerial2_catalog.pdf が既存なら上書きしない（中断＝破壊しない）。"""
import os, csv, sys
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
IMGDIR = os.path.join(BASE, "collect_aerial2", "img")
INDEX = os.path.join(BASE, "collect_aerial2", "aerial2_index.csv")
OUT_PDF = os.path.join(BASE, "aerial2_catalog.pdf")
DATE = "2026-06-25"

PW, PH = 1240, 1754
M = 54
RED = (192, 57, 43)
INK = (25, 25, 25)
GRAY = (110, 110, 110)
BLUE = (11, 102, 195)

# 事故の型ごとの色（バッジ用）
CATCOL = {
    "墜落・転落": (200, 60, 40),
    "挟まれ・巻き込まれ": (170, 70, 160),
    "転倒・横転": (200, 120, 0),
    "感電": (30, 90, 170),
    "飛来落下": (0, 130, 130),
    "不安全行動": (120, 100, 0),
    "その他": (100, 100, 100),
}

COLS, ROWS = 2, 3          # 6 per page
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


FT = font(46); FH = font(32); FL = font(30); FM = font(26, False)
FS = font(22, False); FU = font(19, False); FNUM = font(32)


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

    def keyfn(r):
        try:
            return int(r.get("通し番号", "0"))
        except Exception:
            return 0
    rows.sort(key=keyfn)
    return rows


def domain(r):
    dm = r.get("出所ドメイン", "")
    if dm:
        return dm
    try:
        return urlparse(r.get("出所URL", "")).netloc or ""
    except Exception:
        return ""


pages = []


def cover(rows):
    n = len(rows)
    cats, kinds = {}, {}
    for r in rows:
        cats[r.get("カテゴリ", "?")] = cats.get(r.get("カテゴリ", "?"), 0) + 1
        kinds[r.get("種別", "?")] = kinds.get(r.get("種別", "?"), 0) + 1
    im, d = new_page()
    d.rectangle([0, 0, PW, 150], fill=RED)
    d.text((M, 46), "高所作業車 事故・危険イメージ カタログ", font=FT, fill="white")
    y = 205
    lines = [
        (f"{DATE}　/　全 {n} 点（通し番号で選べる一覧）", FH, INK),
        ("", FS, INK),
        ("ブーム式／垂直昇降式／シザース／トラック搭載型の高所作業車の", FM, INK),
        ("『事故・ヒヤリハット・危険行動』を表す画像（教育用・架空も含む）を収集。", FM, INK),
        ("事故の型は不問：墜落・転落／挟まれ・巻き込まれ／転倒・横転／感電／飛来落下／不安全行動 等。", FS, GRAY),
        ("機種カタログの完成写真・構造/部品名称図・通常作業のみは除外。md5で重複排除済み。", FS, GRAY),
        ("画像生成は一切なし。各画像の出所URLは collect_aerial2/aerial2_index.csv に全件記録。", FS, GRAY),
    ]
    for t, f, c in lines:
        if t == "":
            y += 16; continue
        for ln in wrap(d, t, f, PW - 2 * M):
            d.text((M, y), ln, font=f, fill=c); y += int(f.size * 1.5)
        y += 6
    y += 18
    d.text((M, y), "■ 事故の型別", font=FL, fill=INK); y += 50
    for k, v in sorted(cats.items(), key=lambda kv: -kv[1]):
        col = CATCOL.get(k, INK)
        d.text((M + 20, y), f"● {k}： {v} 点", font=FM, fill=col); y += 40
    y += 18
    d.text((M, y), "■ 種別別", font=FL, fill=INK); y += 50
    for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]):
        d.text((M + 20, y), f"・{k}： {v} 点", font=FS, fill=INK); y += 34
    d.text((M, PH - 60), "限定共有用・noindex・非公開。詳細(出所URL/md5/状況メモ)は collect_aerial2/aerial2_index.csv。",
           font=FS, fill=GRAY)
    pages.append(im)


def grid_pages(rows):
    cell_w = (PW - 2 * M - (COLS - 1) * 28) // COLS
    cell_h = (PH - 150 - 60 - (ROWS - 1) * 26) // ROWS
    img_h = cell_h - 120
    total_pages = (len(rows) + PER - 1) // PER
    for pi in range(total_pages):
        im, d = new_page()
        d.rectangle([0, 0, PW, 110], fill=RED)
        d.text((M, 30), "高所作業車 事故・危険 一覧（通し番号で選択）", font=FH, fill="white")
        d.text((PW - M - 230, 60), f"page {pi+1}/{total_pages}", font=FU, fill="white")
        for idx in range(PER):
            gi = pi * PER + idx
            if gi >= len(rows):
                break
            r = rows[gi]
            cr, cc = divmod(idx, COLS)
            x = M + cc * (cell_w + 28)
            y = 140 + cr * (cell_h + 26)
            no = r.get("通し番号", "")
            cat = r.get("カテゴリ", "")
            catcol = CATCOL.get(cat, GRAY)
            d.rectangle([x, y, x + cell_w, y + img_h + 4], outline=(214, 214, 214))
            paste_fit(im, os.path.join(IMGDIR, r["ファイル名"]),
                      (x, y, cell_w, img_h))
            # 通し番号バッジ（左上）
            tw = d.textlength(f"No.{no}", font=FNUM) + 18
            d.rectangle([x, y, x + tw, y + 42], fill=catcol)
            d.text((x + 9, y + 4), f"No.{no}", font=FNUM, fill="white")
            ty = y + img_h + 12
            badge = f"[{cat}] {r.get('種別','')}"
            for ln in wrap(d, badge, FS, cell_w)[:1]:
                d.text((x + 2, ty), ln, font=FS, fill=catcol); ty += 30
            memo = r.get("状況メモ", "")
            for ln in wrap(d, memo, FU, cell_w)[:2]:
                d.text((x + 2, ty), ln, font=FU, fill=INK); ty += 26
            dm = domain(r)
            if dm:
                for ln in wrap(d, "出所: " + dm, FU, cell_w)[:1]:
                    d.text((x + 2, ty), ln, font=FU, fill=BLUE)
        d.text((M, PH - 44), f"高所作業車 事故・危険イメージカタログ {DATE}　|　全{len(rows)}点",
               font=FU, fill=GRAY)
        pages.append(im)


def main():
    if not os.path.exists(INDEX):
        print("ERROR: index not found", INDEX); sys.exit(1)
    if os.path.exists(OUT_PDF):
        print("EXISTS: aerial2_catalog.pdf already present; not overwriting. Abort.")
        sys.exit(0)
    rows = load_rows()
    print("rows=", len(rows))
    cover(rows)
    grid_pages(rows)
    pages[0].save(OUT_PDF, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
    print("WROTE", OUT_PDF, "pages=", len(pages), "imgs=", len(rows))


if __name__ == "__main__":
    main()
