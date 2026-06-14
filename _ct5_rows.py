import csv, os, io
base = r"C:\Users\kanet\20260522\safe1\data\jniosh"
want = {"SHIBO_2014.csv":[815,157], "SHIBO_2018.csv":[850]}
hdr = None
out = io.StringIO()
for fn, lines in want.items():
    rows = list(csv.reader(open(os.path.join(base,fn), encoding='utf-8')))
    hdr = rows[0]
    for ln in lines:
        row = rows[ln-1]
        out.write(f"\n==== {fn}:{ln} ID{row[0]} ====\n")
        for h,v in zip(hdr,row):
            out.write(f"  {h} = {v}\n")
open(r"C:\Users\kanet\20260522\safe1\_ct5_rows.txt","w",encoding="utf-8").write(out.getvalue())
print("ok")
