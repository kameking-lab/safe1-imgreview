import csv, io
targets = {
 'data/jniosh/SHIBO_2016.csv':[895],
 'data/jniosh/SHIBO_2017.csv':[490],
 'data/jniosh/SHIBO_2014.csv':[263],
 'data/jniosh/SHIBO_2015.csv':[555,556],
}
out=io.StringIO()
for f,lines in targets.items():
    with open(f,encoding='utf-8') as fh:
        r=list(csv.reader(fh))
    hdr=r[0]
    for ln in lines:
        row=r[ln-1]
        out.write(f"##### {f}:{ln}\n")
        for h,v in zip(hdr,row):
            if v.strip(): out.write(f"  {h}: {v}\n")
        out.write("\n")
open('_ca1_dump.txt','w',encoding='utf-8').write(out.getvalue())
print("ok")
