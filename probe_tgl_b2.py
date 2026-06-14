# -*- coding: utf-8 -*-
"""B2 probe: count TGL-related keyword hits in jniosh_all.jsonl (read-only)."""
import json

SRC = "data/jniosh/parsed/jniosh_all.jsonl"
kws = [
    "テールゲート", "テールゲートリフタ", "テールゲートリフター", "パワーゲート",
    "昇降装置", "昇降板", "リフトゲート", "荷台昇降", "昇降機", "格納式",
    "床面昇降", "テールリフト", "パワーリフト", "後部昇降", "リフター",
    "リフト付", "昇降テール",
]
cnt = {k: 0 for k in kws}
any_cnt = 0
n = 0
with open(SRC, encoding="utf-8") as f:
    for line in f:
        n += 1
        r = json.loads(line)
        blob = "".join([
            r.get("jokyo", ""), r.get("kiin_S", ""),
            r.get("kiin_M", ""), r.get("kiin_L", ""),
        ])
        hit = False
        for k in kws:
            if k in blob:
                cnt[k] += 1
                hit = True
        if hit:
            any_cnt += 1
print("total lines", n)
for k in kws:
    print(k, cnt[k])
print("ANY", any_cnt)
