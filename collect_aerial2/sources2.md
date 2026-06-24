# sources2.md — 高所作業車「事故・危険」イメージ画像 収集元・検索クエリ案

作成: 2026-06-25 / 方式: instagram-automation `launchBrowser("anzen")` + Bing画像検索（雛形 `safe1/search_ra1.mjs` 準拠）
本タスクは**収集のみ**（新規画像生成なし）。追記専用・非破壊。出所URLは必ず index に記録する。

## ■収集方式（確認済み）
- ブラウザ: `C:/Users/kanet/20260522/instagram-automation/scripts/lib/browser-helpers.mjs` の
  `launchBrowser("anzen",{viewport:{width:1500,height:1200}})`（別プロファイル・別PID・ユーザーChrome非干渉）。
- 取得: Bing画像検索 `https://www.bing.com/images/search?q=...`（イラスト寄りは `&qft=+filterui:photo-clipart`）
  → `document.querySelectorAll("a.iusc")` の `m` 属性JSON → `{murl,purl,t}`
  → `fetch(murl,{Referer:purl,UA:Chrome})` で保存 → `murl` でユニーク化 → 中身で拡張子判定（png/jpg/gif/webp）。
- 重複排除: md5（実体同一は1枚に統合）。
- 索引: `collect_aerial2/aerial2_index.csv`
  列＝〔通し番号, ファイル名, カテゴリ(事故の型), 種別, 出所URL, 出所ドメイン, 状況メモ, md5〕。
- 実行済みクエリ: `collect_aerial2/queries_done.txt` に追記し再実行しない。
- 出尽くし判定: 8クエリ連続で新規ゼロ → そのカテゴリ終了。

## ■主な収集元ドメイン（公開・教育/公的資料中心）
- 職場のあんぜんサイト（厚労省）: anzeninfo.mhlw.go.jp — 死傷災害事例・図/写真
- 厚生労働省: mhlw.go.jp — 通達・パンフ・統計図
- 建設業労働災害防止協会（建災防）: kensaibou.or.jp
- 陸上貨物運送事業労働災害防止協会（陸災防）: rikusai.or.jp
- 中央労働災害防止協会（中災防/安全衛生情報センター）: jaish.gr.jp / jisha.or.jp
- 各都道府県労働局・労基署のリーフレット（mhlw.go.jp 配下 PDF）
- 高所作業車メーカー/レンタルの安全啓発・KYT教材（カタログ完成写真は除外）
- 安全教育イラスト/素材サイト・KYTシート・注意喚起ポスター（公開分）
- 解説記事・ブログの図解（出所URL記録）

## ■クエリ案（カテゴリ別・各最大40・clip=イラスト寄りフィルタ）

### A2 墜落・転落
- 高所作業車 墜落 災害 イラスト / 高所作業車 転落 事故 イラスト
- 高所作業車 バケット 墜落 安全帯 未使用 イラスト
- 高所作業車 乗り出し 墜落 ヒヤリハット イラスト
- 高所作業車 アウトリガー 墜落 KYT 教材
- 高所作業車 墜落 死亡災害 事例 厚生労働省
- 職場のあんぜんサイト 高所作業車 墜落 災害事例
- 高所作業車 墜落 注意喚起 ポスター
- aerial work platform fall from bucket accident illustration
- boom lift worker fall safety harness illustration
- scissor lift fall accident hiyari hatto illustration

### A3 挟まれ・巻き込まれ
- 高所作業車 挟まれ 災害 イラスト / 高所作業車 挟まれ 天井 鉄骨 事故
- 高所作業車 バケット 挟まれ 上昇 災害 イラスト
- 高所作業車 巻き込まれ ヒヤリハット KYT
- 高所作業車 挟まれ 死亡災害 事例 あんぜんサイト
- 高所作業車 挟まれ 注意喚起 ポスター
- aerial lift crushing caught between accident illustration
- boom lift crush hazard overhead illustration

### A4 転倒・横転
- 高所作業車 転倒 災害 イラスト / 高所作業車 横転 事故 イラスト
- 高所作業車 不整地 転倒 搭乗者 投げ出され イラスト
- 高所作業車 軟弱地盤 傾き 転倒 災害
- 高所作業車 アウトリガー 不備 転倒 KYT
- 高所作業車 転倒 死亡災害 事例 厚生労働省
- 高所作業車 横転 注意喚起 ポスター
- aerial work platform tip over uneven ground accident illustration
- boom lift overturn outrigger illustration

### A5 感電・飛来落下・不安全行動・その他
- 高所作業車 感電 電線 接触 災害 イラスト
- 高所作業車 充電電路 感電 注意喚起 ポスター
- 高所作業車 飛来落下 工具 落下 災害 イラスト
- 高所作業車 不安全行動 立ち乗り 手すり 乗り越え イラスト
- 高所作業車 ヒヤリハット 事例集 イラスト
- 高所作業車 危険予知 KYT シート
- aerial lift electrocution power line accident illustration
- aerial work platform falling object hazard illustration
- aerial lift unsafe act standing on rail illustration

## ■収集対象 / 除外（再掲）
- 採用: 事故の瞬間・ヒヤリハット・危険行動・やってはいけない例が分かる画像
  （実事例図・写真、安全教育イラスト、KYT教材挿絵、注意喚起ポスター、啓発イメージ、ピクト/標識、解説記事の図解）。
- 除外: 機種カタログの綺麗な完成写真、構造/部品名称図、無関係画像、通常作業のみの画像。

## ■疎通確認
- 雛形 `search_ra1.mjs` 確認済み（a.iusc 解析・Referer fetch・拡張子判定・murl重複排除）。
- anzen プロファイル疎通: `collect_aerial2/_smoke_a1.mjs` で launchBrowser→Bing→a.iusc件数を確認（保存はしない）。
  結果ログ: `collect_aerial2/_smoke_a1.log`。
