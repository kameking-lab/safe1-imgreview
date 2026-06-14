# -*- coding: utf-8 -*-
"""B3 probe: show one record + count aerial(高所作業車)関連 keyword hits (read-only)."""
import json

SRC = "data/jniosh/parsed/jniosh_all.jsonl"

# first record for field inspection
with open(SRC, encoding="utf-8") as f:
    first = json.loads(f.readline())
print("=== sample record keys ===")
print(list(first.keys()))
print("=== sample record ===")
print(json.dumps(first, ensure_ascii=False, indent=2))

kws = [
    "高所作業車", "高所作業者", "高所作業", "作業床", "バスケット",
    "ブーム", "ゴンドラ", "リフト車", "車両系建設機械（高所作業車）",
    "高所作業台", "垂直昇降", "伸縮ブーム", "屈折ブーム", "アウトリガ",
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
print("=== total lines", n, "===")
for k in kws:
    print(k, cnt[k])
print("ANY", any_cnt)
