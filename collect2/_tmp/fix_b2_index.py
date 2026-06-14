# -*- coding: utf-8 -*-
# Correct 事故種類 and 説明 for rows 0063-0073 (A5 batch) using the saved SAI_DET pages.
# Preserves rows 0001-0062 byte-identical; only rewrites the 11 new rows' type+desc.
import re, csv, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INDEX = 'collect2/img_index.csv'
HTMLDIR = 'collect2/_tmp/b2_aerial'

TYPE_MAP = [
    ('はさまれ', 'はさまれ・巻き込まれ'), ('巻き込まれ', 'はさまれ・巻き込まれ'),
    ('感電', '感電'), ('激突され', '激突'), ('激突', '激突'),
    ('交通事故', '激突'), ('転倒', '転倒'),
    ('飛来', '飛来・落下'), ('落下', '飛来・落下'),
    ('墜落', '墜落・転落'), ('転落', '墜落・転落'),
]

def parse(jno):
    h = open(f'{HTMLDIR}/sai_{jno}.html', 'rb').read().decode('cp932', 'replace')
    text = re.sub(r'<[^>]+>', ' ', h); text = re.sub(r'\s+', ' ', text)
    t = re.search(r'事故の型\)\s*([^ <　]+)', text)
    raw_type = t.group(1) if t else ''
    atype = '墜落・転落'
    for k, v in TYPE_MAP:
        if k in raw_type:
            atype = v; break
    # description: prefer "この災害は…。" else first 。-sentence mentioning the accident/車
    desc = ''
    m = re.search(r'(この災害は[^。]{8,110}。)', text)
    if m:
        desc = m.group(1)
    else:
        for mm in re.finditer(r'([^。\)＞> ][^。]{14,110}。)', text):
            s = mm.group(1)
            if ('作業車' in s or 'バケット' in s or 'バスケット' in s or '搬器' in s) and \
               any(w in s for w in ['墜落','転落','挟','はさ','感電','激突','転倒','落下','逸走','死亡','被災','巻き込']):
                desc = s; break
    desc = desc.strip()
    if len(desc) > 90:
        desc = desc[:88] + '…'
    if not desc:
        desc = f'高所作業車による労働災害（{atype}・事例No.{jno}）'
    return atype, desc

# read index
with open(INDEX, encoding='utf-8') as f:
    rows = list(csv.reader(f))
header = rows[0]
out = [header]
for row in rows[1:]:
    if not row:
        continue
    seq = int(row[0])
    if 63 <= seq <= 73:
        m = re.search(r'joho_no=(\d+)', row[4])
        jno = m.group(1)
        atype, desc = parse(jno)
        row = [row[0], row[1], row[2], atype, row[4], row[5], desc]
        print(f"{row[0]} joho={jno} -> [{atype}] {desc}")
    out.append(row)

with open(INDEX, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    for row in out:
        w.writerow(row)
print(f"\nrewrote index, total rows={len(out)-1}")
