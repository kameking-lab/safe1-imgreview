# -*- coding: utf-8 -*-
"""candidates_v14_interim.pdf : 中間版。完成分のみ収録。新規画像生成なし・既存ファイル読むだけ。
各機序: 見出し / 元絵(I-*) / 実事故(C-*: CSVファイル名+行番号+抜粋+型+起因物+年) / 確定写真(あれば01-03, 無ければ未完)。
表紙に中間版日付と完成数。末尾に出典一覧。"""
import os, re, glob
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
REFS = os.path.join(BASE, "refs")
V14 = os.path.join(BASE, "v14")
OUT_PDF = os.path.join(BASE, "candidates_v14_interim.pdf")
DATE = "2026-06-14"

PW, PH = 1240, 1754  # A4 portrait @ ~150dpi
M = 60
RED = (192, 57, 43)
INK = (25, 25, 25)
GRAY = (110, 110, 110)
BLUE = (11, 102, 195)

MECHS = [
    ("T1", "TGL 人が昇降板から墜落"),
    ("T2", "TGL 昇降板と荷台の間に頭部はさまれ"),
    ("T3", "TGL 後傾昇降板から荷(パネル)滑落で下敷き"),
    ("T4", "TGL 昇降板上でカゴ車倒れ激突"),
    ("T5", "TGL 降下中に足を地面との間にはさまれ"),
    ("A1", "高所 不整地で機体ごと後方転倒"),
    ("A2", "高所 作業床と上方構造物(梁/看板)で挟まれ"),
    ("A3", "高所 坂道逸走で車体と側溝に挟まれ"),
    ("A4", "高所 安全帯未使用で作業床から墜落"),
    ("A5", "高所 急動作で振られ墜落"),
]


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


FT = font(46)      # title
FH = font(34)      # section header
FL = font(27)      # label bold
FM = font(25, False)  # body
FS = font(22, False)  # small
FU = font(20, False)  # url/mono


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


def find_ref(mid):
    for ext in ("jpg", "png", "gif", "jpeg"):
        p = os.path.join(REFS, f"I-{mid}_ref.{ext}")
        if os.path.exists(p):
            return p
    return None


def load_rgb(p):
    im = Image.open(p)
    if getattr(im, "is_animated", False):
        im.seek(0)
    return im.convert("RGB")


def paste_fit(page, src_path, box):
    """box=(x,y,w,h); fit src inside, centered, with light border."""
    x, y, w, h = box
    d = ImageDraw.Draw(page)
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 245), outline=(210, 210, 210))
    try:
        im = load_rgb(src_path)
    except Exception:
        d.text((x + 12, y + 12), "(画像読込不可)", font=FS, fill=GRAY)
        return
    iw, ih = im.size
    s = min((w - 12) / iw, (h - 12) / ih)
    nw, nh = max(1, int(iw * s)), max(1, int(ih * s))
    im = im.resize((nw, nh), Image.LANCZOS)
    page.paste(im, (x + (w - nw) // 2, y + (h - nh) // 2))


def parse_case(mid):
    """Return dict with src(file:line), year, kata(型), kiin(起因物), excerpt from primary block."""
    p = os.path.join(REFS, f"C-{mid}_case.md")
    txt = open(p, encoding="utf-8").read()
    # limit to primary block: from first '## 採用事例' up to next '## 補強' / '## alternate'
    m = re.search(r"##\s*採用事例.*?(?=\n##\s)", txt, re.S)
    block = m.group(0) if m else txt

    def grab(label):
        mm = re.search(r"\*\*" + label + r"[^*]*\*\*[:：]\s*(.+)", block)
        return mm.group(1).strip() if mm else ""

    src = grab("引用元（ファイル名＋行番号）") or grab("引用元")
    year = grab("発生年")
    kata = grab("事故の型")
    kiin = grab("起因物")
    # excerpt: blockquote lines
    ex = [ln.strip()[1:].strip() for ln in block.splitlines() if ln.strip().startswith(">")]
    excerpt = " ".join(ex).strip()
    # clean src: keep `file` 行目(ID)
    src = src.replace("`", "")
    return {"src": src, "year": year, "kata": kata, "kiin": kiin, "excerpt": excerpt}


def photos(mid):
    return [os.path.join(V14, mid, f"{i:02d}.png") for i in (1, 2, 3)
            if os.path.exists(os.path.join(V14, mid, f"{i:02d}.png"))]


pages = []


def new_page():
    im = Image.new("RGB", (PW, PH), "white")
    return im, ImageDraw.Draw(im)


# ---------- COVER ----------
def cover():
    im, d = new_page()
    d.rectangle([0, 0, PW, 150], fill=RED)
    d.text((M, 46), "労働災害 機序別 参照資料（中間版）", font=FT, fill="white")
    y = 210
    done = sum(1 for mid, _ in MECHS if photos(mid))
    lines = [
        (f"中間版・{DATE} 時点", FH, INK),
        (f"写真 {done}/10 完成・残り{10-done}機序は生成中（後日確定）", FM, RED),
        ("", FS, INK),
        ("構成：機序ごとに〔元絵(公式事故図)〕→〔実在の死亡災害(出典=厚労省 死亡災害DB)〕", FM, INK),
        ("→〔確定写真 01-03（完成分のみ）〕。元絵の構図・力の向き・接触点・機種を厳守し写実写真化。", FM, INK),
        ("", FS, INK),
        ("実事故の出典：厚生労働省 死亡災害データベース（JNIOSH整形CSV, ROUSAIDB 2014-2018）。", FS, GRAY),
        ("各機序に〔CSVファイル名＋行番号＋災害発生状況の抜粋〕を明記（創作なし・生データ裏取り）。", FS, GRAY),
    ]
    for t, f, c in lines:
        if t == "":
            y += 24; continue
        for ln in wrap(d, t, f, PW - 2 * M):
            d.text((M, y), ln, font=f, fill=c); y += int(f.size * 1.5)
        y += 6
    # mechanism index
    y += 20
    d.text((M, y), "■ 収録機序", font=FL, fill=INK); y += 46
    for mid, name in MECHS:
        has = "写真01-03 ✓" if photos(mid) else "写真 未完(生成中)"
        d.text((M + 20, y), f"{mid}  {name}", font=FS, fill=INK)
        d.text((PW - M - d.textlength(has, font=FU) - 4, y + 2), has, font=FU,
               fill=((0, 130, 60) if photos(mid) else GRAY))
        y += 40
    d.text((M, PH - 70), "中間レビュー用・noindex・非公開URL。最終版で残り4機序の写真を追加予定。",
           font=FS, fill=GRAY)
    pages.append(im)


# ---------- INFO PAGE per mechanism ----------
def info_page(idx, mid, name):
    im, d = new_page()
    d.rectangle([0, 0, PW, 110], fill=RED)
    d.text((M, 30), f"{idx}. {mid}  {name}", font=FH, fill="white")
    y = 150
    # ref illustration
    d.text((M, y), "● 元絵（公式事故図 I-%s）" % mid, font=FL, fill=INK); y += 44
    ref = find_ref(mid)
    rh = 430
    if ref:
        paste_fit(im, ref, (M, y, PW - 2 * M, rh))
    y += rh + 30
    # accident
    c = parse_case(mid)
    d.text((M, y), "● 実事故（厚労省 死亡災害DB / C-%s）" % mid, font=FL, fill=INK); y += 46
    meta = f"引用元: {c['src']}"
    for ln in wrap(d, meta, FM, PW - 2 * M):
        d.text((M + 10, y), ln, font=FM, fill=BLUE); y += 36
    meta2 = f"発生年: {c['year']}　／　事故の型: {c['kata']}"
    for ln in wrap(d, meta2, FS, PW - 2 * M):
        d.text((M + 10, y), ln, font=FS, fill=INK); y += 32
    meta3 = f"起因物: {c['kiin']}"
    for ln in wrap(d, meta3, FS, PW - 2 * M):
        d.text((M + 10, y), ln, font=FS, fill=INK); y += 32
    y += 10
    d.text((M + 10, y), "災害発生状況（抜粋）:", font=FS, fill=GRAY); y += 36
    # excerpt box
    ex_lines = wrap(d, c["excerpt"], FM, PW - 2 * M - 40)
    box_h = len(ex_lines) * 38 + 30
    d.rectangle([M + 10, y, PW - M, y + box_h], fill=(248, 246, 240), outline=(220, 210, 190))
    yy = y + 14
    for ln in ex_lines:
        d.text((M + 26, yy), ln, font=FM, fill=(40, 30, 20)); yy += 38
    y += box_h + 24
    has = photos(mid)
    tag = "→ 確定写真は次ページ" if has else "→ 写真：未完（生成中につき後日）"
    d.text((M + 10, y), tag, font=FM, fill=((0, 110, 50) if has else GRAY))
    d.text((M, PH - 50), f"中間版 {DATE}　|　{mid}", font=FU, fill=GRAY)
    pages.append(im)


# ---------- PHOTO PAGE ----------
def photo_page(idx, mid, name):
    ph = photos(mid)
    if not ph:
        return
    im, d = new_page()
    d.rectangle([0, 0, PW, 110], fill=(0, 120, 60))
    d.text((M, 30), f"{idx}. {mid} 確定写真 01-03", font=FH, fill="white")
    y = 140
    labels = ["01 真横 (side)", "02 斜後 (rear-diagonal)", "03 ローアングル (low)"]
    cell_h = (PH - y - 60) // 3
    for i, p in enumerate(ph):
        d.text((M, y + 4), labels[i] if i < len(labels) else f"0{i+1}", font=FS, fill=INK)
        paste_fit(im, p, (M, y + 36, PW - 2 * M, cell_h - 46))
        y += cell_h
    d.text((M, PH - 46), f"中間版 {DATE}　|　{mid}　元絵の構図・力の向き・接触点・機種を厳守", font=FU, fill=GRAY)
    pages.append(im)


# ---------- SOURCES PAGE ----------
def sources_page():
    im, d = new_page()
    d.rectangle([0, 0, PW, 110], fill=RED)
    d.text((M, 30), "出典一覧（実事故の裏取り）", font=FH, fill="white")
    y = 160
    intro = ("実事故はすべて厚生労働省 死亡災害データベース（JNIOSH整形CSV, ROUSAIDB）の生データで裏取り。"
             "取得元: https://www.jniosh.johas.go.jp/publication/houkoku/houkoku_2022_01.html "
             "／ ローカル: data/jniosh/SHIBO_2014〜2018.csv（第7列=災害状況）。")
    for ln in wrap(d, intro, FM, PW - 2 * M):
        d.text((M, y), ln, font=FM, fill=INK); y += 38
    y += 16
    for mid, name in MECHS:
        c = parse_case(mid)
        d.text((M, y), f"{mid}  {name}", font=FL, fill=INK); y += 40
        d.text((M + 20, y), c["src"], font=FU, fill=BLUE); y += 32
        d.text((M + 20, y), f"型: {c['kata']}　起因物: {c['kiin']}　年: {c['year']}", font=FU, fill=GRAY)
        y += 44
    pages.append(im)


# ---------- BUILD ----------
cover()
for i, (mid, name) in enumerate(MECHS, 1):
    info_page(i, mid, name)
    photo_page(i, mid, name)
sources_page()

pages[0].save(OUT_PDF, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
print("WROTE", OUT_PDF, "pages=", len(pages))
