# -*- coding: utf-8 -*-
import csv, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r"C:\Users\kanet\20260522\safe1\data\jniosh"
# print header
with open(base+r"\SHIBO_2014.csv", encoding='utf-8') as f:
    h = next(csv.reader(f))
print("HEADER:", list(enumerate(h)))
print("="*60)
targets = {'SHIBO_2014.csv':[804], 'SHIBO_2015.csv':[387,895], 'SHIBO_2018.csv':[226]}
for fn, ids in targets.items():
    with open(base+"\\"+fn, encoding='utf-8') as f:
        rows = list(csv.reader(f))
    for i, row in enumerate(rows):
        if i == 0: continue
        try: rid = int(row[0])
        except: continue
        if rid in ids:
            print("==== %s line=%d ID=%s" % (fn, i+1, row[0]))
            for idx in range(len(row)):
                v = row[idx]
                if v and (len(v) > 1) and idx in (1,3, len(h)-1) or ('型' in h[idx]) or ('起因' in h[idx]):
                    print("   [%d %s] = %s" % (idx, h[idx], v))
            print("   災害状況:", row[6])
            print()
