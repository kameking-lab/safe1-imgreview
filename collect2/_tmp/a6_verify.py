import csv, hashlib, os
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx=os.path.join(base,'img_index.csv')
imgdir=os.path.join(base,'img')
rows=list(csv.DictReader(open(idx,encoding='utf-8')))
print("index rows:", len(rows))
nums=[r['通し番号'] for r in rows]
exp=['%04d'%i for i in range(1,len(rows)+1)]
print("numbering sequential:", nums==exp)
files=set(os.listdir(imgdir))
print("img files:", len(files))
seen={}; mism=[]; dup=[]; missing=[]
for r in rows:
    fn=r['ファイル名']; p=os.path.join(imgdir,fn)
    if not os.path.exists(p): missing.append(fn); continue
    m=hashlib.md5(open(p,'rb').read()).hexdigest()
    if m!=r['md5']: mism.append((fn,r['md5'],m))
    if m in seen: dup.append((fn,seen[m]))
    else: seen[m]=fn
print("missing files:", missing)
print("md5 mismatches:", mism)
print("duplicate md5 groups:", dup)
idxfiles=set(r['ファイル名'] for r in rows)
print("orphan img files:", sorted(files-idxfiles))
from collections import Counter
print("category:", dict(Counter(r['カテゴリ'] for r in rows)))
print("type:", dict(Counter(r['事故種類'] for r in rows)))
print("rows missing URL:", [r['通し番号'] for r in rows if not r['出所URL'].strip()])
