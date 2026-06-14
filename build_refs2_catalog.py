# -*- coding: utf-8 -*-
"""build_refs2_catalog.py : refs2_catalog.pdf（最終版）を作成。
refs2/ に今ある採用イラスト（01..03）と refs2/{SID}.md のメタだけで作成。新規画像生成なし・既存読むだけ。
カテゴリ[TGL/高所]→スロット→採用イラストを大きく＋〔出所URL〕〔何の事故か〕〔3要素チェック〕。
各スロットに採用枚数と「該当なし/置換」を明記。md は2形式（〔〕表記 / コロン表記・##/###）両対応。"""
import os, re
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
R2 = os.path.join(BASE, "refs2")
OUT_PDF = os.path.join(BASE, "refs2_catalog.pdf")
DATE = "2026-06-14"

PW, PH = 1240, 1754
M = 60
RED = (192, 57, 43)
INK = (25, 25, 25)
GRAY = (110, 110, 110)
BLUE = (11, 102, 195)
GREEN = (0, 120, 60)
ORANGE = (200, 110, 0)
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
    """Return (head, status, replaced, reason, {filename: {url, what, three}})."""
    p = os.path.join(R2, f"{sid}.md")
    if not os.path.exists(p):
        return "", "未探索", False, "", {}
    txt = open(p, encoding="utf-8").read()
    mm = re.search(r"採用枚数[:：]\s*(.+)", txt)
    head = mm.group(1).strip() if mm else ""
    nomatch = ("該当イラスト=**なし**" in txt or "該当イラストなし" in txt or "**なし**" in head
               or re.search(r"採用枚数[:：]\s*0", txt))
    status = "該当なし" if nomatch else "あり"
    replaced = ("置換" in head)  # RA7: 代替/置換採用
    # 判定結果 paragraph (for 該当なし slots)
    reason = ""
    rm = re.search(r"^##\s*判定結果.*?$\n+(.+?)(?=\n##|\n\Z)", txt, re.S | re.M)
    if rm:
        reason = re.sub(r"\s*\n\s*", "", rm.group(1)).strip()
    # adopted image sections (## NN.ext  OR  ### NN.ext（採用）= ...)
    secs = {}
    for m in re.finditer(r"^#{2,3}\s+(\d{2}\.(?:jpg|jpeg|png|gif))\b(.*?)(?=^#{2,3}\s|\Z)",
                         txt, re.S | re.M):
        fn, body = m.group(1), m.group(2)
        url = (re.search(r"〔出所URL〕\s*(\S+)", body)
               or re.search(r"出所URL[:：]\s*(\S+)", body))
        what = (re.search(r"〔何の事故か〕\s*(.+)", body)
                or re.search(r"何の事故か[:：]\s*(.+)", body))
        three = (re.search(r"〔3要素チェック〕\s*(.+)", body)
                 or re.search(r"3要素(?:チェック)?[:：]\s*(.+)", body))
        secs[fn] = {
            "url": url.group(1).strip() if url else "",
            "what": what.group(1).strip() if what else "",
            "three": three.group(1).strip() if three else "",
        }
    return head, status, replaced, reason, secs


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


# ----- aggregate -----
META = {sid: parse_md(sid) for _, sid, _ in SLOTS}
IMGS = {sid: slot_imgs(sid) for _, sid, _ in SLOTS}
n_adopt_slot = sum(1 for _, s, _ in SLOTS if IMGS[s])
n_imgs = sum(len(IMGS[s]) for _, s, _ in SLOTS)
n_nomatch = sum(1 for _, s, _ in SLOTS if (not IMGS[s]) and META[s][1] == "該当なし")
n_replaced = sum(1 for _, s, _ in SLOTS if IMGS[s] and META[s][2])


def tag_for(sid):
    imgs = IMGS[sid]
    head, status, replaced, reason, secs = META[sid]
    if imgs:
        t = f"採用 {len(imgs)}点" + ("（置換採用）" if replaced else "")
        return t, GREEN
    if status == "該当なし":
        return "該当イラストなし", RED
    return "未探索", GRAY


def cover():
    im, d = new_page()
    d.rectangle([0, 0, PW, 150], fill=RED)
    d.text((M, 46), "事故イラスト カタログ（最終版）", font=FT, fill="white")
    y = 205
    lines = [
        (f"最終版・{DATE}　/　全20スロット（TGL 10・高所作業車 10）", FH, INK),
        (f"採用 {n_adopt_slot} スロット・採用イラスト総数 {n_imgs} 点／該当イラストなし {n_nomatch} スロット／置換採用 {n_replaced} スロット",
         FM, INK),
        ("", FS, INK),
        ("TGL付きトラック／高所作業車の『事故イラスト』(3要素=機械＋事故の事象＋被災者を満たす絵)を収集。", FM, INK),
        ("通常作業・構造/部品名称図・単体写真・汎用転落ピクトは採用禁止。無理な当てはめはしない。", FM, INK),
        ("画像生成は一切なし。ブラウザ画像検索→当方で実目視し3要素で判定したもののみ採用。", FS, GRAY),
        ("※重複1点を明記：RT1/01.jpg と RT3/01.jpg は同一画像（md5一致）。墜落(RT1)／荷の滑落・下敷き(RT3)の両事象を満たすため両スロットに併記採用。",
         FS, GRAY),
    ]
    for t, f, c in lines:
        if t == "":
            y += 18; continue
        for ln in wrap(d, t, f, PW - 2 * M):
            d.text((M, y), ln, font=f, fill=c); y += int(f.size * 1.5)
        y += 6
    y += 14
    d.text((M, y), "■ 凡例", font=FL, fill=INK); y += 44
    for t, c in [("採用◯点：3要素を満たす事故イラストを採用", GREEN),
                 ("置換採用：規定原因の厳密図は未取得→同系統の事故イラスト/事故写真で置換（旨を明記）", ORANGE),
                 ("該当イラストなし：規定どおり無理に当てない（候補は実目視で全数判定済み）", RED)]:
        d.text((M + 20, y), "● " + t, font=FS, fill=c)
        y += 38
    d.text((M, PH - 70), "限定共有用・noindex・非公開URL。各スロット詳細は refs2/{SID}.md に記録。",
           font=FS, fill=GRAY)
    pages.append(im)


def status_page():
    im, d = new_page()
    d.rectangle([0, 0, PW, 110], fill=RED)
    d.text((M, 30), "スロット別 採用一覧（全20スロット）", font=FH, fill="white")
    y = 150
    for cat, sid, name in SLOTS:
        tag, col = tag_for(sid)
        catcol = TGLC if cat == "TGL" else AERC
        d.text((M, y), f"[{cat}]", font=FU, fill=catcol)
        d.text((M + 80, y), f"{sid}", font=FL, fill=INK)
        for ln in wrap(d, name, FS, PW - M - 380):
            d.text((M + 200, y + 2), ln, font=FS, fill=INK); break
        d.text((PW - M - d.textlength(tag, font=FL) - 4, y), tag, font=FL, fill=col)
        y += 46
    d.text((M, y + 20),
           f"合計：採用 {n_adopt_slot}スロット / {n_imgs}点・置換採用 {n_replaced}スロット・該当なし {n_nomatch}スロット",
           font=FM, fill=INK)
    d.text((M, PH - 50), f"最終版 {DATE}", font=FU, fill=GRAY)
    pages.append(im)


def cat_divider(cat):
    im, d = new_page()
    col = TGLC if cat == "TGL" else AERC
    d.rectangle([0, PH // 2 - 120, PW, PH // 2 + 120], fill=col)
    label = "カテゴリ：TGL（テールゲートリフター付きトラック）" if cat == "TGL" \
        else "カテゴリ：高所作業車"
    d.text((M, PH // 2 - 28), label, font=FH, fill="white")
    pages.append(im)


def slot_detail(cat, sid, name, imgs, secs, replaced):
    catcol = TGLC if cat == "TGL" else AERC
    per = 2
    chunks = [imgs[i:i + per] for i in range(0, len(imgs), per)] or [[]]
    for pi, chunk in enumerate(chunks):
        im, d = new_page()
        d.rectangle([0, 0, PW, 112], fill=catcol)
        ttl = f"{sid}  {name}"
        d.text((M, 18), ttl if d.textlength(ttl, font=FL) < PW - 2 * M else sid + " " + name[:22] + "…",
               font=FL, fill="white")
        sub = f"[{cat}] 採用{len(imgs)}点" + ("（置換採用）" if replaced else "（事故イラスト＝あり）")
        if len(chunks) > 1:
            sub += f"  ({pi+1}/{len(chunks)})"
        d.text((M, 66), sub, font=FU, fill="white")
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
        d.text((M, PH - 46), f"最終版 {DATE}　|　{sid}", font=FU, fill=GRAY)
        pages.append(im)


def slot_nomatch(cat, sid, name, reason):
    catcol = TGLC if cat == "TGL" else AERC
    im, d = new_page()
    d.rectangle([0, 0, PW, 112], fill=catcol)
    d.text((M, 18), f"{sid}  {name}", font=FL, fill="white")
    d.text((M, 66), f"[{cat}] 採用0点", font=FU, fill="white")
    y = 190
    d.rectangle([M, y, PW - M, y + 110], fill=(253, 236, 234), outline=RED)
    d.text((M + 30, y + 34), "該当イラストなし（3要素を満たす事故イラスト/写真が見つからず）", font=FH, fill=RED)
    y += 160
    note = reason or "収集候補を実目視で全数判定したが、3要素（機械=TGL/高所作業車・事故の事象・被災者）を同時に満たす事故イラストは存在しなかった。規定どおり無理な当てはめはせず該当なしとする。"
    for ln in wrap(d, note, FM, PW - 2 * M):
        d.text((M, y), ln, font=FM, fill=INK); y += 38
    d.text((M, PH - 46), f"最終版 {DATE}　|　{sid}　詳細: refs2/{sid}.md", font=FU, fill=GRAY)
    pages.append(im)


# ----- build -----
cover()
status_page()
cur_cat = None
for cat, sid, name in SLOTS:
    if cat != cur_cat:
        cat_divider(cat); cur_cat = cat
    head, status, replaced, reason, secs = META[sid]
    imgs = IMGS[sid]
    if imgs:
        slot_detail(cat, sid, name, imgs, secs, replaced)
    else:
        slot_nomatch(cat, sid, name, reason)

pages[0].save(OUT_PDF, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
print("WROTE", OUT_PDF, "pages=", len(pages),
      "| adopt_slots=", n_adopt_slot, "imgs=", n_imgs,
      "nomatch=", n_nomatch, "replaced=", n_replaced)
