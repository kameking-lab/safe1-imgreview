# -*- coding: utf-8 -*-
"""B3 probe2: identify kiin code(s) for 高所作業車 and measure precise sets.
Writes UTF-8 report to probe_aerial_b3b.json to avoid console mojibake."""
import json
from collections import Counter

SRC = "data/jniosh/parsed/jniosh_all.jsonl"

KW_AERIAL_CAR = "高所作業車"   # specific aerial work platform/boom lift

# code -> sample kiin_S text, count, for codes whose kiin text contains 高所
code_text = {}   # (level,code) -> Counter of texts
code_count = Counter()
kw_car = 0
kw_car_codes = Counter()       # kiin_S_code distribution among 高所作業車 keyword hits
all_high_kiin = Counter()      # any kiin text containing 高所
n = 0
with open(SRC, encoding="utf-8") as f:
    for line in f:
        n += 1
        r = json.loads(line)
        for lvl in ("kiin_S", "kiin_M", "kiin_L"):
            txt = r.get(lvl, "")
            code = r.get(lvl + "_code", "")
            if "高所" in txt:
                all_high_kiin[(lvl, code, txt)] += 1
        blob = "".join([r.get("jokyo", ""), r.get("kiin_S", ""),
                        r.get("kiin_M", ""), r.get("kiin_L", "")])
        if KW_AERIAL_CAR in blob:
            kw_car += 1
            kw_car_codes[(r.get("kiin_S_code", ""), r.get("kiin_S", ""))] += 1

report = {
    "total": n,
    "kw_高所作業車_hits": kw_car,
    "kiin_texts_containing_高所 (level,code,text)->count": [
        {"lc": list(k), "n": v} for k, v in all_high_kiin.most_common(40)
    ],
    "kw_高所作業車__kiinS_code_distribution": [
        {"code_text": list(k), "n": v} for k, v in kw_car_codes.most_common(25)
    ],
}
with open("probe_aerial_b3b.json", "w", encoding="utf-8", newline="\n") as o:
    json.dump(report, o, ensure_ascii=False, indent=2)
print("done", n)
