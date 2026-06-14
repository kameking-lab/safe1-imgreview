# -*- coding: utf-8 -*-
# A5 final: append 11 aerial rows (0063-0073) to img_index.csv (append-only).
# Run AFTER `git checkout HEAD -- collect2/img_index.csv` so prior 62 rows are byte-identical.
import csv, hashlib, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
INDEX = 'collect2/img_index.csv'
IMGDIR = 'collect2/img'

# seq -> (joho, accident-type, one-line desc).  Types are the OFFICIAL 事故の型 from each SAI_DET page.
DATA = [
 (63,401,'はさまれ・巻き込まれ','パイプラックの塗装でバケット上から旋回操作中、被災者がパイプラックとバケットの間に挟まれ死亡した'),
 (64,447,'感電','トラック積載形ブーム式高所作業車で左官工事中、感電した災害'),
 (65,507,'激突','機械設備架台の組立作業中、バケットの縁と架台の梁の間に挟まれ死亡した（事故の型=激突され）'),
 (66,549,'激突','梁の塗装で次の作業箇所へ走行中、地面の凹凸で高所作業車が傾きバケットが急上昇した'),
 (67,648,'はさまれ・巻き込まれ','体育館天井の吹付け塗装中に突然ブームが上昇し、搬器から身を乗り出していた被災者が挟まれた'),
 (68,724,'転倒','電線の絶縁用防護管を取り外す作業中に高所作業車が転倒し、乗っていた被災者が被災した'),
 (69,728,'墜落・転落','垂直昇降型高所作業車で高架道路の型わく材を地上に降ろす作業中、リフトアームが折れ墜落した'),
 (70,100010,'墜落・転落','幹線電柱の鳥害対策で電線のバインド線取替作業を高所作業車で行っていた際に墜落した'),
 (71,100076,'はさまれ・巻き込まれ','地下室でコンクリート壁仕上げのため移動中、扉下がり壁と作業車の手すりの間に挟まれた'),
 (72,100094,'激突','道路照明灯の設置工事中、走行してきた大型トラックが作業中の高所作業車に激突した'),
 (73,100432,'墜落・転落','造船所で新造船外板の塗装作業中、高所作業車から作業者が墜落した'),
]

# verify existing index ends at seq 62
with open(INDEX, encoding='utf-8') as f:
    rows = list(csv.reader(f))
maxseq = max(int(r[0]) for r in rows[1:] if r)
assert maxseq == 62, f"expected maxseq=62 before append, got {maxseq}"

new = []
for seq, jno, atype, desc in DATA:
    fn = f"{seq:04d}.gif"
    path = os.path.join(IMGDIR, fn)
    md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
    url = f"https://anzeninfo.mhlw.go.jp/anzen_pg/sai_det.aspx?joho_no={jno}"
    new.append([f"{seq:04d}", fn, '高所', atype, url, md5, desc])

with open(INDEX, 'a', encoding='utf-8', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    for r in new:
        w.writerow(r)
        print('APPEND', r[0], r[3], r[6][:30])
print(f"\nappended {len(new)} rows")
