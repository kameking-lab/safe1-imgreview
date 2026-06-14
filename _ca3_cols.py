import csv
targets = {
  'data/jniosh/SHIBO_2017.csv': [86],
  'data/jniosh/SHIBO_2014.csv': [253, 905],
  'data/jniosh/SHIBO_2018.csv': [117],
}
for f, lines in targets.items():
    with open(f, encoding='utf-8') as fh:
        r = list(csv.reader(fh))
    hdr = r[0]
    for ln in lines:
        row = r[ln-1]
        print(f"\n==== {f}:{ln}  ID={row[0]} yr={row[1]} ====")
        for idx in [12, 15, 17, 19, 18, 21]:
            if idx < len(row):
                print(f"  [{idx}] {hdr[idx] if idx < len(hdr) else '?'} = {row[idx]}")
