# RULES_EVENT — 展示会場 設営中の事故事例イラスト 生成（aerial2 元絵25枚ベース・全自動・無人継続）

## ■目的
aerial2 収集イラストの指定25番号をベースに、その「事故の型・構図・被災状況」を引き継ぎつつ
舞台を「日本の展示会場・ブース設営作業現場」に置き換えた事故事例イラストを生成する。
1元絵につき4枚＝OpenAI(gpt-image-2 quality=high)で2案＋Google(gemini-3-pro-image-preview / Nano Banana Pro)で2案。

## ■安全（厳守）
- 削除/上書き禁止（追加は必ず新ファイル名）。既存成果物（collect_aerial2/・review_*・layers_* 等）は非破壊。
- Chrome を kill しない。taskkill しない。rm/Remove-Item/del/move を使わない。
- APIキー/認証値は **値を出力しない**（`.env` から読む。ログ等に出す場合は末尾4桁マスクのみ）。
- 時刻は `powershell.exe -Command "Get-Date"`。git push は origin master(=main) に append-only。競合は `git pull --rebase` 後再push。
- 着手前に `gen_event_v20/` の既存を確認し**未生成分のみ**生成（出力先が既にあれば skip＝再開安全）。捏造禁止。

## ■キー / 生成API（.env から読む・値出力禁止）
- `.env` の `OPENAI_API_KEY` / `GEMINI_API_KEY` を読む（既存 `gen_img.mjs` の readEnv 方式）。
- OpenAI: 参照画像つきは画像編集エンドポイント `POST https://api.openai.com/v1/images/edits`
  （multipart: `model=gpt-image-2`, `image=`元画像, `prompt=`, `size=1024x1024`, `quality=high`, `n=1` → b64_json）。
- Google: `POST .../v1beta/models/gemini-3-pro-image-preview:generateContent`、
  `contents.parts=[{inlineData:{mimeType, data:base64(元画像)}},{text:プロンプト}]`、`responseModalities:["IMAGE"]`。
- 既存 `gen_img.mjs`（テキスト→画像）が雛形。**新ファイル名**で参照画像対応版（例 `gen_event_v20.mjs`）を作る（gen_img.mjs は上書きしない）。
- レート/429/5xx は指数バックオフ再試行。各画像 最大2回試行（破綻時のみ1回だけ再生成）。

## ■元イラスト（aerial2 通し番号 → collect_aerial2/img/）
対象番号: 1,2,3,45,64,91,93,94,97,100,104,112,114,137,138,196,215,372,379,497,518,519,520,597,914
- `collect_aerial2/aerial2_index.csv` で各番号のファイル名・事故の型を引き、その元画像を「参照画像」として渡す。
- 元画像が特定できない番号は「該当なし」と明記しスキップ（捏造しない）。※25番号は全て実体確認済。

## ■生成内容（統一ルール）
- 元絵の「事故の型・構図・誰がどう被災するか」を読み取り引き継ぎ、舞台を展示会場ブース設営現場に置換。
- (a) 高所作業車は登場時すべて**シザース型（垂直昇降式・シザースリフト）**に統一（ブーム/トラック型にしない）。
- (b) タッチ統一：高品質・臨場感・リアル寄りの安全教育用イラスト（陰影と立体感のあるクリーンなプロ作画の災害事例イラスト風）。元絵のタッチに引きずられない。
- (c) 舞台＝日本の展示会場・ブース設営現場（組みかけブース、トラス、看板パネル、什器、搬入口等）。人物＝日本人作業員、あごひも付きヘルメット・蛍光ベスト・安全靴・(高所作業時)フルハーネス。
- (d) 事故の瞬間・危険が起きている状態を明確に（安定した通常作業の絵にしない）。
- (e) 画像内テキスト一切なし（文字/矢印/キャプション/吹き出し/記号なし）。流血なし。実在ロゴ/ブランドなし。
- 各元絵: OpenAI 2案 + Google 2案。生成後に自己点検（①シザース型②事故の瞬間③タッチ統一の高品質イラスト④文字/矢印/キャプション無し⑤PPE適切・流血/ロゴ無し）。明らかな破綻のみ1回だけ再生成（各最大2回試行）。

## ■保存 / index
- `gen_event_v20/{番号}/openai_1.png` `openai_2.png` `google_1.png` `google_2.png`（通常PNG・透過不要）。
- `gen_event_v20/event_index_v20.csv`：〔元番号, 元ファイル, 元の事故の型, 生成タイトル(展示会設営版の状況), 生成4枚のファイル, 使用モデル〕。

## ■作業の進め方（ランナーが1タスクずつ起動）
- `BACKLOG_EVENT.md` の未完最上段 `- [ ]` を**1つだけ**実行 → 完了で `- [x]` にして git push。
- 着手前に `gen_event_v20/{番号}/` を確認し未生成分のみ。未完が無ければ空ファイル `DONE_EVENT.flag` を作成し停止。
- usage/rate/429 到達時は WIP を保存・push して停止（ランナーが reset 時刻まで待ち自動再開）。

## ■対比PDF / 発行
- `compare_event_v20.pdf`：1元絵1ページ・見出し＝元番号＋事故の型。左に元イラスト（aerial2収集・出所ドメイン付）、右に生成4枚（OpenAI-1/OpenAI-2/Google-1/Google-2）を大きくラベル付きで並べる。見比べて選抜できる大きさ・歪み/見切れなし。
- `review_event/<ランダム32文字>/` に PDF＋index.html（静的・外部読込なし・noindex・スマホ縦・「開く/保存」＋iframe縦表示）。
- Vercel hakuten-review を**過去全トークンの union** で再デプロイ（既存URL全200保持・ルート/=404・HTTP200を curl 実測検証）。GitHub(master/main) へ push。
- `REPORT_EVENT.md`：公開URL／PDF直URL＋raw／生成枚数（元絵数×4）／特定できなかった番号／残課題 を記載し push。
