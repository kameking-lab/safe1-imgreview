# REPORT_ILLUST — 採用写真の「事故事例イラスト」化 × 元写真vsイラスト対比 最終報告

生成日: 2026-06-16（JST）

## ■目的
V2で作成した各事例の採用写真（`photos_v16/{N01..N15}/base.png`）を「事故事例イラスト（KYT教材・安全ポスター風のクリーンなフラット/ベクター）」へ再生成し、写実（写真）よりも**物理破綻が緩和されるか／被災の瞬間を明確に描けるか**を検証した。元写真 vs 生成イラスト（OpenAI版・Google版）を左右対比したPDFを発行・公開。

## ■公開URL
- レビューページ（静的/noindex/スマホ縦/外部読込なし）:
  https://hakuten-review.vercel.app/lkvzufp4mfvwnfmgafm9pi5kbqmtejwu/
- PDF直URL（Vercel）:
  https://hakuten-review.vercel.app/lkvzufp4mfvwnfmgafm9pi5kbqmtejwu/compare_illust_v17.pdf
- PDF（GitHub main・raw）:
  https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/compare_illust_v17.pdf
- PDF（GitHub main・blob）:
  https://github.com/kameking-lab/safe1-imgreview/blob/main/compare_illust_v17.pdf

検証（2026-06-16 JST 実測）:
- ルート `/` = 404（意図どおり非公開ルート）
- レビューページ = 200（text/html, 6,644 B）
- PDF（Vercel）= 200（application/pdf, 3,987,138 B）
- GitHub raw PDF = 200（3,987,138 B）

## ■生成枚数（成功/失敗）
- 事例: 15/15
- イラスト: **30/30 成功（失敗 0）**
  - 各事例2枚: OpenAI `gpt-image-2`（quality=high）／ Google `gemini-3-pro-image-preview`
- 自己点検で明らかな破綻による再生成は発生せず（初回採用が大半）。

## ■各事例の使用モデル（OpenAI / Google）
全事例共通:
- OpenAI = `gpt-image-2`
- Google = `gemini-3-pro-image-preview`（Nano Banana Pro）

| 新No | カテゴリ | 事故タイトル | OpenAI | Google |
|---|---|---|---|---|
| N01 | TGL | 展示パネル積み下ろし中、昇降板からの墜落 | gpt-image-2 | gemini-3-pro-image-preview |
| N02 | TGL | 什器の積み下ろし中、昇降板と車体の間に足を挟まれ | gpt-image-2 | gemini-3-pro-image-preview |
| N03 | TGL | パワーゲートでの荷役中、昇降板から転落しかけ | gpt-image-2 | gemini-3-pro-image-preview |
| N04 | TGL | 台車を昇降装置へ移す際、台車が落下し下敷きに | gpt-image-2 | gemini-3-pro-image-preview |
| N05 | TGL | 荷下ろし中、カゴ台車が倒れ作業員が転倒 | gpt-image-2 | gemini-3-pro-image-preview |
| N06 | 高所 | 会場天井付近の作業中、作業床手すりと上方構造物の間に挟まれ | gpt-image-2 | gemini-3-pro-image-preview |
| N07 | 高所 | 梁下を移動中、上方の梁と操作盤の間に挟まれ | gpt-image-2 | gemini-3-pro-image-preview |
| N08 | 高所 | 養生ネットを外そうとしてバスケットから墜落 | gpt-image-2 | gemini-3-pro-image-preview |
| N09 | 高所 | 看板取付で身を乗り出し、作業床から墜落 | gpt-image-2 | gemini-3-pro-image-preview |
| N10 | 高所 | 作業床上昇中、操作盤フレームと天井の間に胸部を挟まれ | gpt-image-2 | gemini-3-pro-image-preview |
| N11 | 高所 | バスケットから移ろうとして墜落 | gpt-image-2 | gemini-3-pro-image-preview |
| N12 | 高所 | 傾斜地で旋回中、機体がバランスを崩し転倒 | gpt-image-2 | gemini-3-pro-image-preview |
| N13 | 高所 | 手すりに足をかけたダクト取付中に墜落 | gpt-image-2 | gemini-3-pro-image-preview |
| N14 | 高所 | 外周作業で作業床から身を出し、高所から墜落 | gpt-image-2 | gemini-3-pro-image-preview |
| N15 | 高所 | 低い梁下を移動中、下がり壁と手すりの間に挟まれ | gpt-image-2 | gemini-3-pro-image-preview |

## ■物理破綻が補正できた事例の所感
イラスト化の最大の効果は、**写真版で曖昧だった「被災の瞬間」を、×印・矢印・衝撃線で確実に成立させられた**こと。写真は重力・重心・接触の整合を1枚で破綻なく描くのが難しく、「墜落しきっていない／踏ん張っている／機体が宙に浮いて見える」中途半端な絵になりがちだったが、イラストは記号表現で因果（危険→結果）を明示でき、教材としての可読性が大きく上がった。

- **N03（昇降板から転落しかけ）**: 写真では作業員がカゴ台車を支えて踏ん張る“しかけ”止まりだったが、両イラストとも重心が昇降板の外へ抜け、台車もろとも投げ出される瞬間に補正。×印（手すり）＋下向き矢印＋衝撃線で「転落が確実に起きている絵」へ。Google版は16:9の広い画面で会場の奥行き・トラスまで描き込み、状況が読み取りやすい。
- **N12（傾斜地で旋回中に高所作業車が転倒）**: 写真は機体が傾いて“浮いて見える”物理的に不自然なカットだったが、イラストでは車輪の片側接地・キャブ側への重心移動・作業員が作業床から振り出される様子が自然に成立。衝撃線とアスファルトの影で「いままさに転倒」が明確。
- **墜落系（N08・N09・N11・N13・N14）**: 写真で手すり際に留まりがちだった姿勢を、イラストでは体が手すりを越えて投げ出される構図へ補正でき、フルハーネスの装着有無や墜落方向（矢印）も判読しやすい。
- **挟まれ系（N02・N06・N07・N10・N15）**: 接触点（昇降板と車体／梁と操作盤／下がり壁と手すり）をイラストでは赤い衝撃マークで一点に集約でき、写真より「どこに挟まれるか」が直感的。

機種・人数・PPE（あごひもヘルメット／ハイビズ／安全靴／高所のフルハーネス）・日本の会場・実在ロゴ無し・流血無しの方針は全事例で概ね保持。両モデルとも構図と事故の向きは元写真を踏襲できた。

## ■モデル別の傾向
- **OpenAI `gpt-image-2`**: 正方形寄りのトリミングで主役（被災者・機体）に寄った構図。線画＋平塗りのKYT教材調が安定し、危険記号がはっきり。背景はやや簡素。
- **Google `gemini-3-pro-image-preview`**: 横長（16:9）で会場・トラス・他作業員まで描き込み、状況説明力が高い。表情・動きの誇張で「瞬間」が伝わりやすい。

## ■残課題
- ごく一部に手指・四肢の軽微な歪みや余剰描写が残る（教材用途では許容範囲だが、印刷配布前に要目視）。
- フルハーネスのランヤード接続先（親綱/アンカー）が描かれない／宙に浮くカットがあり、「正しい墜落制止」を示す用途には別途補強が必要。
- 縦横比がモデル間で異なる（OpenAI=正方形寄り／Google=16:9）ため、対比PDFでは各画像をラベル付きで個別配置して見切れを回避済み。揃える場合は後段で余白合成が必要。
- 写真版で残っていた物理破綻のうち、機体形状そのものの不正確さ（スペック差）はイラストでも完全には解消しないため、機種同定が要点の教材では実機写真の併用が望ましい。

## ■成果物
- イラスト: `illust_v17/{N01..N15}/openai_illust.png・google_illust.png`＋`gen_meta.json`
- 索引: `illust_index_v17.csv`
- 対比PDF: `compare_illust_v17.pdf`（1事例1ページ・A4横・全15ページ・元写真＋イラスト2枚をラベル付き対比）
- 公開: `review_illust/lkvzufp4mfvwnfmgafm9pi5kbqmtejwu/`（PDF＋index.html）／Vercel hakuten-review
