import csv, glob, re, io, sys
# C-A2: 高所作業車 作業床(バスケット)と上方構造物(梁/桁/天井/看板)で挟まれ
files = sorted(glob.glob('data/jniosh/SHIBO_201*.csv'))
KIND = re.compile(r'高所作業車|高所作業者|垂直昇降|ブーム|バスケット|作業床|スカイマスター|スカイボーイ|リフト車')
PINCH = re.compile(r'はさ|挟|挟まれ|挟圧|圧迫|押しつけ|押し付け|押潰|押しつぶ')
OVER = re.compile(r'梁|桁|天井|上方|上部|構造物|スラブ|配管|ダクト|看板|庇|ひさし|軒|床版|橋|フレーム|鉄骨|トラス|建屋|シャッター|開口|窓|壁|障害物')
out = io.StringIO()
def w(s): out.write(s+"\n")
hits = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        r = list(csv.reader(fh))
    for i, row in enumerate(r[1:], start=2):
        if len(row) < 22: continue
        situ = row[6]
        if KIND.search(situ) and PINCH.search(situ):
            over = 'OVER' if OVER.search(situ) else '----'
            hits.append((f,i,row[0],row[1],row[12],row[21],over,situ))
w(f"=== KIND x PINCH hits: {len(hits)} ===")
for f,i,id_,yr,kiin,kata,over,situ in hits:
    w(f"{f}:{i}\tID={id_}\tyr={yr}\t起因={kiin}\t型={kata}\t{over}")
    w("  "+situ)
    w("")
with open('_ca2_results.txt','w',encoding='utf-8') as fo:
    fo.write(out.getvalue())
print("done", len(hits))
