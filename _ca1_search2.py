import csv, glob, re, io, sys
files = sorted(glob.glob('data/jniosh/SHIBO_201*.csv'))
out = io.StringIO()
KIND = re.compile(r'高所作業車|高所作業者|垂直昇降|ブーム|バスケット|作業床|スカイ')
TIP = re.compile(r'転倒|横転|倒れ|転落')
for f in files:
    with open(f, encoding='utf-8') as fh:
        r = list(csv.reader(fh))
    header = r[0]
    for i, row in enumerate(r[1:], start=2):
        if len(row) < 7: continue
        situ = row[6]
        if re.search(r'高所作業車', situ) and TIP.search(situ):
            kata = row[-1]
            kiin = "/".join([row[15] if len(row)>15 else '', row[17] if len(row)>17 else '', row[19] if len(row)>19 else ''])
            out.write(f"=== {f}:{i}  ID={row[0]} 年={row[1]} 型={kata} 起因={kiin}\n")
            out.write(situ + "\n\n")
open('_ca1_results.txt','w',encoding='utf-8').write(out.getvalue())
print("done", len(out.getvalue()))
