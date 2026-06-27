# -*- coding: utf-8 -*-
"""build_modelslab_pdf.py — 方式A/B/C1/C2の比較PDFを作成。各画像に〔方式・モデル・原因〕見出し、
   B/Cは ベース/下書き(左) と 生成(右) を並べる。A4横 1754x1240@150dpi。PIL使用(py で実行)。"""
import os, csv
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img"); BASE = os.path.join(HERE, "base"); DRAFT = os.path.join(HERE, "draft")
OUT = os.path.join(HERE, "compare_modelslab_v1.pdf")
W, H = 1754, 1240
def font(sz, bold=False):
    for p in [r"C:\Windows\Fonts\YuGothB.ttc" if bold else r"C:\Windows\Fonts\YuGothM.ttc",
              r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc",
              r"C:\Windows\Fonts\msgothic.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except: pass
    return ImageFont.load_default()
F_H1, F_H2, F_B, F_S = font(46, True), font(30, True), font(24), font(20)
METHOD_DESC = {
 "A":  ("方式A: text2img（文章のみ・ベース無し）", "イラスト系モデル flat-2d-animerge。プロンプトだけで10原因を生成。"),
 "B":  ("方式B: img2img（本物の災害イラストをベース）", "realtime(SDXL) prompt_strength=0.55。元の構図/姿勢を残し画風を変換。左=元イラスト 右=生成。"),
 "C1": ("方式C1: img2img（自作下書きベース・拘束ゆるめ strength=0.72）", "flat-2d-animerge。下書きの線を強く上書きし画質優先。左=下書き 右=生成。"),
 "C2": ("方式C2: img2img（自作下書きベース・拘束つよめ strength=0.5）", "flat-2d-animerge。下書きの構図をより保持。左=下書き 右=生成。controlnet不可のため強度比較で代替。"),
}
def load(path, box):
    try:
        im = Image.open(path).convert("RGB")
    except Exception:
        im = Image.new("RGB", box, (230,230,230))
    im.thumbnail(box, Image.LANCZOS)
    return im
def read_rows():
    rows = []
    with open(os.path.join(HERE, "index.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f): rows.append(r)
    return rows
rows = read_rows()
by = {"A":[], "B":[], "C1":[], "C2":[]}
for r in rows:
    m = r["方式"]
    if m in by: by[m].append(r)
pages = []
def new_page():
    p = Image.new("RGB", (W, H), (255,255,255)); return p, ImageDraw.Draw(p)
def section_header(d, title, desc, y=28):
    d.rectangle([28, y, W-28, y+92], fill=(21,57,107))
    d.text((44, y+12), title, font=F_H2, fill=(255,255,255))
    d.text((44, y+54), desc, font=F_S, fill=(200,215,235))
    return y+108
def cause_of(r): return r["原因状況"]
# --- 方式A: 5枚×2列のグリッド（ベース無し） ---
def build_A(items):
    cols, rows_per = 5, 2
    cw, ch = (W-56)//cols, (H-150-40)//rows_per
    i = 0
    while i < len(items):
        p, d = new_page()
        y0 = section_header(d, *METHOD_DESC["A"])
        for r in range(rows_per):
            for c in range(cols):
                if i >= len(items): break
                it = items[i]; i += 1
                x = 28 + c*cw; y = y0 + r*ch
                im = load(os.path.join(IMG, it["画像ファイル"]), (cw-20, ch-90))
                p.paste(im, (x+(cw-20-im.width)//2+10, y+8))
                d.text((x+10, y+ch-78), f'A-{it["連番"]}  {it["使用モデルID"]}', font=F_S, fill=(20,20,20))
                cau = cause_of(it)
                d.text((x+10, y+ch-52), cau[:20], font=F_S, fill=(60,60,60))
                if len(cau) > 20: d.text((x+10, y+ch-30), cau[20:40], font=F_S, fill=(60,60,60))
        pages.append(p)
# --- 方式B/C: 1行=ベース/下書き(左)+生成(右)、3行/ページ ---
def build_pair(method, items, leftdir, leftlabel):
    per = 3; rh = (H-150-30)//per
    i = 0
    while i < len(items):
        p, d = new_page()
        y0 = section_header(d, *METHOD_DESC[method])
        for r in range(per):
            if i >= len(items): break
            it = items[i]; i += 1
            y = y0 + r*rh
            bd = it["ベース下書き"]   # base/0002 or draft/01
            lid = bd.split("/")[-1] if "/" in bd else ""
            lpath = None
            if leftdir == BASE:
                for ext in ("jpg","png","jpeg","webp"):
                    cand = os.path.join(BASE, f"{lid}.{ext}")
                    if os.path.exists(cand): lpath = cand; break
            else:
                cand = os.path.join(DRAFT, f"{lid}.png")
                if os.path.exists(cand): lpath = cand
            limg = load(lpath, (rh-30, rh-30)) if lpath else Image.new("RGB",(rh-30,rh-30),(235,235,235))
            gimg = load(os.path.join(IMG, it["画像ファイル"]), (rh-30, rh-30))
            d.text((40, y+6), f'{method}-{it["連番"]}  生成モデル: {it["使用モデルID"]}  strength={it["prompt_strength"]}', font=F_B, fill=(21,57,107))
            ly = y+40
            p.paste(limg, (40, ly)); d.text((40, ly+limg.height+2), f'{leftlabel}({lid})', font=F_S, fill=(90,90,90))
            d.text((40+rh+10, ly+ (rh-30)//2), "→", font=F_H2, fill=(150,150,150))
            gx = 40+rh+70
            p.paste(gimg, (gx, ly)); d.text((gx, ly+gimg.height+2), "生成(ModelsLab)", font=F_S, fill=(90,90,90))
            cau = cause_of(it)
            tx = gx + (rh-30) + 40
            d.text((tx, ly+10), "原因/状況:", font=F_B, fill=(20,20,20))
            yy = ly+44
            for k in range(0, len(cau), 16):
                d.text((tx, yy), cau[k:k+16], font=F_B, fill=(50,50,50)); yy += 30
        pages.append(p)
# cover
cv, d = new_page()
d.rectangle([0,0,W,H], fill=(248,249,251))
d.text((60, 80), "高所作業車 墜落事故 安全教育イラスト", font=F_H1, fill=(21,57,107))
d.text((60, 150), "ModelsLab API 方式別比較 (compare_modelslab_v1)", font=F_H2, fill=(40,40,40))
yy=240
for t in ["方式A: text2img（文章のみ）— イラスト系モデル flat-2d-animerge",
          "方式B: img2img（本物の災害イラストをベース）— realtime(SDXL) strength0.55",
          "方式C1: img2img（自作下書きベース・拘束ゆるめ strength0.72）— flat-2d-animerge",
          "方式C2: img2img（自作下書きベース・拘束つよめ strength0.5）— flat-2d-animerge",
          "高所作業車=シザースリフト/人の墜落のみ。原因=危険姿勢が引き金。文字/矢印/流血なし方針。",
          "注: ModelsLab controlnet エンドポイントは本プランで利用不可(POST非対応)→C2は低strengthで代替。"]:
    d.text((70, yy), "・"+t, font=F_B, fill=(30,30,30)); yy+=46
pages.append(cv)
build_A(by["A"]); build_pair("B", by["B"], BASE, "元イラスト"); build_pair("C1", by["C1"], DRAFT, "自作下書き"); build_pair("C2", by["C2"], DRAFT, "自作下書き")
pages[0].save(OUT, save_all=True, append_images=pages[1:], resolution=150.0)
# QA: 数ページをPNG出力
pages[1].save(os.path.join(HERE, "_qa_pA.png"))
if len(pages) > 2: pages[2].save(os.path.join(HERE, "_qa_pB.png"))
for i,p in enumerate(pages):
    if "C1" in "" : pass
print("PDF", OUT, os.path.getsize(OUT), "bytes,", len(pages), "pages")
