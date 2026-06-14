# -*- coding: utf-8 -*-
"""B1: JNIOSH 労災DB CSV群を正規化して 1本の JSONL に集約する。
入力 : data/jniosh/SHIBO_*.csv (死亡災害DB H3-H30) / SHISYO_*.csv (死傷DB H18-H29)
        文字コード=UTF-8(BOM可)。SHIBO=22列, SHISYO=23列(末尾に年齢)。位置は共通。
出力 : data/jniosh/parsed/jniosh_all.jsonl  (1行=1災害, B2/B3 が grep する一次正規化データ)
        data/jniosh/parsed/parse_summary.json (件数サマリ)
再実行安全: 出力ディレクトリ/ファイルが既存でも決定的に再生成（追加のみ・元CSVは不変）。
"""
import csv, glob, json, os, sys

SRC_DIR = "data/jniosh"
OUT_DIR = os.path.join(SRC_DIR, "parsed")

# 位置インデックス（SHIBO/SHISYO 共通の先頭22列）
IDX = {
    "id": 0, "seireki": 1, "nengo": 2, "nen": 3, "tsuki": 4,
    "jikan": 5, "jokyo": 6,
    "gyosyu_L_code": 7, "gyosyu_L": 8,
    "gyosyu_M_code": 9, "gyosyu_M": 10,
    "gyosyu_S_code": 11, "gyosyu_S": 12,
    "kibo": 13,
    "kiin_L_code": 14, "kiin_L": 15,
    "kiin_M_code": 16, "kiin_M": 17,
    "kiin_S_code": 18, "kiin_S": 19,
    "type_code": 20, "type": 21,
}


def parse_file(path):
    base = os.path.basename(path)
    db = "SHIBO" if base.startswith("SHIBO") else "SHISYO"
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        r = csv.reader(fh)
        hdr = next(r, None)
        for lineno, row in enumerate(r, start=2):  # 2 = 1件目のデータ行
            if len(row) < 22:
                continue
            rec = {
                "db": db,
                "src_file": base,
                "src_row": lineno,
                "seireki": row[IDX["seireki"]],
                "nen": row[IDX["nen"]],
                "tsuki": row[IDX["tsuki"]],
                "gyosyu_L": row[IDX["gyosyu_L"]],
                "gyosyu_M": row[IDX["gyosyu_M"]],
                "kiin_L": row[IDX["kiin_L"]],
                "kiin_L_code": row[IDX["kiin_L_code"]],
                "kiin_M": row[IDX["kiin_M"]],
                "kiin_M_code": row[IDX["kiin_M_code"]],
                "kiin_S": row[IDX["kiin_S"]],
                "kiin_S_code": row[IDX["kiin_S_code"]],
                "type": row[IDX["type"]],
                "type_code": row[IDX["type_code"]],
                "jokyo": row[IDX["jokyo"]],
            }
            rows.append(rec)
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    files = sorted(
        f for f in glob.glob(os.path.join(SRC_DIR, "*.csv"))
        if "SHUSEI" not in os.path.basename(f)
    )
    out_path = os.path.join(OUT_DIR, "jniosh_all.jsonl")
    summary = {"files": {}, "total": 0, "by_db": {"SHIBO": 0, "SHISYO": 0},
               "by_year": {}}
    total = 0
    with open(out_path, "w", encoding="utf-8", newline="\n") as out:
        for f in files:
            recs = parse_file(f)
            for rec in recs:
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                yr = rec["seireki"]
                summary["by_year"][yr] = summary["by_year"].get(yr, 0) + 1
            base = os.path.basename(f)
            summary["files"][base] = len(recs)
            db = "SHIBO" if base.startswith("SHIBO") else "SHISYO"
            summary["by_db"][db] += len(recs)
            total += len(recs)
            print(f"{base}: {len(recs)} rows")
    summary["total"] = total
    with open(os.path.join(OUT_DIR, "parse_summary.json"), "w",
              encoding="utf-8", newline="\n") as sf:
        json.dump(summary, sf, ensure_ascii=False, indent=2)
    print(f"--- TOTAL {total} records -> {out_path}")
    print(f"SHIBO={summary['by_db']['SHIBO']}  SHISYO={summary['by_db']['SHISYO']}")


if __name__ == "__main__":
    sys.exit(main())
