# -*- coding: utf-8 -*-
"""B3: 高所作業車(AERIAL)群の抽出・重複排除・カテゴリ(事故の型)付与。

入力: data/jniosh/parsed/jniosh_all.jsonl (B1の正規化済み全件)
出力: data/jniosh/parsed/aerial_extracted.jsonl  (1件1行・dedup済・category付与)
      data/jniosh/parsed/aerial_summary.json     (件数・カテゴリ別・年別・キーワード別)
append-only / 既存を壊さない: 出力は新ファイル名。再実行で上書き生成は同一結果(冪等)。

抽出方針（高精度）:
  probe(probe_aerial_b3b.json)で確定:
    - 起因物コード146 = 「高所作業車」(kiin_S_code=="146") … 426件
    - キーワード「高所作業車」が状況/起因物本文に出現 … 877件（うち451件は
      起因物が送配電線・トラック・建築物等＝高所作業車が関与した災害で正当）
  これを核に、曖昧語(ブーム/バスケット/作業床/ゴンドラ等)は「高所」共起時のみ採用し
  クレーンのブーム・足場の作業床など非高所作業車を除外する。
"""
import json
import hashlib

SRC = "data/jniosh/parsed/jniosh_all.jsonl"
OUT_JSONL = "data/jniosh/parsed/aerial_extracted.jsonl"
OUT_SUMMARY = "data/jniosh/parsed/aerial_summary.json"

# 常に採用（高所作業車そのものを指す特異語）
AERIAL_PRIMARY = ["高所作業車", "高所作業台"]
# 起因物コード146=高所作業車（本文に語が無くてもコードで確実に拾う）
AERIAL_KIIN_CODE = "146"
# 曖昧語：単独ではクレーン等を含むため「高所」共起時のみ採用
AERIAL_CONTEXT = [
    "バスケット", "作業床", "ゴンドラ", "リフト車",
    "垂直昇降", "伸縮ブーム", "屈折ブーム", "ブーム",
]
ALL_KEYS = AERIAL_PRIMARY + AERIAL_CONTEXT + ["起因物コード146"]


def category_of(rec):
    t = (rec.get("type") or "").strip()
    return t if t else "その他・不明"


def dedup_key(rec):
    parts = [
        rec.get("seireki", ""), rec.get("tsuki", ""),
        rec.get("gyosyu_L", ""), rec.get("gyosyu_M", ""),
        rec.get("type", ""), rec.get("jokyo", ""),
    ]
    return hashlib.md5("␟".join(parts).encode("utf-8")).hexdigest()


def matches(r):
    """戻り値: (matched:bool, matched_keys:list)"""
    blob = "".join([
        r.get("jokyo", ""), r.get("kiin_S", ""),
        r.get("kiin_M", ""), r.get("kiin_L", ""),
    ])
    keys = []
    for p in AERIAL_PRIMARY:
        if p in blob:
            keys.append(p)
    if r.get("kiin_S_code", "") == AERIAL_KIIN_CODE:
        keys.append("起因物コード146")
    if "高所" in blob:
        for c in AERIAL_CONTEXT:
            if c in blob:
                keys.append(c)
    return (len(keys) > 0), keys


def main():
    seen = set()
    kept = []
    kw_hits = {k: 0 for k in ALL_KEYS}
    n = 0
    raw_match = 0
    with open(SRC, encoding="utf-8") as f:
        for line in f:
            n += 1
            r = json.loads(line)
            ok, keys = matches(r)
            if not ok:
                continue
            raw_match += 1
            for k in keys:
                kw_hits[k] += 1
            key = dedup_key(r)
            if key in seen:
                continue
            seen.add(key)
            out = dict(r)
            out["group"] = "AERIAL"
            out["category"] = category_of(r)
            out["matched_keywords"] = keys
            out["dedup_key"] = key
            kept.append(out)

    by_cat, by_year, by_db = {}, {}, {}
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


if __name__ == "__main__":
    main()
