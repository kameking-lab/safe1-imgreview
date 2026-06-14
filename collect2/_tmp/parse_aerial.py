# -*- coding: utf-8 -*-
# Parse hiyari category pages, find 高所作業車-related cases. No downloads here.
import re, glob, os, sys

KEYS = ['高所作業車', 'ブーム', '作業床', 'バスケット', '高所作業', 'アウトリガ', 'スカイ', '垂直昇降']
# exclude obvious non-aerial false hits handled later by review

cat_files = sorted(glob.glob('cat*.html'))
rows = []  # (case_no, accident_type, img, alt, srcfile)
case_re = re.compile(
    r'<a href="hiyari/(hiy_\d+\.html)"[^>]*>\s*<div class="photoFlame">\s*'
    r'<img src="hiyari/(image/[^"]+)"\s+alt="([^"]*)"',
    re.S)
h3_re = re.compile(r'<h3>(.*?)</h3>', re.S)

for f in cat_files:
    raw = open(f, 'rb').read().decode('shift_jis', 'replace')
    # build position->accident-type map from h3 headers
    h3s = [(m.start(), re.sub('<[^>]+>', '', m.group(1)).strip()) for m in h3_re.finditer(raw)]
    for m in case_re.finditer(raw):
        pos = m.start()
        atype = ''
        for hp, ht in h3s:
            if hp < pos:
                atype = ht
            else:
                break
        case = m.group(1)
        img = m.group(2)
        alt = re.sub(r'\s+', ' ', m.group(3)).strip()
        rows.append((case, atype, img, alt, f))

# dedup by case_no
seen = {}
for case, atype, img, alt, f in rows:
    if case not in seen:
        seen[case] = (case, atype, img, alt, f)

aerial = []
for case, atype, img, alt, f in seen.values():
    if any(k in alt for k in KEYS):
        aerial.append((case, atype, img, alt, f))

print(f"total cases parsed: {len(seen)}  aerial-matching: {len(aerial)}")
print("="*80)
for case, atype, img, alt, f in sorted(aerial):
    print(f"{case}\t[{atype}]\t{img}\t{alt}")
