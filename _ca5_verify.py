import csv
def show(path, line):
    with open(path, encoding='utf-8') as fh:
        r = list(csv.reader(fh))
    hdr = r[0]
    row = r[line-1]
    print(f"\n===== {path}:{line}  (len={len(row)}) =====")
    idxs = {6:'災害状況',8:'業種大',10:'業種中',12:'業種小',15:'起因大',17:'起因中',18:'起因コード',19:'起因小',21:'事故の型'}
    for i,name in idxs.items():
        print(f"  [{i}] {name}: {row[i] if i<len(row) else '??'}")
    print("  ID col0:", row[0], " year col1:", row[1])
show('data/jniosh/SHIBO_2015.csv', 77)   # primary candidate ID76
show('data/jniosh/SHIBO_2014.csv', 598)  # truck collision jolt ID597
show('data/jniosh/SHIBO_2016.csv', 382)  # truck collision jolt ID381
show('data/jniosh/SHIBO_2017.csv', 236)  # truck collision jolt ID235
