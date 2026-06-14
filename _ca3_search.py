import csv, glob, re, io
# C-A3: 高所作業車 坂道逸走で車体と側方構造物(側溝/壁/法面/縁石/別車両等)に挟まれ
files = sorted(glob.glob('data/jniosh/SHIBO_201*.csv'))
KIND = re.compile(r'高所作業車|高所作業者|垂直昇降|ブーム|バスケット|作業床|スカイマスター|スカイボーイ|リフト車')
PINCH = re.compile(r'はさ|挟|挟まれ|挟圧|圧迫|押しつけ|押し付け|押潰|押しつぶ|下敷')
RUN = re.compile(r'逸走|暴走|ずり下が|ずり落ち|滑り出|動き出|走り出|後退|前進|坂|傾斜|勾配|スロープ|ブレーキ|輪止め|車止め|転動')
STRUCT = re.compile(r'側溝|溝|壁|塀|擁壁|法面|のり面|縁石|ガードレール|柵|電柱|柱|構造物|建物|建屋|車両|車体|トラック|門|ゲート|シャッター')
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
            run = 'RUN' if RUN.search(situ) else '---'
            st = 'ST' if STRUCT.search(situ) else '--'
            hits.append((f,i,row[0],row[1],row[12],row[21],run,st,situ))
w(f"=== KIND x PINCH hits: {len(hits)} ===")
for f,i,id_,yr,kiin,kata,run,st,situ in hits:
    w(f"{f}:{i}\tID={id_}\tyr={yr}\t起因={kiin}\t型={kata}\t{run}\t{st}")
    w("  "+situ)
    w("")
with open('_ca3_results.txt','w',encoding='utf-8') as fo:
    fo.write(out.getvalue())
print("done", len(hits))
