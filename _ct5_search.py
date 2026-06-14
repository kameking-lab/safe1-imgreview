# C-T5 search: TGL descending, foot caught between platform and ground (はさまれ)
import csv, glob, re, os
base = r"C:\Users\kanet\20260522\safe1\data\jniosh"
files = sorted(glob.glob(os.path.join(base, "SHIBO_201*.csv")))
gate = re.compile(r'(テールゲート|パワーゲート|昇降板|ゲートリフ|リフター|テールリフト|ゲート|リフト)')
foot = re.compile(r'(足|下肢|脚|つま先|足首|くるぶし|下半身)')
pinch = re.compile(r'(はさま|挟ま|挟まれ|はさみ)')
ground = re.compile(r'(地面|床|路面|段差|地上)')

print("=== A) gate + pinch ===")
for f in files:
    rows = list(csv.reader(open(f, encoding='utf-8')))
    for i, row in enumerate(rows, start=1):
        if len(row) < 7: continue
        s = row[6]
        if gate.search(s) and pinch.search(s):
            print(f"{os.path.basename(f)}:{i} ID{row[0]} 型={row[-1]} foot={bool(foot.search(s))} grnd={bool(ground.search(s))}")
            print("   ", s[:260])

print("\n=== B) gate + foot + ground (no pinch req) ===")
for f in files:
    rows = list(csv.reader(open(f, encoding='utf-8')))
    for i, row in enumerate(rows, start=1):
        if len(row) < 7: continue
        s = row[6]
        if gate.search(s) and foot.search(s) and ground.search(s) and not pinch.search(s):
            print(f"{os.path.basename(f)}:{i} ID{row[0]} 型={row[-1]}")
            print("   ", s[:260])
