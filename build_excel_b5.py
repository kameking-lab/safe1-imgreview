# -*- coding: utf-8 -*-
# B5: enriched JSONL -> Excel (TGL / AERIAL + 集計シート)
# append-only: 既存があれば上書きしない（新ファイル名で出す）。画像生成なし・収集物の整形のみ。
import json, os, sys
from collections import Counter, OrderedDict
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

BASE = os.path.dirname(os.path.abspath(__file__))
PARSED = os.path.join(BASE, "data", "jniosh", "parsed")
OUTDIR = os.path.join(BASE, "data_xlsx")
os.makedirs(OUTDIR, exist_ok=True)

SRC = {
    "TGL":    os.path.join(PARSED, "tgl_enriched.jsonl"),
    "AERIAL": os.path.join(PARSED, "aerial_enriched.jsonl"),
}

HEADERS = ["通し番号", "カテゴリ(事故の型)", "発生年", "業種", "起因物",
           "災害発生状況(全文)", "出典", "データ源"]

def load(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def gyosyu(r):
    parts = [r.get("gyosyu_L", ""), r.get("gyosyu_M", "")]
    parts = [p for p in parts if p]
    return " / ".join(OrderedDict.fromkeys(parts))

def kiin(r):
    parts = [r.get("kiin_L", ""), r.get("kiin_M", ""), r.get("kiin_S", "")]
    parts = [p for p in parts if p]
    return " / ".join(OrderedDict.fromkeys(parts))

def shutten(r):
    fileref = "{}:{}".format(r.get("src_file", ""), r.get("src_row", ""))
    url = r.get("source_url", "")
    return "{} | {}".format(fileref, url) if url else fileref

def build_book(group, rows):
    # 出典URL必須: source_url が無い行は除外
    rows = [r for r in rows if r.get("source_url")]
    # 安定ソート: 発生年 -> カテゴリ
    rows.sort(key=lambda r: (str(r.get("seireki", "")), str(r.get("category", ""))))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "事故一覧"

    head_fill = PatternFill("solid", fgColor="1F4E78")
    head_font = Font(bold=True, color="FFFFFF")
    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.fill = head_fill
        cell.font = head_font
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"

    for i, r in enumerate(rows, 1):
        ws.cell(row=i + 1, column=1, value=i)
        ws.cell(row=i + 1, column=2, value=r.get("category", ""))
        ws.cell(row=i + 1, column=3, value=r.get("seireki", ""))
        ws.cell(row=i + 1, column=4, value=gyosyu(r))
        ws.cell(row=i + 1, column=5, value=kiin(r))
        ws.cell(row=i + 1, column=6, value=r.get("jokyo", ""))
        ws.cell(row=i + 1, column=7, value=shutten(r))
        ws.cell(row=i + 1, column=8, value=r.get("data_source", ""))

    widths = [8, 18, 8, 26, 26, 70, 60, 10]
    for c, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    # 集計シート
    agg = wb.create_sheet("集計")
    cat = Counter(r.get("category", "") for r in rows)
    year = Counter(str(r.get("seireki", "")) for r in rows)
    ds = Counter(r.get("data_source", "") for r in rows)

    def write_table(ws, start_row, title, counter, key_label, sort_by_key=False):
        ws.cell(row=start_row, column=1, value=title).font = Font(bold=True)
        ws.cell(row=start_row + 1, column=1, value=key_label).font = Font(bold=True)
        ws.cell(row=start_row + 1, column=2, value="件数").font = Font(bold=True)
        items = sorted(counter.items()) if sort_by_key else counter.most_common()
        r = start_row + 2
        for k, v in items:
            ws.cell(row=r, column=1, value=k)
            ws.cell(row=r, column=2, value=v)
            r += 1
        ws.cell(row=r, column=1, value="合計").font = Font(bold=True)
        ws.cell(row=r, column=2, value=sum(counter.values())).font = Font(bold=True)
        return r + 2

    agg.cell(row=1, column=1, value="{} 事故情報 集計".format(group)).font = Font(bold=True, size=14)
    agg.cell(row=2, column=1, value="総件数")
    agg.cell(row=2, column=2, value=len(rows))
    nxt = write_table(agg, 4, "■ カテゴリ(事故の型)別", cat, "カテゴリ")
    nxt = write_table(agg, nxt, "■ データ源別", ds, "データ源")
    nxt = write_table(agg, nxt, "■ 発生年別", year, "発生年", sort_by_key=True)
    agg.column_dimensions["A"].width = 22
    agg.column_dimensions["B"].width = 12

    return wb, len(rows), cat, ds

def main():
    summary = {}
    for group, path in SRC.items():
        rows = load(path)
        wb, n, cat, ds = build_book(group, rows)
        out = os.path.join(OUTDIR, "accidents_{}.xlsx".format(group))
        if os.path.exists(out):
            print("SKIP (exists, append-only):", out)
        else:
            wb.save(out)
            print("WROTE:", out, "rows=", n)
        summary[group] = {"rows": n, "by_category": dict(cat.most_common()),
                          "by_data_source": dict(ds.most_common())}
    sp = os.path.join(OUTDIR, "b5_summary.json")
    if not os.path.exists(sp):
        with open(sp, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print("WROTE:", sp)
    else:
        print("SKIP (exists):", sp)
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == "__main__":
    main()
