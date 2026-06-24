# RULES_AERIAL2 — 高所作業車「事故・危険」イメージ画像 ブラウザ収集（全自動・無人継続）

## ■目的
高所作業車（ブーム式／垂直昇降式／シザース／トラック搭載型）の「事故・ヒヤリハット・危険行動」を表す
イラスト・写真・イメージ画像を、**実災害事例に限らず教育用・架空のものも含めて**集められるだけ集める。
事故の型は不問（墜落・転落／挟まれ・巻き込まれ／転倒・横転／感電／飛来落下／不安全行動 等）。

## ■安全（厳守）
- 削除/上書き禁止（追加は必ず新ファイル名）。既存成果物（collect2/・collect_aerial/・review_*・layers_*・photos_* 等）は非破壊。
- Chrome を kill しない。taskkill しない。rm/Remove-Item/del/move を使わない。
- API キー/認証情報の **値は出力しない**。
- 時刻は `powershell.exe -Command "Get-Date"`。
- git push は origin master(=main) に append-only。競合したら `git pull --rebase` 後に再 push。
- 著作権配慮：出所URLを必ず記録。SNSの個人投稿・有料素材の透かし無し抜き取りは避け、
  公開されている教育資料・素材サイト・団体資料・解説記事・公的DBの画像を中心にする。
- 本タスクは**収集のみ**（新規画像生成はしない）。捏造禁止（確定素材のみ）。

## ■収集方式（instagram-automation 方式・実績あり）
- ブラウザは `C:/Users/kanet/20260522/instagram-automation/scripts/lib/browser-helpers.mjs` の
  `launchBrowser("anzen", {viewport:{width:1500,height:1200}})` を使う（別プロファイル・別PID。ユーザーChromeに触れない）。
- 既存 `safe1/search_ra1.mjs` が完全な雛形：Bing画像検索 `https://www.bing.com/images/search?q=...`
  （イラスト寄りは `&qft=+filterui:photo-clipart`）→ `document.querySelectorAll("a.iusc")` の `m` 属性JSONから
  `{murl,purl,t}` を抽出→ `fetch(murl, {Referer:purl, UA:Chrome})` で保存→`murl`でユニーク化。
- 新規スクリプトは新ファイル名で作る（例 `collect_aerial2_a2.mjs`）。既存 search_*.mjs は上書きしない。
- 厚労省/団体DB（anzeninfo.mhlw.go.jp 等）は WebFetch/page.goto で事例ページの図・写真を直接取得してもよい。

## ■収集対象 / 除外
- 採用：事故の瞬間・ヒヤリハット・危険行動・やってはいけない例が分かる画像。
  実事例図・写真、安全教育イラスト、KYT教材挿絵、注意喚起ポスター、啓発イメージ、ピクト/標識、解説記事の図解。
- 除外：機種カタログの綺麗な完成写真、構造/部品名称図、無関係画像、通常作業のみの画像。

## ■クエリ / 出尽くし
- 型・状況・「イラスト/写真/ポスター/ヒヤリハット/KYT/注意喚起/危険/墜落/転倒」等を組み合わせ多数試す（1カテゴリ最大40クエリ）。
- 実行済みクエリは `collect_aerial2/queries_done.txt` に追記し再実行しない。
- 出尽くし判定：**8クエリ連続で新規ゼロ → そのカテゴリ終了**。

## ■保存 / 索引（重複排除）
- 画像：`collect_aerial2/img/0001.xxx …`（4桁連番・通し番号）。拡張子は中身判定（png/jpg/gif/webp）。
- 重複は **md5** で統合（実体が同じものは1枚に）。可能なら pHash も併用。
- 索引：`collect_aerial2/aerial2_index.csv`。列＝
  〔通し番号, ファイル名, カテゴリ(事故の型), 種別(実事例図/教育イラスト/ポスター/写真/ピクト 等), 出所URL, 出所ドメイン, 状況メモ, md5〕。

## ■作業の進め方（ランナーが1タスクずつ起動）
- `BACKLOG_AERIAL2.md` の未完最上段 `- [ ]` を**1つだけ**実行 → 完了で `- [x]` にして git push。
- 着手前に既存 `collect_aerial2/` を確認し未取得分のみ追加（途中再開で重複/破壊しない）。
- 未完タスクが無ければ空ファイル `DONE_AERIAL2.flag` を作成して停止。
- usage/rate limit/429 到達時は WIP を保存・push して停止（ランナーが reset 時刻まで待って自動再開）。

## ■最終発行
- `aerial2_catalog.pdf`：全画像を通し番号付き一覧（1ページ6枚・各サムネ直下に〔通し番号/事故の型/種別/出所ドメイン〕・選抜できる大きさ）。
- `review_aerial2/<ランダム32文字>/` に PDF＋index.html（静的・外部読込なし・noindex・スマホ縦・「開く/保存」＋iframe縦表示）を配置。
- Vercel hakuten-review を**過去全トークンの union** で再デプロイ（既存URL全200保持・ルート/=404・HTTP200を curl 実測検証）。
- 成果物を GitHub(master/main) へ push。
- `REPORT_AERIAL2.md`：公開URL／PDF直URL＋raw／収集枚数（型別合計・種別内訳）／主な出所ドメイン別内訳／出尽くし判定／残課題 を記載し push。
