# -*- coding: utf-8 -*-
# A5: 高所事故イラスト バッチ2. anzeninfo 労働災害事例DB(SAI_DET) の発生状況図サムネを収集。
# append-only, dedup by md5, NO deletion. category=高所.
import os, csv, hashlib, subprocess, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IMGDIR = os.path.join(ROOT, 'img')
INDEX = os.path.join(ROOT, 'img_index.csv')
TMP = os.path.join(os.path.dirname(__file__), 'b2_aerial')
os.makedirs(TMP, exist_ok=True)
BASE = 'https://anzeninfo.mhlw.go.jp'

JOHO = [401,447,507,549,648,724,728,100010,100076,100094,100432,101037,101240,101377,101412,101529]

# load existing index
existing_md5 = set(); existing_url = set(); maxseq = 0; nexist = 0
with open(INDEX, encoding='utf-8') as f:
    r = csv.reader(f); next(r)
    for row in r:
        if not row: continue
        nexist += 1
        maxseq = max(maxseq, int(row[0]))
        existing_md5.add(row[5]); existing_url.add(row[4])
print(f"existing rows={nexist} maxseq={maxseq} md5s={len(existing_md5)}")

def magic_ok(p):
    with open(p,'rb') as fh: h = fh.read(12)
    if h[:3]==b'\xff\xd8\xff': return 'jpg'
    if h[:8]==b'\x89PNG\r\n\x1a\n': return 'png'
    if h[:6] in (b'GIF87a',b'GIF89a'): return 'gif'
    return None

TYPES = ['墜落・転落','転倒','激突され','激突','飛来・落下','崩壊・倒壊','はさまれ・巻き込まれ',
         '切れ・こすれ','感電','爆発','破裂','火災','交通事故','動作の反動・無理な動作']
def classify(text):
    if '感電' in text: return '感電'
    if 'はさ' in text or '挟' in text or '巻き込' in text: return 'はさまれ・巻き込まれ'
    if '激突' in text: return '激突'
    if '転倒' in text or '横転' in text or '逸走' in text: return '転倒'
    if '墜落' in text or '転落' in text or '落下' in text: return '墜落・転落'
    return '墜落・転落'

def fetch(jno):
    url = f"{BASE}/anzen_pg/sai_det.aspx?joho_no={jno}"
    out = os.path.join(TMP, f"sai_{jno}.html")
    subprocess.run(['curl','-sL','-A','Mozilla/5.0','-o',out,url],capture_output=True)
    raw = open(out,'rb').read()
    try: html = raw.decode('cp932','replace')
    except: html = raw.decode('utf-8','replace')
    return url, html

new_rows = []; seq = maxseq; batch_md5 = set()
report = []
for jno in JOHO:
    url, html = fetch(jno)
    m = re.search(r"/anzen/sai/thumnail/([^\"'> ]+\.(?:jpg|gif|png))", html, re.I)
    if not m:
        report.append((jno,'no-thumb','')); print(f"SKIP no-thumb joho={jno}"); continue
    imgpath = '/anzen/sai/thumnail/' + m.group(1)
    imgurl = BASE + imgpath
    # title
    tm = re.search(r'<title>(.*?)</title>', html, re.S)
    title = re.sub(r'\s+',' ', tm.group(1)).strip() if tm else ''
    title = re.split(r'\s*[-－|]\s*職場のあんぜん', title)[0].strip()
    # confirm aerial relevance
    if '高所作業車' not in html and '作業車' not in title:
        report.append((jno,'not-aerial',title)); print(f"SKIP not-aerial joho={jno} {title[:30]}"); continue
    # accident type
    atype = classify(title + ' ' + html[:4000])
    o = os.path.join(TMP, f"img_{jno}_" + m.group(1).replace('/','_'))
    res = subprocess.run(['curl','-sL','-A','Mozilla/5.0','-w','%{http_code}','-o',o,imgurl],
                         capture_output=True, text=True)
    code = res.stdout.strip()[-3:]
    if code!='200' or not os.path.exists(o):
        report.append((jno,f'http{code}',title)); print(f"SKIP http={code} joho={jno}"); continue
    ext = magic_ok(o)
    if not ext:
        report.append((jno,'not-image',title)); print(f"SKIP not-image joho={jno}"); continue
    data = open(o,'rb').read()
    md5 = hashlib.md5(data).hexdigest()
    if md5 in existing_md5 or md5 in batch_md5:
        report.append((jno,'dup-md5',title)); print(f"SKIP dup-md5 joho={jno}"); continue
    batch_md5.add(md5); seq += 1
    fn = f"{seq:04d}.{ext}"
    with open(os.path.join(IMGDIR, fn),'wb') as w: w.write(data)
    desc = title if title else f"高所作業車による労働災害(事例No.{jno})"
    new_rows.append([f"{seq:04d}", fn, '高所', atype, url, md5, desc])
    report.append((jno,'ADD '+fn,title))
    print(f"ADD {fn} <- joho={jno} [{atype}] {desc[:30]}")

if new_rows:
    with open(INDEX,'a',encoding='utf-8',newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for row in new_rows: w.writerow(row)
print(f"\nADDED {len(new_rows)} images. new maxseq={seq}")
