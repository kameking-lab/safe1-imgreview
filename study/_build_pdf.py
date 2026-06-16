# -*- coding: utf-8 -*-
"""BUILD: study/*.md を統合し A4縦・日本語PDF (study_tgl_aerial.pdf) を生成。
既存PDFは上書きしない新名。py + PIL のみ。画像生成・外部読込なし。"""
import os, re
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDY = os.path.join(ROOT, "study")
OUT = os.path.join(ROOT, "study_tgl_aerial.pdf")

# ---- 版面 (A4縦 150dpi) ----
W, H = 1240, 1754
ML, MR, MT, MB = 80, 80, 90, 90
CW = W - ML - MR  # content width
FG = (20, 20, 20)
GRAY = (90, 90, 90)
RULE = (170, 170, 170)
QUOTE_BG = (244, 246, 248)
QUOTE_BAR = (120, 150, 190)
TH_BG = (224, 232, 240)
TCELL_BORDER = (180, 180, 180)
ACCENT = (28, 70, 120)

FREG = "C:/Windows/Fonts/meiryo.ttc"
FBLD = "C:/Windows/Fonts/meiryob.ttc"
_cache = {}
def font(size, bold=False):
    key = (size, bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FBLD if bold else FREG, size, index=0)
    return _cache[key]

# 本文/見出しサイズ
S_BODY = 23
S_H1 = 40
S_H2 = 31
S_H3 = 26
S_SMALL = 20
LH_BODY = 36   # 行送り(本文)

pages = []
def new_page():
    img = Image.new("RGB", (W, H), "white")
    return img, ImageDraw.Draw(img), MT

cur_img, draw, y = new_page()

def flush():
    global cur_img, draw, y
    pages.append(cur_img)
    cur_img, draw, y = new_page()

def ensure(space):
    """残り高さが足りなければ改ページ"""
    global y
    if y + space > H - MB:
        flush()

# ---- インライン: **bold** / `code` を (char,bold) 列に ----
def tokenize(text):
    out = []
    bold = False
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("**", i):
            bold = not bold
            i += 2
            continue
        c = text[i]
        if c == "`":      # コードマーカは除去
            i += 1
            continue
        out.append((c, bold))
        i += 1
    return out

def wrap_runs(chars, fnt_reg, fnt_bld, max_w):
    """(char,bold)列を max_w で折返し、行(=run列)のリストにする"""
    lines = []
    cur = []
    cw = 0
    for c, b in chars:
        f = fnt_bld if b else fnt_reg
        w = f.getlength(c)
        if c == "\n":
            lines.append(cur); cur = []; cw = 0; continue
        if cw + w > max_w and cur:
            lines.append(cur); cur = []; cw = 0
        cur.append((c, b))
        cw += w
    lines.append(cur)
    return lines

def draw_line_runs(d, x, yy, runs, fnt_reg, fnt_bld, color=FG):
    cx = x
    for c, b in runs:
        f = fnt_bld if b else fnt_reg
        d.text((cx, yy), c, font=f, fill=color)
        cx += f.getlength(c)

def render_paragraph(text, size=S_BODY, indent=0, color=FG, lh=LH_BODY, gap=6):
    global y
    fr = font(size); fb = font(size, True)
    chars = tokenize(text)
    maxw = CW - indent
    lines = wrap_runs(chars, fr, fb, maxw)
    for ln in lines:
        ensure(lh)
        draw_line_runs(draw, ML + indent, y, ln, fr, fb, color)
        y += lh
    y += gap

def render_bullet(text, size=S_BODY, level=0, checkbox=None):
    global y
    fr = font(size); fb = font(size, True)
    bx_indent = 24 + level * 28
    marker = "・"
    if checkbox == "off": marker = "□ "
    elif checkbox == "on": marker = "☑ "
    chars = tokenize(text)
    maxw = CW - bx_indent - 8
    lines = wrap_runs(chars, fr, fb, maxw)
    lh = LH_BODY
    for i, ln in enumerate(lines):
        ensure(lh)
        if i == 0:
            draw.text((ML + bx_indent - 22, y), marker, font=fr, fill=ACCENT if checkbox is None else GRAY)
        draw_line_runs(draw, ML + bx_indent, y, ln, fr, fb)
        y += lh
    y += 4

def render_h1(text):
    global y
    flush()  # 章は新ページ
    f = font(S_H1, True)
    draw.rectangle([ML, y, W - MR, y + 6], fill=ACCENT)
    y += 18
    chars = tokenize(text)
    lines = wrap_runs(chars, f, f, CW)
    for ln in lines:
        draw_line_runs(draw, ML, y, ln, f, f, ACCENT)
        y += S_H1 + 10
    y += 6
    draw.line([ML, y, W - MR, y], fill=RULE, width=2)
    y += 20

def render_h2(text):
    global y
    ensure(70)
    y += 8
    f = font(S_H2, True)
    chars = tokenize(text)
    lines = wrap_runs(chars, f, f, CW - 16)
    draw.rectangle([ML, y + 2, ML + 8, y + S_H2 + 4], fill=ACCENT)
    for i, ln in enumerate(lines):
        draw_line_runs(draw, ML + 18, y, ln, f, f, (15, 40, 75))
        y += S_H2 + 8
    y += 8

def render_h3(text):
    global y
    ensure(56)
    y += 4
    f = font(S_H3, True)
    chars = tokenize(text)
    lines = wrap_runs(chars, f, f, CW)
    for ln in lines:
        draw_line_runs(draw, ML, y, ln, f, f, (40, 40, 40))
        y += S_H3 + 7
    y += 4

def render_quote(lines_text):
    global y
    size = S_SMALL
    fr = font(size); fb = font(size, True)
    lh = 30
    # 事前に行数を測り、背景帯を描く
    wrapped = []
    for t in lines_text:
        chars = tokenize(t)
        wrapped.extend(wrap_runs(chars, fr, fb, CW - 60) or [[]])
    total_h = lh * len(wrapped) + 18
    ensure(total_h)
    top = y
    draw.rectangle([ML, top, W - MR, top + total_h], fill=QUOTE_BG)
    draw.rectangle([ML, top, ML + 6, top + total_h], fill=QUOTE_BAR)
    yy = top + 9
    for ln in wrapped:
        draw_line_runs(draw, ML + 22, yy, ln, fr, fb, GRAY)
        yy += lh
    y = top + total_h + 12

def render_hr():
    global y
    ensure(20)
    y += 6
    draw.line([ML, y, W - MR, y], fill=RULE, width=1)
    y += 14

# ---- テーブル ----
def render_table(header, rows):
    global y
    size = S_SMALL
    fr = font(size); fb = font(size, True)
    ncol = len(header)
    # 列幅: 内容の最大自然幅から比率配分(上限あり)
    natural = [0] * ncol
    for r in [header] + rows:
        for j in range(ncol):
            if j < len(r):
                txt = re.sub(r"\*\*|`", "", r[j])
                natural[j] = max(natural[j], fr.getlength(txt))
    tot = sum(natural) or 1
    avail = CW - (ncol + 1) * 1
    widths = []
    for j in range(ncol):
        w = max(70, min(natural[j] + 24, avail * 0.55))
        widths.append(w)
    # 正規化して合計を avail に収める
    scale = avail / sum(widths)
    widths = [w * scale for w in widths]

    pad = 8
    line_h = 28

    def cell_lines(text):
        chars = tokenize(text)
        return wrap_runs(chars, fr, fb, 0) if False else None

    def draw_row(cells, is_header):
        global y
        # 各セルを折返し、行高を決定
        wrapped_cells = []
        maxlines = 1
        for j in range(ncol):
            txt = cells[j] if j < len(cells) else ""
            chars = tokenize(txt)
            wl = wrap_runs(chars, fr, fb, widths[j] - 2 * pad)
            wrapped_cells.append(wl)
            maxlines = max(maxlines, len(wl))
        rh = maxlines * line_h + 2 * pad
        ensure(rh)
        x0 = ML
        top = y
        # 背景(ヘッダ)
        if is_header:
            draw.rectangle([x0, top, x0 + sum(widths), top + rh], fill=TH_BG)
        # セル
        cx = x0
        for j in range(ncol):
            # 枠
            draw.rectangle([cx, top, cx + widths[j], top + rh], outline=TCELL_BORDER, width=1)
            yy = top + pad
            for ln in wrapped_cells[j]:
                draw_line_runs(draw, cx + pad, yy, ln, fr, fb, FG)
                yy += line_h
            cx += widths[j]
        y = top + rh

    ensure(line_h * 2)
    draw_row(header, True)
    for r in rows:
        draw_row(r, False)
    y += 12

# ---- マークダウン解析 ----
def is_table_sep(line):
    return bool(re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line

def split_row(line):
    s = line.strip()
    if s.startswith("|"): s = s[1:]
    if s.endswith("|"): s = s[:-1]
    return [c.strip() for c in s.split("|")]

def render_markdown(md, chapter_title=None):
    global y
    lines = md.split("\n")
    i = 0
    n = len(lines)
    # 先頭 H1 を章タイトルに使う
    while i < n:
        line = lines[i].rstrip("\n")
        s = line.strip()
        # テーブル検出
        if "|" in line and i + 1 < n and is_table_sep(lines[i + 1]):
            header = split_row(line)
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            render_table(header, rows)
            continue
        if s == "":
            y += 6; i += 1; continue
        if s == "---":
            render_hr(); i += 1; continue
        if s.startswith("# "):
            render_h1(s[2:].strip()); i += 1; continue
        if s.startswith("## "):
            render_h2(s[3:].strip()); i += 1; continue
        if s.startswith("### "):
            render_h3(s[4:].strip()); i += 1; continue
        if s.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            render_quote(block); continue
        m = re.match(r"^(\s*)- \[( |x)\] (.*)$", line)
        if m:
            lvl = len(m.group(1)) // 2
            render_bullet(m.group(3), level=lvl, checkbox=("on" if m.group(2) == "x" else "off"))
            i += 1; continue
        m = re.match(r"^(\s*)[-*] (.*)$", line)
        if m:
            lvl = len(m.group(1)) // 2
            render_bullet(m.group(2), level=lvl)
            i += 1; continue
        m = re.match(r"^(\s*)(\d+)\. (.*)$", line)
        if m:
            lvl = len(m.group(1)) // 2
            render_bullet(m.group(3), level=lvl)
            # 番号付きは番号を前置
            i += 1; continue
        # 通常段落
        render_paragraph(s); i += 1

# ---- 表紙 ----
def cover():
    global y
    d = draw
    d.rectangle([0, 0, W, 230], fill=ACCENT)
    f1 = font(46, True)
    d.text((ML, 70), "テールゲートリフター／高所作業車", font=f1, fill="white")
    d.text((ML, 135), "安全 学習資料（理論武装メモ）", font=f1, fill="white")
    y = 300
    sub = [
        "イベント設営現場の打合せで即答するための自習資料",
        "",
        "・事故データは手元一次データ(accidents_TGL.xlsx n=1,878 / accidents_AERIAL.xlsx n=1,149)の実数",
        "・法令/施行日/条文は厚労省通達・JAISH収録本文・mhlw法令データベースで HTTP200＋本文一致を確認",
        "・TGLは貨物自動車のテールゲートリフターに限定／高所は起因物=高所作業車(コード146)のみ",
        "・確認できない事項は「出典確認できず(要確認)」と明記し断定しない",
    ]
    for t in sub:
        if t == "":
            y += 14; continue
        render_paragraph(t, size=S_SMALL, color=(50, 50, 50), lh=32, gap=4)
    y += 30
    # 目次
    render_h2_inline("目次")
    toc = [
        "第1章  エグゼクティブ要点（最多の事故の型・最初に言う危険3つ・法令要点）",
        "第2章  事故データ集計（事故の型別 件数ランキング：TGL／高所）",
        "第3章  TGL編 危険ポイント・機序・実事故事例",
        "第4章  TGL編 法令・規則（特別教育義務化ほか）",
        "第5章  高所作業車編 危険ポイント・機序・実事故事例",
        "第6章  高所作業車編 法令・規則（運転資格／フルハーネス／離隔距離）",
        "第7章  横断管理＋イベント設営現場の留意",
        "第8章  想定問答10問＋模範回答（根拠付き）",
        "第9章  用語集＋引用URL一覧",
    ]
    for t in toc:
        render_paragraph(t, size=S_BODY, lh=38, gap=2)
    y += 20
    ts = font(S_SMALL)
    draw.text((ML, H - MB - 10), "作成日: 2026-06-16 ／ 数値・法令は本文記載の出典に基づく", font=ts, fill=GRAY)

def render_h2_inline(text):
    global y
    y += 6
    f = font(S_H2, True)
    draw.rectangle([ML, y + 2, ML + 8, y + S_H2 + 4], fill=ACCENT)
    draw.text((ML + 18, y), text, font=f, fill=(15, 40, 75))
    y += S_H2 + 16

# ============ ビルド ============
cover()

# summary.md を「エグゼクティブ要点」と「用語集＋出典一覧」に分割
sm = open(os.path.join(STUDY, "summary.md"), encoding="utf-8").read()
split_marker = "## 2. 用語集"
idx = sm.find(split_marker)
sm_exec = sm[:idx].rstrip()
sm_ref = sm[idx:]
# 章タイトルを付け替える
sm_exec = re.sub(r"^# .*$", "# 第1章 エグゼクティブ要点", sm_exec, count=1, flags=re.M)
sm_ref = "# 第9章 用語集＋引用URL一覧\n\n" + sm_ref

def load(name, newtitle):
    md = open(os.path.join(STUDY, name), encoding="utf-8").read()
    md = re.sub(r"^# .*$", "# " + newtitle, md, count=1, flags=re.M)
    return md

render_markdown(sm_exec)
render_markdown(load("stats.md", "第2章 事故データ集計（事故の型別 件数）"))
render_markdown(load("tgl.md", "第3章 TGL編 危険ポイント・機序・実事故事例"))
render_markdown(load("tgl_law.md", "第4章 TGL編 法令・規則"))
render_markdown(load("aerial.md", "第5章 高所作業車編 危険ポイント・機序・実事故事例"))
render_markdown(load("aerial_law.md", "第6章 高所作業車編 法令・規則"))
render_markdown(load("cross.md", "第7章 横断管理＋イベント設営現場の留意"))
render_markdown(load("qa.md", "第8章 想定問答10問＋模範回答"))
render_markdown(sm_ref)

# 最終ページを確定
pages.append(cur_img)

# ---- フッタ(ページ番号) ----
fsmall = font(18)
total = len(pages)
for n, pg in enumerate(pages, 1):
    d = ImageDraw.Draw(pg)
    d.line([ML, H - MB + 18, W - MR, H - MB + 18], fill=RULE, width=1)
    txt = "テールゲートリフター／高所作業車 安全学習資料"
    d.text((ML, H - MB + 26), txt, font=fsmall, fill=GRAY)
    pno = f"{n} / {total}"
    w = fsmall.getlength(pno)
    d.text((W - MR - w, H - MB + 26), pno, font=fsmall, fill=GRAY)

if os.path.exists(OUT):
    raise SystemExit("ERROR: 既存PDFが存在。上書き禁止。中止。")

pages[0].save(OUT, "PDF", resolution=150.0, save_all=True, append_images=pages[1:])
print("OK pages=%d -> %s" % (total, OUT))
