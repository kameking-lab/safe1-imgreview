# C-T5: dump full 災害状況 (UTF-8 file) for candidate rows matching I-T5
# mechanism: TGL/power gate DESCENDING, foot/leg caught between platform and ground/floor
import csv, glob, re, os, io
base = r"C:\Users\kanet\20260522\safe1\data\jniosh"
files = sorted(glob.glob(os.path.join(base, "SHIBO_201*.csv")))
out = io.StringIO()

gate = re.compile(r'(テールゲート|パワーゲート|昇降板|ゲートリフ|リフター|テールリフト|ゲート)')
descend = re.compile(r'(下降|降下|降ろ|降り|下り|下げ|下がっ|下りて|降りて|下ろし)')
foot = re.compile(r'(足|下肢|脚|つま先|足首|くるぶし|下半身|下腿)')
pinch = re.compile(r'(はさま|挟ま|挟まれ|はさみ)')
ground = re.compile(r'(地面|床|路面|段差|地上)')

def colidx(header):
    return header

queries = {
 "Q1 gate+descend+pinch": lambda s: gate.search(s) and descend.search(s) and pinch.search(s),
 "Q2 gate+foot+pinch": lambda s: gate.search(s) and foot.search(s) and pinch.search(s),
 "Q3 (TGL terms)+ground+pinch": lambda s: re.search(r'(テールゲート|パワーゲート|昇降板)', s) and ground.search(s) and pinch.search(s),
 "Q4 (TGL terms)+foot": lambda s: re.search(r'(テールゲート|パワーゲート|昇降板)', s) and foot.search(s),
}

seen = {}
for qname, fn in queries.items():
    out.write(f"\n########## {qname} ##########\n")
    for f in files:
        rows = list(csv.reader(open(f, encoding='utf-8')))
        header = rows[0]
        for i, row in enumerate(rows, start=1):
            if len(row) < 7: continue
            s = row[6]
            if fn(s):
                # 事故の型 = last col; 起因物 columns
                kata = row[-1]
                kiin = row[18] if len(row) > 18 else "?"
                out.write(f"\n[{os.path.basename(f)}:{i}] ID{row[0]} 年={row[1]} 型={kata} 起因物中分類={kiin}\n")
                out.write(s + "\n")
outpath = r"C:\Users\kanet\20260522\safe1\_ct5_results.txt"
open(outpath, "w", encoding="utf-8").write(out.getvalue())
print("wrote", outpath, len(out.getvalue()), "chars")
