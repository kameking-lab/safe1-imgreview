import csv
targets = {
 'data/jniosh/SHIBO_2017.csv':[532,369,370,371,490],
 'data/jniosh/SHIBO_2016.csv':[715,304],
 'data/jniosh/SHIBO_2014.csv':[602,598,84,263],
 'data/jniosh/SHIBO_2018.csv':[16,17,784,124],
 'data/jniosh/SHIBO_2015.csv':[438],
}
for f,lines in targets.items():
    with open(f, encoding='utf-8') as fh:
        r=list(csv.reader(fh))
    for ln in lines:
        row=r[ln-1]
        print(f"=== {f}:{ln} ID={row[0]} yr={row[1]} ===")
        print("  業種(大/中/小):", row[8],"/",row[10],"/",row[12])
        print("  起因物(大15/中17/小19) code18:", row[15],"/",row[17],"/",row[19]," code=",row[18])
        print("  事故の型(21):", row[21])
        print()
