# RULES_ILLUST — 採用写真の「事故事例イラスト」化＋元写真vsイラスト対比（全自動・無人継続）

## ■安全（厳守）
- 削除/上書き禁止（追加・新ファイル名）。**既存成果物/テンプレ/photos_v15・photos_v16 は非破壊**。Chrome kill厳禁（taskkill厳禁）。
- **APIキー/認証情報の値は一切出力しない**（.env から読む・末尾マスクのみ可）。`.env` は触らない。
- 時刻は `powershell.exe -Command "Get-Date"`。python は `py`。push は origin main（master へ commit→push、続けて master:main を fast-forward。競合時 pull --rebase 後再push）。
- 着手前に `illust_v17/`・`compare_illust_v17.pdf`・`review_illust/` の既存を確認し未生成分のみ作る（再開安全）。
- 制限到達（usage/rate/429）時は WIP を保存・push して停止（ランナーが自動再開）。

## ■目的
V2で作った各事例の採用写真（`photos_v16/{N01..N15}/base.png`）を「事故事例イラスト」に再生成し、写実より物理破綻が緩和されるかを検証する。元写真 vs 生成イラストを左右対比したPDFを発行。

## ■対象（15事例）
- 元画像＝各事例のベース採用写真：`photos_v16/{N01..N15}/base.png`。
- 情景・事故内容は `img_index_v16.csv` の創作タイトル/事故種類（無ければ `cases_v2/` の発生事象1行）。機序は `gen_illust_v17.mjs` の MAP に定義済み。

## ① イラスト化（各事例：OpenAI＋Google 各1）
- 正準ジェネレータ `gen_illust_v17.mjs`：`node gen_illust_v17.mjs <N01..N15>` で `openai_illust.png`（gpt-image-2,quality=high）＋`google_illust.png`（gemini-3-pro-image-preview）を生成（既存スキップ・429backoff・モデル名記録）。
- プロンプト方針（MAPに実装済）：base.png を参照に **構図・事故の向き・接触点・機種・人数・PPE を保持**しつつ、画風だけ「日本の労働災害事例イラスト（KYT教材・安全ポスター風のクリーンなフラット/ベクター、線画＋平塗り、×印・矢印・衝撃線で危険強調）」へ変換。(a)事故内容を具体記述、(b)「写真でなくイラスト・被災の瞬間を明確に（確実に墜落/転倒/挟まれている＝危険が起きている絵。安定作業の絵にしない）」、(c)日本の会場/日本人/あごひもヘルメット・ハイビズ・安全靴・(高所)フルハーネス・実在ロゴ無し・流血無し、(d)写真版で「墜落しきっていない/踏ん張っている」ものはイラストで明確に重心が外・体が投げ出される構図へ補正。
- 生成後に自己点検（①事故の瞬間か②機種・向き・接触点が元と一致③イラスト調か④PPE/ロゴ/流血OK）。明らかな破綻のみ1回だけ再生成（各最大2回試行）。API がモデル名/形式でエラーなら `gen_illust_v17.mjs` の新名コピーで調整可（元は上書きしない）。キー値は出さない。
- 保存：`illust_v17/{N}/openai_illust.png・google_illust.png`＋`gen_meta.json`。`illust_index_v17.csv`〔新No,事故タイトル,元写真パス,イラスト2枚パス,使用モデル〕を更新。GitHub(main) push。

## ② 対比PDF `compare_illust_v17.pdf`
- 1事例1ページ、見出し＝新No＋事故タイトル。左に「元写真（ベース採用）」、右に「生成イラスト（OpenAI版・Google版の2枚）」を大きく対比配置（1ページに 写真1＋イラスト2 の計3枚）。各画像にラベル（元写真／イラスト:OpenAI／イラスト:Google）。歪み/見切れなく大きく。
- python(`py`)＋PIL で生成（既存PDFは上書きしない・新名）。

## ■公開・報告
- `review_illust/<ランダム32文字>/` に PDF＋index.html(静的・外部読込なし・noindex・スマホ縦・PDFを開く/保存＋iframe縦表示) を置き Vercel hakuten-review 再デプロイ（既存URL保持・ルート/=404・HTTP200検証）。PDF を GitHub(main) push。
- `REPORT_ILLUST.md`：公開URL/PDF直URL＋raw・生成枚数(成功/失敗)・各事例の使用モデル・破綻補正できた事例の所感・残課題 を記載し push（キー値非出力）。
