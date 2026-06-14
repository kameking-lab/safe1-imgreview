import csv, glob, re, os, io
base = r"C:\Users\kanet\20260522\safe1\data\jniosh"
files = sorted(glob.glob(os.path.join(base, "SHIBO_201*.csv")))
out = io.StringIO()

tgl = re.compile(r'(テールゲート|パワーゲート|昇降板|ゲートリフ|テールリフト)')  # TGL-specific (no generic ゲート/リフター)
descend = re.compile(r'(下降|降下|降ろ|降り|下り|下げ|下がっ|下りて|降りて|下ろし|降ろし)')
foot = re.compile(r'(足|下肢|脚|つま先|足首|くるぶし|下半身|下腿)')
pinch = re.compile(r'(はさま|挟ま|挟まれ|はさみ)')
ground = re.compile(r'(地面|床|路面|段差|地上|床面)')

queries = {
 "R1 TGL-specific only (all)": lambda s: tgl.search(s),
 "R2 TGL + ground": lambda s: tgl.search(s) and ground.search(s),
}
for qname, fn in queries.items():
    out.write(f"\n########## {qname} ##########\n")
    for f in files:
        rows = list(csv.reader(open(f, encoding='utf-8')))
        for i, row in enumerate(rows, start=1):
            if len(row) < 7: continue
            s = row[6]
            if fn(s):
                out.write(f"\n[{os.path.basename(f)}:{i}] ID{row[0]} 年={row[1]} 型={row[-1]}\n{s}\n")
open(r"C:\Users\kanet\20260522\safe1\_ct5_results2.txt","w",encoding="utf-8").write(out.getvalue())
print("ok", len(out.getvalue()))
