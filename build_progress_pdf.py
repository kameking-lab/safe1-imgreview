# -*- coding: utf-8 -*-
"""progress_report PDF (A4縦・日本語). 収集タスクの進捗・サイクル統計・終了予想・残タスク。
既存ファイルを読むだけ。新規生成・破壊なし。"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
STAMP = sys.argv[1] if len(sys.argv) > 1 else "20260614_1958"
NOW = sys.argv[2] if len(sys.argv) > 2 else "2026-06-14 19:58 JST"
OUT = os.path.join(BASE, f"progress_report_{STAMP}.pdf")

PW, PH = 1240, 1754
M = 60
RED = (192, 57, 43); INK = (25, 25, 25); GRAY = (110, 110, 110)
BLUE = (11, 102, 195); GREEN = (0, 120, 60); AMBER = (176, 106, 0)


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


FT = font(44); FH = font(30); FL = font(25); FM = font(23, False)
FS = font(20, False); FU = font(18, False)
pages = []


def new_page():
    im = Image.new("RGB", (PW, PH), "white")
    return im, ImageDraw.Draw(im)


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


def hbar(d, y, title):
    d.rectangle([0, y, PW, y + 56], fill=RED)
    d.text((M, y + 12), title, font=FH, fill="white")
    return y + 80


def table(d, x, y, cols, rows, widths, fcell=FS, rh=40, header=True):
    """Simple table. cols=list headers, rows=list of lists. widths=list px."""
    tw = sum(widths)
    # header
    if header:
        d.rectangle([x, y, x + tw, y + rh], fill=(235, 238, 242))
        cx = x
        for c, w in zip(cols, widths):
            d.text((cx + 8, y + 8), c, font=FL, fill=INK); cx += w
        y += rh
    for r in rows:
        cx = x
        d.line([x, y, x + tw, y], fill=(220, 220, 220))
        for v, w in zip(r, widths):
            col = INK
            d.text((cx + 8, y + 7), str(v), font=fcell, fill=col); cx += w
        y += rh
    d.line([x, y, x + tw, y], fill=(220, 220, 220))
    # verticals
    cx = x
    for w in widths:
        d.line([cx, y - rh * (len(rows) + (1 if header else 0)), cx, y], fill=(220, 220, 220)); cx += w
    d.line([x + tw, y - rh * (len(rows) + (1 if header else 0)), x + tw, y], fill=(220, 220, 220))
    return y + 10


# ---------- DATA ----------
A_TGL, A_AER = 39, 34
A_TOTAL = A_TGL + A_AER
QDONE = 10
B_TGL, B_AER = 1386, 916
B_SCANNED = 420934
B_SHIBO, B_SHISYO = 44537, 376397
N_CSV = 40
CYCLES = 9
LIMITS = 0
DONE_N, TOTAL_N = 9, 14
PROG = round(DONE_N / TOTAL_N * 100)
AVG_CYCLE = 7.6
REMAIN = 5
TGL_CAT = [("はさまれ・巻き込まれ", 440), ("墜落・転落", 334), ("飛来・落下", 127),
           ("崩壊・倒壊", 120), ("激突され", 117), ("転倒", 98), ("動作の反動・無理な動作", 78),
           ("激突", 54), ("交通事故(道路)", 8), ("切れ・こすれ", 8), ("その他", 2)]
AER_CAT = [("墜落・転落", 311), ("はさまれ・巻き込まれ", 221), ("交通事故(道路)", 67),
           ("転倒", 64), ("激突され", 61), ("飛来・落下", 43), ("激突", 41), ("感電", 27),
           ("動作の反動・無理な動作", 26), ("切れ・こすれ", 25), ("崩壊・倒壊", 11),
           ("高温・低温接触", 10), ("火災", 6), ("その他", 2), ("有害物接触", 1)]
EST = [("楽観", "約20:20 JST", "残5×約4.5分・制限なし(これまで0回)"),
       ("標準", "約20:35〜20:40 JST", "残5×平均7.6分・制限なし"),
       ("悲観", "約21:30 JST", "残5×約10分＋利用制限待ち1回(約30〜60分)を加味")]
REMAIN_TASKS = [
    ("B4", "あんぜんサイトDB等で出典URL補完・件数積み増し", "着手中"),
    ("B5", "Excel生成（TGL/AERIAL＋集計）", "未"),
    ("C1", "img_catalog.pdf 作成（通し番号付き一覧）", "未"),
    ("C2", "review_collect 配置・Vercel再デプロイ・push", "未"),
    ("C3", "REPORT_C.md 作成・push", "未"),
]


# ---------- COVER ----------
def cover():
    im, d = new_page()
    d.rectangle([0, 0, PW, 150], fill=RED)
    d.text((M, 40), "収集タスク 進捗レポート", font=FT, fill="white")
    d.text((M, 104), "事故イラスト収集(A)＋事故情報Excel化(B)・全自動ランナー", font=FU, fill="white")
    y = 200
    d.text((M, y), f"現在時刻: {NOW}", font=FH, fill=INK); y += 56
    d.text((M, y), f"総合進捗: {DONE_N}/{TOTAL_N} タスク完了（{PROG}%）", font=FH, fill=GREEN); y += 50
    d.text((M, y), "現在着手中: B4（あんぜんサイトDB等で出典URL補完）", font=FM, fill=AMBER); y += 60
    # progress bar
    bw = PW - 2 * M
    d.rectangle([M, y, M + bw, y + 40], outline=(180, 180, 180))
    d.rectangle([M, y, M + int(bw * DONE_N / TOTAL_N), y + 40], fill=GREEN)
    d.text((M + 10, y + 7), f"{PROG}%", font=FL, fill="white"); y += 80
    rows = [
        ("(A) 事故イラスト", f"{A_TOTAL}枚 (TGL {A_TGL}/高所 {A_AER}) ・収集確定(A6完了)"),
        ("(B) 事故情報", f"TGL {B_TGL}件 / 高所 {B_AER}件 ・走査{B_SCANNED:,}件"),
        ("サイクル数", f"{CYCLES} サイクル ・利用制限到達 {LIMITS} 回"),
        ("ランナー", "稼働中（無人継続・PID常駐）"),
    ]
    for k, v in rows:
        d.text((M, y), "● " + k, font=FL, fill=INK)
        for i, ln in enumerate(wrap(d, v, FM, PW - 2 * M - 300)):
            d.text((M + 300, y + 2 + i * 30), ln, font=FM, fill=(50, 50, 50))
        y += 30 * max(1, len(wrap(d, v, FM, PW - 2 * M - 300))) + 18
    d.text((M, PH - 70), "限定共有・noindex。ランナーは停止していません（本レポートは読み取りのみ）。",
           font=FS, fill=GRAY)
    pages.append(im)


# ---------- (A)(B) detail ----------
def detail():
    im, d = new_page()
    y = hbar(d, 0, "(A) 事故イラスト収集")
    d.text((M, y), f"採用 {A_TOTAL}枚（TGL {A_TGL}・高所 {A_AER}）／ img_index.csv {A_TOTAL}行 ／ 消化クエリ {QDONE}",
           font=FM, fill=INK); y += 38
    d.text((M, y), "出尽くし判定: A6（全体重複再排除・通し番号確定）まで完了済み＝収集は確定。", font=FS, fill=GREEN)
    y += 32
    d.text((M, y), "重複排除: md5 で実体重複を統合し連番 0001〜 で保存。", font=FS, fill=GRAY); y += 50

    y = hbar(d, y, "(B) 事故情報 抽出（JNIOSH一次データ）")
    d.text((M, y), f"走査総数 {B_SCANNED:,}件（死亡DB {B_SHIBO:,}＋死傷DB {B_SHISYO:,}）／ CSV {N_CSV}本",
           font=FM, fill=INK); y += 36
    d.text((M, y), "DL範囲: 死亡DB SHIBO 1991-2018(28年) ／ 死傷DB SHISYO 2006-2017(12年)。", font=FS, fill=GRAY)
    y += 34
    y = table(d, M, y, ["群", "抽出(重複排除後)", "raw", "重複除去", "目標達成"],
              [["TGL", B_TGL, 1388, 2, "達成(>1000)"],
               ["高所", B_AER, 929, 13, "公的データ上限(916)"]],
              [120, 300, 130, 150, 360], rh=42)
    d.text((M, y), "※高所は一次データを全件走査した結果の上限件数（水増しせず実数を報告）。", font=FS, fill=AMBER)
    y += 32
    d.text((M, y), "Excel(B5)は未生成。B4(あんぜんサイト補完)着手中。", font=FS, fill=GRAY); y += 50

    # category tables side by side
    d.text((M, y), "■ 事故の型別 件数", font=FL, fill=INK); y += 44
    y0 = y
    d.text((M, y), "TGL群", font=FL, fill=BLUE);
    yy = y + 40
    for name, n in TGL_CAT:
        d.text((M, yy), f"・{name}", font=FU, fill=INK)
        d.text((M + 360 - d.textlength(str(n), font=FU), yy), str(n), font=FU, fill=INK); yy += 26
    x2 = M + 440
    d.text((x2, y), "高所群", font=FL, fill=BLUE)
    yy2 = y + 40
    for name, n in AER_CAT:
        d.text((x2, yy2), f"・{name}", font=FU, fill=INK)
        d.text((x2 + 360 - d.textlength(str(n), font=FU), yy2), str(n), font=FU, fill=INK); yy2 += 26
    pages.append(im)


# ---------- cycle stats + estimate + remaining ----------
def estimate_page():
    im, d = new_page()
    y = hbar(d, 0, "サイクル統計・制限到達状況")
    rows = [
        ("サイクル数（col_*.log）", f"{CYCLES}"),
        ("初回ログ", "2026-06-14 18:51:45"),
        ("最新ログ更新", "2026-06-14 19:55:21"),
        ("平均サイクル所要", f"約 {AVG_CYCLE} 分/タスク（経過68.5分 ÷ 9）"),
        ("利用制限到達(usage/rate/429)", f"{LIMITS} 回（自動再開の発生なし）"),
        ("完了/全", f"{DONE_N}/{TOTAL_N}（残 {REMAIN}）"),
    ]
    for k, v in rows:
        d.text((M, y), "● " + k, font=FM, fill=INK)
        d.text((M + 520, y), v, font=FM, fill=(50, 50, 50)); y += 40
    y += 20

    y = hbar(d, y, "終了予想時刻（楽観／標準／悲観）")
    y = table(d, M, y, ["シナリオ", "終了予想(JST)", "根拠"],
              [[s, t, r] for s, t, r in EST],
              [140, 320, 600], rh=58, fcell=FU)
    y += 10
    note = ("算出根拠: 平均サイクル ≈ 7.6分/タスク（実測：経過68.5分/9タスク）。残タスク=5（B4・B5・C1・C2・C3）。"
            "B5/C1/C3 は軽量・C2はデプロイで中程度・B4はWeb補完でやや重い。利用制限はこれまで0回のため標準では無加算、"
            "悲観は5時間枠到達による待機1回(約30〜60分)を仮定。")
    for ln in wrap(d, note, FS, PW - 2 * M):
        d.text((M, y), ln, font=FS, fill=GRAY); y += 30
    y += 24

    y = hbar(d, y, "残タスク一覧")
    for tid, name, st in REMAIN_TASKS:
        col = AMBER if st == "着手中" else GRAY
        d.text((M, y), f"[{tid}]", font=FL, fill=BLUE)
        for ln in wrap(d, name, FS, PW - 2 * M - 260):
            d.text((M + 90, y + 2), ln, font=FS, fill=INK); break
        d.text((PW - M - d.textlength(st, font=FL), y), st, font=FL, fill=col); y += 44
    d.text((M, PH - 50), f"進捗レポート {NOW}", font=FU, fill=GRAY)
    pages.append(im)


cover()
detail()
estimate_page()
pages[0].save(OUT, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
print("WROTE", OUT, "pages=", len(pages))
