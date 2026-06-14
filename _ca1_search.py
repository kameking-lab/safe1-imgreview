import csv, glob, re
files = sorted(glob.glob('data/jniosh/SHIBO_201*.csv'))
# mechanism: aerial work platform overturning on uneven/sloped ground
KIND = re.compile(r'高所作業車|高所作業者|垂直昇降|ブーム|バスケット|作業床|スカイマスター|スカイボーイ')
TIP = re.compile(r'転倒|横転|倒れ|転落|傾い|倒壊')
GROUND = re.compile(r'不整地|傾斜|軟弱|地盤|段差|くぼ|窪|路肩|斜面|凸凹|でこぼこ|不安定|沈下|坂|路面')
for f in files:
    with open(f, encoding='utf-8') as fh:
        r = list(csv.reader(fh))
    header = r[0]
    for i, row in enumerate(r[1:], start=2):  # line number in file (1-based, header=1)
        if len(row) < 7: continue
        situ = row[6]
        if KIND.search(situ) and TIP.search(situ):
            kata = row[-1] if row else ''
            ground = 'G' if GROUND.search(situ) else '-'
            print(f"{f}:{i}\tID={row[0]}\tyr={row[1]}\t型={kata}\tground={ground}")
            print("  " + situ[:200])
