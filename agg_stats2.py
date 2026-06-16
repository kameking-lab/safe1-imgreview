# -*- coding: utf-8 -*-
# V1: 死亡(SHIBO)/死傷(SHISYO) 分離集計 + 事故型別ランキング (stats2.md)
# 一次ソース = data/jniosh/parsed/tgl_enriched.jsonl / aerial_enriched.jsonl
# 捏造禁止: db/type フィールドのみで集計。db未設定は「内訳不明」へ。
import json, io, collections

def load(path):
    rows = []
    with io.open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows

def analyze(rows):
    n = len(rows)
    db = collections.Counter()
    for r in rows:
        v = (r.get("db") or "").strip().upper()
        if v in ("SHIBO", "SHISYO"):
            db[v] += 1
        else:
            db["UNKNOWN"] += 1
    # 事故の型別: 死亡/死傷分離 + 合計
    type_shibo = collections.Counter()
    type_shisyo = collections.Counter()
    type_unknown = collections.Counter()
    type_total = collections.Counter()
    for r in rows:
        t = (r.get("type") or "").strip() or "(型不明)"
        v = (r.get("db") or "").strip().upper()
        type_total[t] += 1
        if v == "SHIBO":
            type_shibo[t] += 1
        elif v == "SHISYO":
            type_shisyo[t] += 1
        else:
            type_unknown[t] += 1
    # data_source 別
    ds = collections.Counter()
    for r in rows:
        ds[(r.get("data_source") or "(不明)").strip()] += 1
    return dict(n=n, db=db, type_shibo=type_shibo, type_shisyo=type_shisyo,
               type_unknown=type_unknown, type_total=type_total, ds=ds)

def pct(a, b):
    return (100.0 * a / b) if b else 0.0

def rank_md(counter, total, topn=None):
    items = counter.most_common()
    if topn:
        items = items[:topn]
    lines = ["| 順位 | 事故の型 | 件数 | 割合 |", "|---:|---|---:|---:|"]
    for i, (k, v) in enumerate(items, 1):
        lines.append("| {} | {} | {} | {:.1f}% |".format(i, k, v, pct(v, total)))
    return "\n".join(lines)

def section(title, a):
    n = a["n"]; db = a["db"]
    shibo = db.get("SHIBO", 0); shisyo = db.get("SHISYO", 0); unk = db.get("UNKNOWN", 0)
    out = []
    out.append("## {}".format(title))
    out.append("")
    out.append("- 総レコード数: **{}**".format(n))
    out.append("- 死亡災害DB (db=SHIBO): **{}** 件 ({:.1f}%)".format(shibo, pct(shibo, n)))
    out.append("- 死傷災害DB (db=SHISYO): **{}** 件 ({:.1f}%)".format(shisyo, pct(shisyo, n)))
    if unk:
        out.append("- db未設定（内訳不明・正直表記）: **{}** 件 ({:.1f}%)".format(unk, pct(unk, n)))
    out.append("- データ出所内訳: " + ", ".join("{}={}".format(k, v) for k, v in a["ds"].most_common()))
    out.append("")
    out.append("### 事故の型別ランキング（合計＝SHIBO+SHISYO+内訳不明）")
    out.append(rank_md(a["type_total"], n))
    out.append("")
    out.append("### 事故の型別ランキング（死亡 SHIBO のみ）n={}".format(shibo))
    if shibo:
        out.append(rank_md(a["type_shibo"], shibo))
    else:
        out.append("（SHIBOレコードなし）")
    out.append("")
    out.append("### 事故の型別ランキング（死傷 SHISYO のみ）n={}".format(shisyo))
    if shisyo:
        out.append(rank_md(a["type_shisyo"], shisyo))
    else:
        out.append("（SHISYOレコードなし）")
    out.append("")
    if unk:
        out.append("### 事故の型別（db未設定・内訳不明分のみ）n={}".format(unk))
        out.append(rank_md(a["type_unknown"], unk))
        out.append("")
    return "\n".join(out), dict(shibo=shibo, shisyo=shisyo, unk=unk,
                                top3_total=a["type_total"].most_common(3),
                                top3_shibo=a["type_shibo"].most_common(3),
                                top3_shisyo=a["type_shisyo"].most_common(3))

tgl = analyze(load("data/jniosh/parsed/tgl_enriched.jsonl"))
aer = analyze(load("data/jniosh/parsed/aerial_enriched.jsonl"))

doc = []
doc.append("# stats2.md — TGL / 高所作業車 事故統計（手元データ一次集計）")
doc.append("")
doc.append("一次ソース: `data/jniosh/parsed/tgl_enriched.jsonl`・`aerial_enriched.jsonl`（1行1事故）。")
doc.append("集計キー: `db`（SHIBO=死亡災害DB / SHISYO=死傷災害DB / 未設定=内訳不明）, `type`（事故の型）。")
doc.append("**捏造なし**: 各レコードの実フィールドを件数カウントしたのみ。db未設定分は「内訳不明」として分離表記。")
doc.append("")
s1, sum_tgl = section("TGL（テールゲートリフター関連）", tgl)
s2, sum_aer = section("高所作業車（AERIAL）", aer)
doc.append(s1)
doc.append(s2)

# 確定サマリー行
def t3(lst):
    return "、".join("{}({}件)".format(k, v) for k, v in lst) if lst else "なし"
doc.append("## 確定サマリー（数値確定）")
doc.append("")
doc.append("| 区分 | 死亡(SHIBO) | 死傷(SHISYO) | 内訳不明 | 事故型トップ3(合計) |")
doc.append("|---|---:|---:|---:|---|")
doc.append("| TGL | {} | {} | {} | {} |".format(sum_tgl["shibo"], sum_tgl["shisyo"], sum_tgl["unk"], t3(sum_tgl["top3_total"])))
doc.append("| 高所 | {} | {} | {} | {} |".format(sum_aer["shibo"], sum_aer["shisyo"], sum_aer["unk"], t3(sum_aer["top3_total"])))
doc.append("")

with io.open("stats2.md", "w", encoding="utf-8") as f:
    f.write("\n".join(doc) + "\n")

# JSON sidecar for downstream chart steps
side = dict(
    tgl=dict(n=tgl["n"], db=dict(tgl["db"]), type_total=dict(tgl["type_total"]),
             type_shibo=dict(tgl["type_shibo"]), type_shisyo=dict(tgl["type_shisyo"]),
             type_unknown=dict(tgl["type_unknown"])),
    aerial=dict(n=aer["n"], db=dict(aer["db"]), type_total=dict(aer["type_total"]),
                type_shibo=dict(aer["type_shibo"]), type_shisyo=dict(aer["type_shisyo"]),
                type_unknown=dict(aer["type_unknown"])),
)
with io.open("stats2_data.json", "w", encoding="utf-8") as f:
    json.dump(side, f, ensure_ascii=False, indent=1)

print("TGL:", dict(tgl["db"]), "| 高所:", dict(aer["db"]))
print("TGL top3:", t3(sum_tgl["top3_total"]))
print("AER top3:", t3(sum_aer["top3_total"]))
