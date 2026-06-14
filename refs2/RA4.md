# RA4 高所作業車 安全帯未使用で作業床から墜落

採用枚数: 3 / 最大3
収集方法: ブラウザ画像検索（instagram-automation方式・別プロファイル anzen・Chrome kill無し・画像生成なし）。Bing画像検索 search_ra4.mjs で11クエリ（高所作業車の安全帯未使用/未着用・作業床/バケットからの墜落・転落・身を乗り出し・手すり乗り越え・建荷協/職場のあんぜんサイト/陸災防・英語 aerial work platform / MEWP / cherry picker fall no harness、clipartフィルタ＋photo含む）→候補153点 d01–d153 を refs2/RA4/_cand に収集。加えて RA3 で「RA4向け」と判定済みの建荷協 高0015 墜落イラスト（RA3/_cand/d01.jpg）を d154.jpg として本スロットへ複製。計154点を sheet_ra4.mjs で全点コンタクトシート化（_sheet_0..5.png）し実目視で3要素判定。判定日時 2026-06-14 16:44 頃（powershell Get-Date 基準）。

## 判定結果（3要素=機械○/事象○/被災者○）
RA4 の事象「高所作業車の作業床（バケット/シザース床）から人が墜落・転落して被災（安全帯未使用/未着用が原因）」を満たす事故イラスト 3 点を採用。

### 01.png（採用）= d154（建荷協）
- 出所URL: http://www.sacl.or.jp/case/ （(一社)日本建設機械施工協会 建設荷役車両安全技術協会「災害事例」高0015「高所作業車からの墜落災害」, 画像 http://www.sacl.or.jp/sa7210/wp-content/uploads/disaster/awp0015_2.jpg ©1999 sacl.or.jp）
- 何の事故か: シザース式高所作業車の作業床上で、作業者が手摺越しに身を乗り出して構造物側へ移ろうとしバランスを崩し墜落しかける（地上には墜落した被災者を示す小図）。安全帯未使用・作業床からの墜落災害事例。
- 3要素: 機械○（シザース式高所作業車） / 事象○（作業床から身を乗り出し墜落） / 被災者○（搭乗者が墜落・被災）。

### 02.png（採用）= d99（dreamstime ベクター・透かしあり）
- 出所URL: https://www.dreamstime.com/illustration-falling-work-platform-as-common-hazard-aerial-safety-man-boom-lift-pure-vector-image321250577 （"Illustration of Falling from the Work Platform As a Common Hazard ... boom lift"）
- 何の事故か: ブーム式高所作業車のバケットから作業者が墜落し、建物の端に両手でぶら下がり、ヘルメットが落下していく場面。安全帯なしで作業床から墜落した瞬間を描く啓発ベクター。
- 3要素: 機械○（ブーム式高所作業車） / 事象○（バケットから墜落） / 被災者○（搭乗者が墜落・被災）。
- 注: dreamstime のプレビュー（透かし入り）。事故イラストとして3要素は満たす。

### 03.png（採用）= d103（stockphotos ベクター・透かしあり）
- 出所URL: https://www.stockphotos.com/vector/fall-from-work-platform-scissor-lift-and-elevated-work-platform-safety-tips-flat-vector-515913 （"Fall from work platform. Scissor lift and elevated work platform safety"）
- 何の事故か: シザース式高所作業車の作業床から作業者が頭から墜落し、ヘルメットが飛ぶ場面。下部に "FALL FROM WORK PLATFORM" の注意キャプション付きの啓発ベクター。
- 3要素: 機械○（シザース式高所作業車） / 事象○（作業床から墜落） / 被災者○（搭乗者が墜落・被災）。
- 注: stockphotos のプレビュー（透かし入り）。事故イラストとして3要素は満たす。

## 不採用メモ（参考・主な候補）
- **d24 / d25(PIXTA) / d23 / d40(illustAC)**＝作業者が縁・脚立から墜落しかける/墜落するイラストだが、いずれも**高所作業車が描かれていない**（脚立・床端のみ）。機械要件不成立で不採用。
- **d26**（「高所作業は安全帯使用」安全標識）＝安全帯を梁にかける作業者の標識で**事故が起きておらず機械もなし**。3要素不成立で不採用。
- **d63（建荷協 ©1999）**＝崖際でブーム式高所作業車のバケットに搭乗し作業する図だが**墜落の事象が起きていない**通常作業＋接触注意の図。事象不一致で不採用（RA6/接触系寄り）。
- **d64（労働新聞社 災害事例）**＝高所作業車が**バランスを崩して転倒し**被災者の上に倒れる図。事象が「転倒・下敷き」で RA1/RA7 向け、RA4 の「作業床からの墜落」ではないため本スロットでは不採用。
- **d76 / d105**＝高所作業車の**通常作業写真**（電気工事・ツールボックストーク用バナー）で事故の事象なし。3要素不成立で不採用。
- その他（MEWP用語/部品解説図・安全帯製品図・統計図・救助手順図・通常作業写真）多数＝事故イラストの3要素不成立で不採用。

## メモ
- 収集スクリプト: search_ra4.mjs（11クエリ→153点 d01–d153）＋建荷協図を d154 として複製。メタ: _cand/_all_meta.json・_dl.json。コンタクトシート: sheet_ra4.mjs → _cand/_sheet_0..5.png。採用確定: adopt_ra4.mjs（白背景フラット化のみ・内容無改変）。
- 削除/上書きなし・追加は新ファイル名のみ・Chrome kill無し・画像生成は一切していない・認証情報やAPIキーの値は出力していない。
