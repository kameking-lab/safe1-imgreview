# RULES_C — 事故イラスト収集(A) ＋ 事故情報1000件×2 Excel化(B)（全自動・無人継続）

## ■安全（厳守）
- 削除/上書き禁止（追加は新ファイル名）。Chrome kill厳禁（taskkill厳禁）。APIキー/認証情報の値は出力しない。今回は画像生成しない（収集のみ）。
- 時刻は `powershell.exe -Command "Get-Date"`。push は origin main(=master) に append-only。競合したら pull --rebase 後に再push。
- 着手前に既存（collect2/・data_xlsx/・data/jniosh/）を確認し未取得分のみ追加（途中再開で重複/破壊しない）。
- ブラウザ画像検索は instagram-automation 方式・別プロファイル・Chrome kill無し。

## ■作業の進め方
- BACKLOG_C.md の未完最上段タスクを1つ実行→完了で `- [x]` にして git push。無ければ `DONE_C.flag` を作成。
- 制限到達（usage/rate limit/429）時は WIP を保存・push して停止（ランナーが自動再開する）。

## (A) 事故イラスト 50〜100枚（被りなし・通し番号）
- TGL付きトラック/高所作業車の「事故イラスト/事故が写った図・写真」をシチュエーション不問で広く収集（墜落/転倒/滑落/下敷き/はさまれ/感電/逸走 など何でも）。通常作業のみ・構造/部品名称図・無関係な単体写真は除外。
- 被りなし：md5（可能ならpHashも）で重複排除。実体が同じものは1枚に統合。
- 保存：`collect2/img/0001.jpg …` 連番(4桁・通し番号)。`collect2/img_index.csv` に〔通し番号,ファイル名,カテゴリ(TGL/高所),事故種類,出所URL,md5,1行説明〕。
- 探す先：陸災防/建災防/中災防/林災防、各都道府県労働局、KYT教材、災害事例イラスト集、メーカー取説の災害・警告図、安全ポスター、各種安全衛生サイト等を幅広く。最低50、可能なら100近くへ。

## (B) 事故情報 各1000件（被りなし・出典URL・カテゴリ別Excel）
- 一次データ：①JNIOSH整形CSV( https://www.jniosh.johas.go.jp/publication/houkoku/houkoku_2022_01.html の死亡災害DB H3-H30 / 死傷DB H18-H29 )をDLしgrep。②あんぜんサイト 死亡災害DB( https://anzeninfo.mhlw.go.jp/anzen_pg/SIB_FND.html )/死傷DB( https://anzeninfo.mhlw.go.jp/anzen_pgm/SHISYO_FND.html )を起因物・事故の型で絞り込み。③出典URLの付く公的事故報告。
- 抽出：起因物/災害発生状況が「テールゲートリフター/パワーゲート/昇降板付きトラック」該当＝TGL群、「高所作業車/ブーム/作業床/バスケット(起因物コード146等)」該当＝高所群。各群1000件目標（集まらなければ最大数を集め件数を報告）。
- 被りなし：(発生年月日+業種+事故の型+災害発生状況)のハッシュで重複排除。
- カテゴリ：事故の型（墜落・転落/転倒/はさまれ・巻き込まれ/崩壊・倒壊/飛来・落下/激突/感電 等）で分類。
- 出力：Excel。`data_xlsx/accidents_TGL.xlsx` と `data_xlsx/accidents_AERIAL.xlsx`（または1ブック2シート＋集計シート）。列＝〔通し番号,カテゴリ(事故の型),発生年,業種,起因物,災害発生状況(全文),出典(ファイル名+行番号 or URL),データ源〕。出典URLは全件必須、無いものは除外。

## ■最終発行
- `img_catalog.pdf`（全イラストを通し番号付き一覧＝後から選べる）を作成。
- `review_collect/<ランダム32文字>/` に PDF＋index.html(静的・外部読込なし・noindex・スマホ縦)＋Excel を配置し Vercel hakuten-review に再デプロイ（既存URL保持・ルート/=404・HTTP200検証）。成果物を GitHub(main)へ push。
- `REPORT_C.md` に〔公開URL/PDF/Excel直URL＋raw・イラスト総数・事故件数(TGL/高所)・カテゴリ別件数〕を記載し push。
