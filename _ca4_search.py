import csv, glob, re, io
# C-A4: 高所作業車 作業床(バスケット)から墜落（安全帯/フルハーネス未使用・乗り出し）
files = sorted(glob.glob('data/jniosh/SHIBO_201*.csv'))
KIND = re.compile(r'高所作業車|高所作業者|垂直昇降|ブーム|バスケット|作業床|スカイマスター|スカイボーイ|リフト車|テーブルリフト|シザース|シーザー')
FALL = re.compile(r'墜落|転落|落下|転落|墜落・転落|墜落転落|放り出|投げ出|振り落と|落ちた')
BELT = re.compile(r'安全帯|命綱|ハーネス|フルハーネス|ランヤード|親綱|墜落制止|親綱|フック|未使用|未着用|未接続|かけ忘れ|かけていな|装着していな')
LEAN = re.compile(r'乗り出|身を乗|手を伸ば|はみ出|乗りだ|越え|手すり|手摺|柵')
out = io.StringIO()
def w(s): out.write(s+"\n")
hits = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        r = list(csv.reader(fh))
    for i, row in enumerate(r[1:], start=2):
        if len(row) < 22: continue
        situ = row[6]
        if KIND.search(situ) and FALL.search(situ):
            belt = 'BELT' if BELT.search(situ) else '----'
            lean = 'LEAN' if LEAN.search(situ) else '----'
            hits.append((f,i,row[0],row[1],row[12],row[21],belt,lean,situ))
w(f"=== KIND x FALL hits: {len(hits)} ===")
for f,i,id_,yr,kiin,kata,belt,lean,situ in hits:
    w(f"{f}:{i}\tID={id_}\tyr={yr}\t起因={kiin}\t型={kata}\t{belt}\t{lean}")
    w("  "+situ)
    w("")
with open('_ca4_results.txt','w',encoding='utf-8') as fo:
    fo.write(out.getvalue())
print("done", len(hits))
