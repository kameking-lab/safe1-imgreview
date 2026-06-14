# -*- coding: utf-8 -*-
"""B2: テールゲートリフター(TGL)群の抽出・重複排除・カテゴリ(事故の型)付与。

入力: data/jniosh/parsed/jniosh_all.jsonl (B1の正規化済み全件)
出力: data/jniosh/parsed/tgl_extracted.jsonl  (1件1行・dedup済・category付与)
      data/jniosh/parsed/tgl_summary.json     (件数・カテゴリ別・年別・キーワード別)
append-only / 既存を壊さない: 出力は新ファイル名。再実行で上書き生成は同一結果(冪等)。
"""
import json
import hashlib
import os

SRC = "data/jniosh/parsed/jniosh_all.jsonl"
OUT_JSONL = "data/jniosh/parsed/tgl_extracted.jsonl"
OUT_SUMMARY = "data/jniosh/parsed/tgl_summary.json"

# 高精度TGLキーワード（テールゲートリフター/パワーゲート系）。
# probe結果より、リフター/昇降機/昇降装置/昇降板(単独)はエレベータ・ドロップリフタ・
# 木工昇降盤など非TGLが大半のため除外。パワーリフト/パワーゲート/テールゲートはTGLが大半。
TGL_KEYWORDS = [
    "テールゲート",        # テールゲートリフター/リフタを内包
    "パワーゲート",
    "パワーリフト",
    "リフトゲート",
    "テールリフト",
    "荷台昇降",
    "床面昇降",
    "後部昇降",
    "昇降テール",
    "昇降ゲート",
    "昇降装置付",          # 昇降装置付きトラック=TGL
    "昇降板付",            # 昇降板付きトラック=TGL
    "格納式パワーゲート",
    "格納式テールゲート",
]


def category_of(rec):
    """事故の型(type)をカテゴリとする。空なら『その他・不明』。"""
    t = (rec.get("type") or "").strip()
    return t if t else "その他・不明"


def dedup_key(rec):
    """(発生年月+業種+事故の型+災害発生状況)のハッシュ。日は元データに無いため年月。"""
    parts = [
        rec.get("seireki", ""), rec.get("tsuki", ""),
        rec.get("gyosyu_L", ""), rec.get("gyosyu_M", ""),
        rec.get("type", ""), rec.get("jokyo", ""),
    ]
    return hashlib.md5("␟".join(parts).encode("utf-8")).hexdigest()


def main():
    seen = set()
    kept = []
    kw_hits = {k: 0 for k in TGL_KEYWORDS}
    n = 0
    raw_match = 0
    with open(SRC, encoding="utf-8") as f:
        for line in f:
            n += 1
            r = json.loads(line)
            blob = "".join([
                r.get("jokyo", ""), r.get("kiin_S", ""),
                r.get("kiin_M", ""), r.get("kiin_L", ""),
            ])
            matched = [k for k in TGL_KEYWORDS if k in blob]
            if not matched:
                continue
            raw_match += 1
            for k in matched:
                kw_hits[k] += 1
            key = dedup_key(r)
            if key in seen:
                continue
            seen.add(key)
            out = dict(r)
            out["group"] = "TGL"
            out["category"] = category_of(r)
            out["matched_keywords"] = matched
            out["dedup_key"] = key
            kept.append(out)

    by_cat = {}
    by_year = {}
    by_db = {}
    for r in kept:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
        by_year[r["seireki"]] = by_year.get(r["seireki"], 0) + 1
        by_db[r["db"]] = by_db.get(r["db"], 0) + 1

    with open(OUT_JSONL, "w", encoding="utf-8", newline="\n") as o:
        for r in kept:
            o.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary = {
        "scanned": n,
        "raw_keyword_matches": raw_match,
        "after_dedup": len(kept),
        "duplicates_removed": raw_match - len(kept),
        "keyword_hits": kw_hits,
        "by_category": dict(sorted(by_cat.items(), key=lambda x: -x[1])),
        "by_year": dict(sorted(by_year.items())),
        "by_db": by_db,
    }
    with open(OUT_SUMMARY, "w", encoding="utf-8", newline="\n") as s:
        json.dump(summary, s, ensure_ascii=False, indent=2)

    print("scanned", n)
    print("raw_keyword_matches", raw_match)
    print("after_dedup", len(kept))
    print("by_category:")
    for k, v in summary["by_category"].items():
        print("  ", v, k)


if __name__ == "__main__":
    main()
