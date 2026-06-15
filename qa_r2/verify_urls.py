# -*- coding: utf-8 -*-
# QA2: re-verify adopted source URLs — confirm body matches the accident mechanism.
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# id -> (encoding, [required keyword groups]).  Each group is a list of synonyms;
# the group passes if ANY synonym is present. All groups must pass.
CHECKS = {
    "0001":  ("cp932", [["テールゲートリフター"], ["転落", "落ち"], ["荷台"]]),
    "0002":  ("cp932", [["テールゲートリフター"], ["挟", "はさ"], ["ゲート"]]),
    "0003":  ("cp932", [["テールゲートリフター"], ["落ち", "転落"], ["台車"]]),
    "0017":  ("cp932", [["昇降装置"], ["台車"], ["下敷き", "落下"]]),
    "0019":  ("cp932", [["カーゴ台車", "台車"], ["ゲート"], ["荷卸", "荷下ろし", "荷下し"]]),
    "0040":  ("utf-8", [["高所作業車"], ["クレーン"], ["はさ", "挟"]]),
    "0041":  ("utf-8", [["高所作業車"], ["バケット"], ["転落", "墜落"]]),
    "0042":  ("utf-8", [["高所作業車"], ["高架橋"], ["はさ", "挟"]]),
    "0042b": ("cp932", [["高所作業車"], ["高架橋"], ["はさ", "挟"]]),
    "0043":  ("utf-8", [["高所作業車"], ["バケット", "作業床"], ["墜落", "滑"]]),
    "0044":  ("utf-8", [["高所作業車"], ["作業床"], ["手すり", "身を乗り出", "上半身"], ["墜落", "転落"]]),
    "0046":  ("utf-8", [["高所作業車"], ["天井"], ["はさ", "挟"], ["胸"]]),
    "0050":  ("utf-8", [["高所作業車"], ["バスケット"], ["コンテナ"], ["乗り移", "落下", "墜落"]]),
    "0052":  ("utf-8", [["高所作業車"], ["傾斜"], ["転倒"]]),
    "0054":  ("utf-8", [["高所作業車"], ["ダクト"], ["手すり"], ["墜落"]]),
    "0057":  ("utf-8", [["高所作業車"], ["外壁", "建物"], ["作業床"], ["墜落"]]),
    "0060":  ("utf-8", [["高所作業車"], ["送電線"], ["感電"]]),
    "0071":  ("cp932", [["高所作業車"], ["下がり壁", "壁"], ["手すり"], ["はさ", "挟"]]),
}

results = []
all_ok = True
for cid, (enc, groups) in CHECKS.items():
    path = os.path.join(HERE, cid + ".html")
    if not os.path.exists(path):
        results.append((cid, "MISSING FILE", []))
        all_ok = False
        continue
    raw = open(path, "rb").read()
    try:
        text = raw.decode(enc, errors="replace")
    except Exception as e:
        results.append((cid, "DECODE-FAIL:%s" % e, []))
        all_ok = False
        continue
    # collapse tags lightly for robustness, but keep raw text searching too
    missing = []
    detail = []
    for grp in groups:
        hit = next((w for w in grp if w in text), None)
        if hit is None:
            missing.append("/".join(grp))
        else:
            cnt = text.count(hit)
            detail.append("%s=%d" % (hit, cnt))
    status = "OK" if not missing else ("MISS:" + ", ".join(missing))
    if missing:
        all_ok = False
    results.append((cid, status, detail))

print("=== QA2 URL body re-verification (decoded, keyword match) ===")
for cid, status, detail in results:
    print("%-6s %-40s %s" % (cid, status, " ".join(detail)))
print()
print("ALL_OK" if all_ok else "SOME_FAILED")
