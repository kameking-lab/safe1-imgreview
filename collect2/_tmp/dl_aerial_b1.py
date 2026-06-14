# -*- coding: utf-8 -*-
# A4: 高所事故イラスト バッチ1 download. append-only, dedup by md5. NO deletion.
import os, csv, hashlib, subprocess, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IMGDIR = os.path.join(ROOT, 'img')
INDEX = os.path.join(ROOT, 'img_index.csv')
TSV = os.path.join(os.path.dirname(__file__), 'aerial_b1.tsv')
TMP = os.path.join(os.path.dirname(__file__), 'b1_aerial')
os.makedirs(TMP, exist_ok=True)
IMGBASE = 'https://www.sacl.or.jp/sa7210/wp-content/uploads/disaster/'

# load existing index: md5 set + max seq + existing source urls
existing_md5 = set()
existing_url = set()
maxseq = 0
rows_existing = []
with open(INDEX, encoding='utf-8') as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        if not row: continue
        rows_existing.append(row)
        maxseq = max(maxseq, int(row[0]))
        existing_md5.add(row[5])
        existing_url.add(row[4])
print(f"existing rows={len(rows_existing)} maxseq={maxseq} md5s={len(existing_md5)}")

def magic_ok(p):
    with open(p, 'rb') as fh:
        h = fh.read(12)
    if h[:3] == b'\xff\xd8\xff': return 'jpg'
    if h[:8] == b'\x89PNG\r\n\x1a\n': return 'png'
    if h[:6] in (b'GIF87a', b'GIF89a'): return 'gif'
    return None

new_rows = []
seq = maxseq
batch_md5 = set()
with open(TSV, encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        if not line.strip(): continue
        page, img, atype, desc = line.split('\t')
        url = IMGBASE + img
        out = os.path.join(TMP, img.replace('/', '_'))
        # download (no Chrome, plain curl)
        res = subprocess.run(['curl', '-sL', '-A', 'Mozilla/5.0', '-w', '%{http_code}',
                              '-o', out, url], capture_output=True, text=True)
        code = res.stdout.strip()[-3:]
        if code != '200' or not os.path.exists(out):
            print(f"SKIP http={code} {img}"); continue
        ext = magic_ok(out)
        if not ext:
            print(f"SKIP not-image {img}"); continue
        md5 = hashlib.md5(open(out, 'rb').read()).hexdigest()
        if md5 in existing_md5 or md5 in batch_md5:
            print(f"SKIP dup-md5 {img}"); continue
        batch_md5.add(md5)
        seq += 1
        fn = f"{seq:04d}.{ext}"
        dst = os.path.join(IMGDIR, fn)
        with open(dst, 'wb') as w:
            w.write(open(out, 'rb').read())
        new_rows.append([f"{seq:04d}", fn, '高所', atype, page, md5, desc])
        print(f"ADD {fn} <- {img} [{atype}] {desc[:24]}")

# append to index (append-only; do not rewrite existing rows)
if new_rows:
    with open(INDEX, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for row in new_rows:
            w.writerow(row)
print(f"\nADDED {len(new_rows)} images. new maxseq={seq}")
