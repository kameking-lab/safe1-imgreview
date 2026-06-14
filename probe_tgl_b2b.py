# -*- coding: utf-8 -*-
"""B2 probe2: sample ambiguous keyword contexts (read-only). Writes to file UTF-8."""
import json

SRC = "data/jniosh/parsed/jniosh_all.jsonl"
OUT = "probe_tgl_b2b_out.txt"
amb = ["リフター", "昇降機", "昇降装置", "格納式", "パワーリフト", "昇降板"]
ctx = ["トラック", "荷台", "荷役", "貨物", "積込", "積み込", "積み下", "積卸", "車両", "ト ラック"]
samples = {k: [] for k in amb}
with open(SRC, encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        jokyo = r.get("jokyo", "")
        blob = jokyo + r.get("kiin_S", "") + r.get("kiin_M", "") + r.get("kiin_L", "")
        for k in amb:
            if k in blob and len(samples[k]) < 12:
                has_ctx = any(c in jokyo for c in ctx)
                samples[k].append((has_ctx, r.get("kiin_M", ""), jokyo[:90]))
with open(OUT, "w", encoding="utf-8", newline="\n") as o:
    for k in amb:
        o.write(f"==== {k} ====\n")
        for hc, kiin, j in samples[k]:
            o.write(f"[ctx={hc}] kiin={kiin} | {j}\n")
        o.write("\n")
print("wrote", OUT)
