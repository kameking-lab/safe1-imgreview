# -*- coding: utf-8 -*-
"""refs2_catalog_interim.pdf : 元絵カタログ中間版。refs2/ に今ある採用イラストだけで作成。
新規画像生成なし・既存ファイル読むだけ。カテゴリ[TGL/高所]→スロット→採用イラスト最大3点を大きく
＋〔出所URL〕〔何の事故か〕〔3要素チェック〕。未探索=「未探索」、該当なし=「該当イラストなし/置換」。"""
import os, re, glob
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
R2 = os.path.join(BASE, "refs2")
OUT_PDF = os.path.join(BASE, "refs2_catalog_interim.pdf")
DATE = "2026-06-14"

PW, PH = 1240, 1754
M = 60
RED = (192, 57, 43)
INK = (25, 25, 25)
GRAY = (110, 110, 110)
BLUE = (11, 102, 195)
GREEN = (0, 120, 60)
TGLC = (30, 90, 170)
AERC = (200, 110, 0)

SLOTS = [
    ("TGL", "RT1", "人が昇降板から墜落"),
    ("TGL", "RT2", "昇降板と荷台/車体の間に頭部・上半身はさまれ"),
    ("TGL", "RT3", "後傾/傾斜で荷(パネル等)が昇降板から滑落・下敷き"),
    ("TGL", "RT4", "昇降板上でカゴ車/台車が倒れ激突"),
    ("TGL", "RT5", "昇降板降下中に手足を地面・床との間にはさまれ"),
    ("TGL", "RT6", "荷を載せた台車ごと昇降板から転落"),
    ("TGL", "RT7", "昇降板の誤操作で被災"),
    ("TGL", "RT8", "段差で台車が逸走・転倒"),
    ("TGL", "RT9", "重量物で昇降板が耐えられず落下"),
    ("TGL", "RT10", "その他TGL起因の死傷（見つかったもの）"),
    ("AER", "RA1", "不整地/傾斜で機体ごと転倒・搭乗者投げ出され"),
    ("AER", "RA2", "作業床と上方構造物(梁/看板/天井)で挟まれ"),
    ("AER", "RA3", "坂道逸走で車体と障害物(側溝/壁)に挟まれ"),
    ("AER", "RA4", "安全帯未使用で作業床から墜落"),
    ("AER", "RA5", "急動作/操作ミスで搭乗者が振られ墜落"),
    ("AER", "RA6", "ブーム/作業床が電線に接触・感電"),
    ("AER", "RA7", "アウトリガー未設置/不良で転倒"),
    ("AER", "RA8", "走行中の段差/穴で転倒"),
    ("AER", "RA9", "積載超過/無理姿勢で転倒"),
    ("AER", "RA10", "その他高所作業車起因の死傷（見つかったもの）"),
]

# slots the runner has explicitly finished ([x] in BACKLOG_REF); RT5 is in progress.
DONE = {"RT1", "RT2", "RT3", "RT4"}
INPROGRESS = "RT5"


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
FS = font(21, False); FU = font(19, False)


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


def slot_imgs(sid):
    fs = []
    for i in (1, 2, 3):
        for ext in ("jpg", "jpeg", "png", "gif"):
            p = os.path.join(R2, sid, f"{i:02d}.{ext}")
            if os.path.exists(p):
                fs.append(p); break
    return fs


def parse_md(sid):
    """Return (adopted_count_text, status, {filename: {url, what, three}}) from refs2/{sid}.md."""
    p = os.path.join(R2, f"{sid}.md")
    if not os.path.exists(p):
        return None, "未探索", {}
    txt = open(p, encoding="utf-8").read()
    head = ""
    mm = re.search(r"採用枚数[:：]\s*(.+)", txt)
    if mm:
        head = mm.group(1).strip()
    status = "該当なし" if ("該当イラスト=**なし**" in txt or "該当イラストなし" in txt or
                          re.search(r"採用枚数[:：]\s*0", txt)) else "あり"
    secs = {}
    for m in re.finditer(r"^##\s+(\S+\.(?:jpg|jpeg|png|gif))\s*$(.*?)(?=^##\s|\Z)",
                         txt, re.S | re.M):
        fn, body = m.group(1), m.group(2)
        url = re.search(r"〔出所URL〕\s*(\S+)", body)
        what = re.search(r"〔何の事故か〕\s*(.+)", body)
        three = re.search(r"〔3要素チェック〕\s*(.+)", body)
        secs[fn] = {
            "url": url.group(1).strip() if url else "",
            "what": what.group(1).strip() if what else "",
            "three": three.group(1).strip() if three else "",
        }
    return head, status, secs


pages = []


def new_page():
    im = Image.new("RGB", (PW, PH), "white")
    return im, ImageDraw.Draw(im)


def paste_fit(page, src, box):
    x, y, w, h = box
    d = ImageDraw.Draw(page)
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 245), outline=(210, 210, 210))
    try:
        im = Image.open(src)
        if getattr(im, "is_animated", False):
            im.seek(0)
        im = im.convert("RGB")
    except Exception:
        d.text((x + 12, y + 12), "(画像読込不可)", font=FS, fill=GRAY); return
    iw, ih = im.size
    s = min((w - 12) / iw, (h - 12) / ih)
    nw, nh = max(1, int(iw * s)), max(1, int(ih * s))
    page.paste(im.resize((nw, nh), Image.LANCZOS), (x + (w - nw) // 2, y + (h - nh) // 2))


# ----- counts for cover -----
n_adopt_slot = sum(1 for c, s, n in SLOTS if slot_imgs(s))
n_imgs = sum(len(slot_imgs(s)) for c, s, n in SLOTS)
n_explored = len([s for c, s, n in SLOTS if s in DONE])
n_nomatch = sum(1 for c, s, n in SLOTS if (not slot_imgs(s)) and parse_md(s)[1] == "該当なし")


def cover():
    im, d = new_page()
    d.rectangle([0, 0, PW, 150], fill=RED)
    d.text((M, 46), "元絵カタログ（中間版）", font=FT, fill="white")
    y = 210
    lines = [
        (f"中間版・{DATE}　/　採用 {n_adopt_slot} スロット・探索済 {n_explored}/22", FH, INK),
        (f"採用イラスト総数 {n_imgs} 点（うち1点はRT1/RT3で重複・md5一致を明記）・該当なし {n_nomatch} スロット（RT2）", FM, INK),
        ("", FS, INK),
        ("TGL付きトラック／高所作業車の『事故イラスト』(3要素=機械＋事故の事象＋被災者を満たす絵)を収集。", FM, INK),
        ("通常作業・構造/部品名称図・単体写真・汎用転落ピクトは採用禁止。無理な当てはめはしない。", FM, INK),
        ("画像生成は一切なし。ブラウザ画像検索→当方で実目視し3要素で判定したもののみ採用。", FS, GRAY),
    ]
    for t, f, c in lines:
        if t == "":
            y += 22; continue
        for ln in wrap(d, t, f, PW - 2 * M):
            d.text((M, y), ln, font=f, fill=c); y += int(f.size * 1.5)
        y += 6
    y += 16
    d.text((M, y), "■ 凡例", font=FL, fill=INK); y += 44
    for t, c in [("採用◯点：3要素を満たす事故イラストを採用", GREEN),
                 ("該当イラストなし：規定どおり無理に当てない（置換は今後判断）", RED),
                 ("着手中：本サイクルで探索中（次サイクルで確定）", AERC),
                 ("未探索：未着手", GRAY)]:
        d.text((M + 20, y), "● " + t, font=FS, fill=c); y += 38
    d.text((M, PH - 70), "中間レビュー用・noindex・非公開URL。最終版で全22スロットを確定予定。",
           font=FS, fill=GRAY)
    pages.append(im)


def status_page():
    im, d = new_page()
    d.rectangle([0, 0, PW, 110], fill=RED)
    d.text((M, 30), "スロット別 進捗一覧（全20スロット）", font=FH, fill="white")
    y = 150
    for cat, sid, name in SLOTS:
        imgs = slot_imgs(sid)
        if imgs:
            tag, col = f"採用 {len(imgs)}点", GREEN
        elif sid == INPROGRESS:
            tag, col = "着手中", AERC
        elif parse_md(sid)[1] == "該当なし":
            tag, col = "該当イラストなし", RED
        else:
            tag, col = "未探索", GRAY
        catcol = TGLC if cat == "TGL" else AERC
        d.text((M, y), f"[{cat}]", font=FU, fill=catcol)
        d.text((M + 80, y), f"{sid}", font=FL, fill=INK)
        for ln in wrap(d, name, FS, PW - M - 360):
            d.text((M + 200, y + 2), ln, font=FS, fill=INK); break
        d.text((PW - M - d.textlength(tag, font=FL) - 4, y), tag, font=FL, fill=col)
        y += 46
    d.text((M, PH - 50), f"中間版 {DATE}", font=FU, fill=GRAY)
    pages.append(im)


def cat_divider(cat):
    im, d = new_page()
    col = TGLC if cat == "TGL" else AERC
    d.rectangle([0, PH // 2 - 120, PW, PH // 2 + 120], fill=col)
    label = "カテゴリ：TGL（テールゲートリフター付きトラック）" if cat == "TGL" \
        else "カテゴリ：高所作業車"
    d.text((M, PH // 2 - 28), label, font=FH, fill="white")
    pages.append(im)


def slot_detail(cat, sid, name, imgs, secs):
    catcol = TGLC if cat == "TGL" else AERC
    # paginate: 2 image-cards per page
    per = 2
    chunks = [imgs[i:i + per] for i in range(0, len(imgs), per)] or [[]]
    for pi, chunk in enumerate(chunks):
        im, d = new_page()
        d.rectangle([0, 0, PW, 112], fill=catcol)
        ttl = f"{sid}  {name}"
        d.text((M, 18), ttl if d.textlength(ttl, font=FL) < PW - 2 * M else sid + " " + name[:22] + "…",
               font=FL, fill="white")
        d.text((M, 66), f"[{cat}] 採用{len(imgs)}点（事故イラスト＝あり）" +
               (f"  ({pi+1}/{len(chunks)})" if len(chunks) > 1 else ""), font=FU, fill="white")
        y = 140
        card_h = (PH - y - 60) // per
        for p in chunk:
            fn = os.path.basename(p)
            meta = secs.get(fn, {})
            img_h = card_h - 200
            paste_fit(im, p, (M, y, PW - 2 * M, img_h))
            ty = y + img_h + 10
            d.text((M, ty), f"● {fn}", font=FS, fill=INK); ty += 32
            url = meta.get("url", "")
            if url:
                for ln in wrap(d, "出所: " + url, FU, PW - 2 * M):
                    d.text((M, ty), ln, font=FU, fill=BLUE); ty += 26
            what = meta.get("what", "")
            if what:
                for ln in wrap(d, "事故: " + what, FS, PW - 2 * M)[:2]:
                    d.text((M, ty), ln, font=FS, fill=INK); ty += 28
            three = meta.get("three", "")
            if three:
                for ln in wrap(d, "3要素: " + three, FS, PW - 2 * M)[:1]:
                    d.text((M, ty), ln, font=FS, fill=GREEN); ty += 28
            y += card_h
        d.text((M, PH - 46), f"中間版 {DATE}　|　{sid}", font=FU, fill=GRAY)
        pages.append(im)


def slot_nomatch(cat, sid, name):
    catcol = TGLC if cat == "TGL" else AERC
    im, d = new_page()
    d.rectangle([0, 0, PW, 112], fill=catcol)
    d.text((M, 18), f"{sid}  {name}", font=FL, fill="white")
    d.text((M, 66), f"[{cat}]", font=FU, fill="white")
    y = 200
    d.rectangle([M, y, PW - M, y + 120], fill=(253, 236, 234), outline=RED)
    d.text((M + 30, y + 38), "該当イラストなし（事故イラスト/事故写真が見つからず）", font=FH, fill=RED)
    y += 170
    head, status, _ = parse_md(sid)
    note = ("収集候補（237点）を実目視したが、3要素(機械=TGL／事象=板と車体の間に頭部・上半身はさまれ／"
            "被災者)を同時に満たす事故イラストは皆無。TGLの絵は通常作業・解説・構造図・製品写真のみ、"
            "『はさまれ』の絵はTGL不在の汎用ピクトor別機械(フォークリフト/塵芥車/吊荷)であった。"
            "規定どおり無理な当てはめはせず該当なしを明記。置換は最終カタログ段階で判断する。")
    for ln in wrap(d, note, FM, PW - 2 * M):
        d.text((M, y), ln, font=FM, fill=INK); y += 38
    d.text((M, PH - 46), f"中間版 {DATE}　|　{sid}　詳細: refs2/{sid}.md", font=FU, fill=GRAY)
    pages.append(im)


# ----- build -----
cover()
status_page()
cur_cat = None
for cat, sid, name in SLOTS:
    if cat != cur_cat:
        cat_divider(cat); cur_cat = cat
    imgs = slot_imgs(sid)
    head, status, secs = parse_md(sid)
    if imgs:
        slot_detail(cat, sid, name, imgs, secs)
    elif status == "該当なし":
        slot_nomatch(cat, sid, name)
    # 未探索/着手中 slots: covered on status_page only (kept compact)

pages[0].save(OUT_PDF, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
print("WROTE", OUT_PDF, "pages=", len(pages),
      "| adopt_slots=", n_adopt_slot, "imgs=", n_imgs, "explored=", n_explored, "nomatch=", n_nomatch)
