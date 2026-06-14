import csv, glob, re, io
# C-A5: 高所作業車の作業床(バスケット)上で、ブームの急操作/急停止/反動/突き上げ/揺れ等の
#       急動作により作業者が振られて(あおられて)体勢を崩し作業床から墜落（放り出され）。
files = sorted(glob.glob('data/jniosh/SHIBO_201*.csv'))
KIND = re.compile(r'高所作業車|高所作業者|垂直昇降|ブーム|バスケット|作業床|スカイマスター|スカイボーイ|リフト車|スカイ|搬器|搭乗')
FALL = re.compile(r'墜落|転落|落下|放り出|投げ出|振り落と|振り落とさ|落ちた|転落|あおられ')
# 「急動作で振られ」系: 急操作/急停止/反動/突き上げ/揺れ/振られ/あおられ/振動/衝撃/弾み/勢い/反力/跳ね
SWING = re.compile(r'急操作|急停止|急発進|急旋回|急上昇|急降下|急激|反動|突き上げ|つき上げ|揺れ|揺ら|振ら|振られ|あおら|あおられ|振動|衝撃|弾み|はずみ|勢い|反力|跳ね|はね|バウンド|振り回|振れ|操作を誤|誤操作|操作ミス')
out = io.StringIO()
def w(s): out.write(s+"\n")
hits = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        r = list(csv.reader(fh))
    for i, row in enumerate(r[1:], start=2):
        if len(row) < 22: continue
        situ = row[6]
        if KIND.search(situ) and (FALL.search(situ) or SWING.search(situ)):
            swing = 'SWING' if SWING.search(situ) else '-----'
            fall = 'FALL' if FALL.search(situ) else '----'
            hits.append((f,i,row[0],row[1],row[18],row[19],row[21],swing,fall,situ))
w(f"=== KIND x (FALL|SWING) hits: {len(hits)} ===")
# SWING付きを先に
hits.sort(key=lambda h: (h[7]!='SWING',))
for f,i,id_,yr,kcode,kiin,kata,swing,fall,situ in hits:
    w(f"{f}:{i}\tID={id_}\tyr={yr}\t起因コード={kcode}\t起因={kiin}\t型={kata}\t{swing}\t{fall}")
    w("  "+situ)
    w("")
with open('_ca5_results.txt','w',encoding='utf-8') as fo:
    fo.write(out.getvalue())
print("done hits=", len(hits), " SWING=", sum(1 for h in hits if h[7]=='SWING'))
