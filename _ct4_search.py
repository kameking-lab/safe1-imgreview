# -*- coding: utf-8 -*-
import csv, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r"C:\Users\kanet\20260522\safe1\data\jniosh"
files = ['SHIBO_2014.csv','SHIBO_2015.csv','SHIBO_2016.csv','SHIBO_2017.csv','SHIBO_2018.csv']
cart = re.compile(r'カゴ車|かご車|かご台車|カゴ台車|ロールボックス|ロールパレット|籠車|ロールボックスパレット|ロールパレット|台車')
topple = re.compile(r'倒れ|転倒|横転|倒壊|傾い|激突')
gate = re.compile(r'テールゲート|パワーゲート|昇降板|ゲートリフ|リフター|荷台|ゲート')
for fn in files:
    with open(base+"\\"+fn, encoding='utf-8') as f:
        rows = list(csv.reader(f))
    for i, row in enumerate(rows):
        if i == 0 or len(row) < 22: continue
        s = row[6]
        if cart.search(s) and topple.search(s) and gate.search(s):
            print("%s line=%d ID=%s 型=%s 起因=%s" % (fn, i+1, row[0], row[21], row[19]))
            print("   ", s[:300])
            print()
