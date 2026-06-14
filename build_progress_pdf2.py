# -*- coding: utf-8 -*-
"""progress_report PDF (A4縦・日本語) — 完了版。収集タスクの最終進捗・サイクル統計・実完了時刻・成果一覧。
既存ファイルを読むだけ。新規生成・破壊なし。"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
STAMP = sys.argv[1] if len(sys.argv) > 1 else "20260614_2116"
NOW = sys.argv[2] if len(sys.argv) > 2 else "2026-06-14 21:16 JST"
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
    tw = sum(widths)
    nrows = len(rows) + (1 if header else 0)
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
            d.text((cx + 8, y + 7), str(v), font=fcell, fill=INK); cx += w
        y += rh
    d.line([x, y, x + tw, y], fill=(220, 220, 220))
    cx = x
    for w in widths:
        d.line([cx, y - rh * nrows, cx, y], fill=(220, 220, 220)); cx += w
    d.line([x + tw, y - rh * nrows, x + tw, y], fill=(220, 220, 220))
    return y + 10


# ---------- DATA ----------
A_TGL, A_AER = 39, 34
A_TOTAL = A_TGL + A_AER
QDONE = 10
B_TGL, B_AER = 1878, 1149
B_TGL_J, B_TGL_A = 1386, 492
B_AER_J, B_AER_A = 916, 233
B_TOTAL = B_TGL + B_AER
B_SCANNED = 420934
N_CSV = 40
CYCLES = 14
LIMITS = 0
DONE_N, TOTAL_N = 14, 14
PROG = 100
SPAN = "18:51:45 〜 20:14:28（約1時間23分）"
AVG_CYCLE = 5.9
TGL_CAT = [("はさまれ・巻き込まれ", 581), ("墜落・転落", 457), ("激突され", 165),
           ("飛来・落下", 158), ("転倒", 145), ("崩壊・倒壊", 142),
           ("動作の反動・無理な動作", 121), ("激突", 88), ("交通事故(道路)", 9),
           ("切れ・こすれ", 9), ("その他", 2), ("高温・低温接触", 1)]
AER_CAT = [("墜落・転落", 392), ("はさまれ・巻き込まれ", 281), ("転倒", 84),
           ("交通事故(道路)", 78), ("激突され", 69), ("飛来・落下", 56), ("激突", 54),
           ("切れ・こすれ", 33), ("感電", 30), ("動作の反動・無理な動作", 30),
           ("崩壊・倒壊", 16), ("高温・低温接触", 15), ("火災", 6), ("その他", 4), ("有害物接触", 1)]
DELIV = [
    ("(A) 連番イラスト", "collect2/img/0001.jpg … ・collect2/img_index.csv"),
    ("(B) Excel TGL", "data_xlsx/accidents_TGL.xlsx（1,878件）"),
    ("(B) Excel 高所", "data_xlsx/accidents_AERIAL.xlsx（1,149件）"),
    ("一覧PDF", "img_catalog.pdf（通し番号付き一覧）"),
    ("最終報告", "REPORT_C.md（公開URL/raw/件数）"),
]


def cover():
    im, d = new_page()
    d.rectangle([0, 0, PW, 150], fill=GREEN)
    d.text((M, 40), "収集タスク 進捗レポート（完了）", font=FT, fill="white")
    d.text((M, 104), "事故イラスト収集(A)＋事故情報Excel化(B)・全自動ランナー", font=FU, fill="white")
    y = 200
    d.text((M, y), f"現在時刻: {NOW}", font=FH, fill=INK); y += 56
    d.text((M, y), f"総合進捗: {DONE_N}/{TOTAL_N} タスク完了（{PROG}%）★全完了", font=FH, fill=GREEN); y += 50
    d.text((M, y), "現在着手中: なし（DONE_C.flag 生成済・ランナー正常終了）", font=FM, fill=INK); y += 60
    bw = PW - 2 * M
    d.rectangle([M, y, M + bw, y + 40], outline=(180, 180, 180))
    d.rectangle([M, y, M + bw, y + 40], fill=GREEN)
    d.text((M + 10, y + 7), "100%", font=FL, fill="white"); y += 80
    rows = [
        ("(A) 事故イラスト", f"{A_TOTAL}枚 (TGL {A_TGL}/高所 {A_AER}) ・収集確定(出尽くし/A6完了)"),
        ("(B) 事故情報", f"計 {B_TOTAL:,}件（TGL {B_TGL:,}/高所 {B_AER:,}）・各群1000件超達成"),
        ("Excel", "accidents_TGL.xlsx ・ accidents_AERIAL.xlsx 生成済"),
        ("サイクル数", f"{CYCLES} サイクル ・利用制限到達 {LIMITS} 回"),
        ("ランナー", "正常終了（全14タスク完了）"),
    ]
    for k, v in rows:
        d.text((M, y), "● " + k, font=FL, fill=INK)
        lns = wrap(d, v, FM, PW - 2 * M - 300)
        for i, ln in enumerate(lns):
            d.text((M + 300, y + 2 + i * 30), ln, font=FM, fill=(50, 50, 50))
        y += 30 * max(1, len(lns)) + 18
    d.text((M, PH - 70), "限定共有・noindex。本レポートは読み取りのみ（収集タスクは既に完了済み）。",
           font=FS, fill=GRAY)
    pages.append(im)


def detail():
    im, d = new_page()
    y = hbar(d, 0, "(A) 事故イラスト収集（完了）")
    d.text((M, y), f"採用 {A_TOTAL}枚（TGL {A_TGL}・高所 {A_AER}）／ img_index.csv {A_TOTAL}行 ／ 消化クエリ {QDONE}",
           font=FM, fill=INK); y += 38
    d.text((M, y), "出尽くし判定: A6（全体重複再排除・通し番号確定）完了＝収集確定。md5で実体重複統合。",
           font=FS, fill=GREEN); y += 50

    y = hbar(d, y, "(B) 事故情報 Excel化（完了）")
    d.text((M, y), f"一次データ走査 {B_SCANNED:,}件（JNIOSH 死亡DB1991-2018＋死傷DB2006-2017・CSV{N_CSV}本）",
           font=FM, fill=INK); y += 36
    y = table(d, M, y, ["群", "件数", "JNIOSH", "あんぜん", "目標(1000)"],
              [["TGL", f"{B_TGL:,}", B_TGL_J, B_TGL_A, "達成 約1.9倍"],
               ["高所", f"{B_AER:,}", B_AER_J, B_AER_A, "達成 約1.1倍"],
               ["合計", f"{B_TOTAL:,}", B_TGL_J + B_AER_J, B_TGL_A + B_AER_A, "—"]],
              [110, 150, 150, 150, 320], rh=42)
    d.text((M, y), "あんぜんサイトDB(B4)で出典URL付き事故を積み増し、両群とも1000件超を達成。", font=FS, fill=GRAY)
    y += 32
    d.text((M, y), "出典: 全件付与（JNIOSHはファイル名+行番号、あんぜんは事例URL）。重複排除済。", font=FS, fill=GRAY)
    y += 50

    d.text((M, y), "■ 事故の型別 件数", font=FL, fill=INK); y += 44
    d.text((M, y), "TGL群（計1,878）", font=FL, fill=BLUE)
    d.text((M + 440, y), "高所群（計1,149）", font=FL, fill=BLUE)
    yy = y + 40; yy2 = y + 40
    for name, n in TGL_CAT:
        d.text((M, yy), f"・{name}", font=FU, fill=INK)
        d.text((M + 400 - d.textlength(str(n), font=FU), yy), str(n), font=FU, fill=INK); yy += 26
    for name, n in AER_CAT:
        d.text((M + 440, yy2), f"・{name}", font=FU, fill=INK)
        d.text((M + 840 - d.textlength(str(n), font=FU), yy2), str(n), font=FU, fill=INK); yy2 += 26
    pages.append(im)


def finish_page():
    im, d = new_page()
    y = hbar(d, 0, "サイクル統計・制限到達状況")
    rows = [
        ("サイクル数（col_*.log）", f"{CYCLES}"),
        ("稼働区間", SPAN),
        ("平均サイクル所要", f"約 {AVG_CYCLE} 分/タスク（約83分 ÷ 14）"),
        ("利用制限到達(usage/rate/429)", f"{LIMITS} 回（自動再開の発生なし）"),
        ("完了/全", f"{DONE_N}/{TOTAL_N}（残 0）"),
    ]
    for k, v in rows:
        d.text((M, y), "● " + k, font=FM, fill=INK)
        d.text((M + 520, y), v, font=FM, fill=(50, 50, 50)); y += 40
    y += 20

    y = hbar(d, y, "終了予想 → 実績（既に完了）")
    d.rectangle([M, y, PW - M, y + 110], fill=(231, 243, 236), outline=GREEN)
    d.text((M + 24, y + 18), "全14タスク完了済み（予想不要）", font=FH, fill=GREEN)
    d.text((M + 24, y + 64), "実完了: 2026-06-14 約20:14 JST ／ 所要 約1時間23分 ／ 制限待ち 0分",
           font=FM, fill=INK)
    y += 140
    note = ("参考：本来の予想式＝平均サイクル(約5.9分)×残タスク＋制限待ち。今回は残0・制限0回のため待ち時間ゼロで完了。"
            "18:50開始→20:14完了。利用制限に一度も到達せず連続稼働した。")
    for ln in wrap(d, note, FS, PW - 2 * M):
        d.text((M, y), ln, font=FS, fill=GRAY); y += 30
    y += 24

    y = hbar(d, y, "成果物一覧（全て生成・push済）")
    for k, v in DELIV:
        d.text((M, y), "● " + k, font=FL, fill=INK)
        for ln in wrap(d, v, FS, PW - 2 * M - 360):
            d.text((M + 360, y + 2), ln, font=FS, fill=(50, 50, 50)); break
        y += 44
    d.text((M, PH - 50), f"進捗レポート {NOW}", font=FU, fill=GRAY)
    pages.append(im)


cover()
detail()
finish_page()
pages[0].save(OUT, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
print("WROTE", OUT, "pages=", len(pages))
