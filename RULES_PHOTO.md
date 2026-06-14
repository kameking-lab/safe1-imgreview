# RULES_PHOTO — 選定17元絵 × 4枚（実写化＋イベント設営版 / OpenAI・Google）写真生成（全自動・無人継続）

## ■安全（厳守）
- 削除/上書き禁止（追加は新ファイル名）。Chrome kill厳禁（taskkill厳禁）。**APIキー/認証情報の値はログ・チャット・報告・コミットに一切出力しない**（末尾マスクのみ可）。
- 時刻は `powershell.exe -Command "Get-Date"`。push は origin main(=master) に append-only。競合したら pull --rebase 後に再push（master へ commit→push、続けて master:main を fast-forward）。
- 着手前に `photos_v15/` の既存を確認し、**未生成分のみ作る**（再開で重複/破壊しない）。今回は画像「生成」する（収集ではない）。
- `.gitignore` の `.env` は対象外のまま（キーをコミットしない）。

## ■APIキー（.envから読む・値は出力しない）
- `.env` から `OPENAI_API_KEY` / `GEMINI_API_KEY` を読む（環境変数/process.env）。未設定なら「キー未設定」と報告して停止。
- **OpenAI**＝`gpt-image-2`（Images API・参照画像=元絵を渡す edits、quality=high、size=1024x1024）。無ければ `gpt-image-1` にフォールバックし使用モデル名を記録。レスポンスの base64 を直接保存（ブラウザDL不使用）。
- **Google**＝`gemini-3-pro-image-preview`（Nano Banana Pro）。無ければ `gemini-2.5-flash-image`（Nano Banana）にフォールバックし使用モデル名を記録。参照画像=元絵を渡す。base64保存。
- 429/レート時は Exponential backoff で自動リトライ。日次無料枠超過時はログに記録し**継続**（停止しない）。

## ■生成器
- 正準ジェネレータ `gen_photo.mjs` を使う：`node gen_photo.mjs <番号>` で当該元絵の A/B/C/D 4枚を生成・保存・モデル名記録まで行う（既存ファイルはスキップ＝再開安全）。
- API がモデル名/エンドポイントでエラーを返す場合は、`gen_photo.mjs` を**新名のコピーで**調整（モデル名フォールバック・リクエスト形式）して再実行してよい（元の `gen_photo.mjs` は上書きしない）。キー値は決して出力しない。

## ■対象17元絵（collect2/img/ の通し番号。詳細は collect2/img_index.csv）
- TGL: 0001, 0002, 0003, 0017, 0019
- 高所: 0040, 0041, 0042, 0043, 0044, 0046, 0050, 0052, 0054, 0057, 0060, 0071

## ■各元絵で作る4枚
- **A 実写化(OpenAI)**：元絵の構図・力の向き・接触点・機種を厳守し、日本の現場のリアル写真化。
- **B 実写化(Google)**：同上を Google モデルで。
- **C イベント設営版(OpenAI)**：同じ事故機序のまま文脈を「展示会・イベント設営の現場」へ（TGLの荷=展示用パネル/什器、高所作業車=会場での看板取付/展示ブース組立/天井トラス施工）。背景・荷・服装をイベント設営に寄せるが、**事故の向き・接触点・機種は崩さない**。
- **D イベント設営版(Google)**：同上を Google モデルで。
- 全画像共通：日本の現場・日本人・あごひもヘルメット/ハイビズ/安全靴・(高所は)フルハーネス、日本仕様機材（掘削機にしない）、実在ロゴ無し、流血無し、危険の瞬間。元絵の「何がどちらに倒れ/落ち/挟まれ、人がどう被災するか」を厳密に再現。

## ■生成と自己点検
- 各画像：生成→開いて自己採点（①元絵構図に合致(向き・接触点) ②機種が正しい ③日本ローカライズ/PPE ④AI破綻無し ⑤ロゴ無し ⑥写真の自然さ）。**明確な破綻のみ1回だけ再生成**（各最大2回試行）。スパークル等の透かしは除去。
- 保存：`photos_v15/{番号}/A_openai.png` / `B_google.png` / `C_openai_event.png` / `D_google_event.png`。各番号フォルダに `source_ref.png`（元絵のコピー）と `gen_meta.json`（使用モデル名・試行回数）を置く。GitHub(main)へ push。

## ■最終発行
- `photos_v15_catalog.pdf`（元絵ごとに 元絵→A/B/C/D を並べ、番号・モデル名・実写/イベント版を明記）。
- `review_photo/<ランダム32文字>/` に PDF＋index.html(静的・外部読込なし・noindex・スマホ縦) を置き Vercel hakuten-review に再デプロイ（既存URL保持・ルート/=404・HTTP200）。PDF を GitHub(main) へ push。
- `REPORT_PHOTO.md` に 公開URL/PDF直URL＋raw・生成枚数(成功/失敗)・各元絵の使用モデル名(OpenAI/Google)・失敗や未生成の一覧 を記載し push（キー値は出力しない）。
