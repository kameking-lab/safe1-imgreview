# RULES_V2 — 博展向け最終版パワポ＋動画プロンプト集（全自動・無人継続）

## ■安全（厳守）
- 削除/上書き禁止（追加・新ファイル名）。**既存pptx/テンプレ/photos_v15 は非破壊**。Chrome kill厳禁（taskkill厳禁）。
- **APIキー/認証情報の値はログ・チャット・報告・コミットに一切出力しない**（.env から読む・末尾マスクのみ可）。`.env`(.gitignore済) は触らない。
- 時刻は `powershell.exe -Command "Get-Date"`。python は `py`。push は origin main（master へ commit→push、続けて master:main を fast-forward。競合時 pull --rebase 後再push）。
- 着手前に既存（`photos_v16/`・`cases_v2/`・`hakuten_jirei_v2.pptx`・`video_prompts_v16.*`・`review_v2/`）を確認し未完分のみ作る（再開安全）。
- 制限到達（usage/rate/429）時は WIP を保存・push して停止（ランナーが自動再開）。

## ■採用15事例と新通し番号（#0041・#0060は没・番号詰め直し）
新No ← 旧番号 / 採用案（実体＝`photos_v15/{旧}/{採用}.png`）:
N01←0001/A_openai, N02←0002/A_openai, N03←0003/D_google_event, N04←0017/D_google_event, N05←0019/C_openai_event, N06←0040/C_openai_event, N07←0042/D_google_event, N08←0043/D_google_event, N09←0044/D_google_event, N10←0046/D_google_event, N11←0050/D_google_event, N12←0052/D_google_event, N13←0054/D_google_event, N14←0057/C_openai_event, N15←0071/C_openai_event。
- TGL＝N01〜N05、高所＝N06〜N15。各Nの機序・創作タイトル・設営文脈は `gen_v16.mjs` の MAP に定義済み（流用）。

## ① 画像リアル化（各事例3枚：base＋OpenAI＋Google）
- 正準ジェネレータ `gen_v16.mjs`：`node gen_v16.mjs <N01..N15>` で base.png（採用コピー）＋openai.png（gpt-image-2,quality=high）＋google.png（gemini-3-pro-image-preview）を生成（既存スキップ・429backoff・モデル名記録）。
- プロンプト方針（MAPに実装済）：採用画像の構図・事故の向き・接触点・機種を保持しつつ、(a)写真リアリティ向上（自然光/質感/被写界深度/現場の雑多さ）、(b)「展示会・イベント設営中にありそうな事故」へ寄せる創作（TGL=展示パネル/什器、高所=看板取付/ブース組立/天井トラス/照明設置 等）、(c)日本の会場・日本人・あごひもヘルメット/ハイビズ/安全靴/(高所)フルハーネス、実在ロゴ無し・流血無し・危険の瞬間。採用画像の不自然点（手足破綻/機種違い/物理矛盾/PPE欠落）の是正指示を含む。
- 生成後に自己点検し明らかな破綻のみ1回だけ再生成（各最大2回試行）。API がモデル名/形式でエラーなら `gen_v16.mjs` の新名コピーで調整可（元は上書きしない）。キー値は出さない。
- 保存：`photos_v16/{新No}/base.png,openai.png,google.png`＋`gen_meta.json`。`img_index_v16.csv`〔新No,旧番号,創作タイトル,元採用案,3ファイル〕を更新。GitHub(main) push。

## ② 最終パワポ `hakuten_jirei_v2.pptx`（新規・テンプレ踏襲・非破壊）
- `template_spec.md`/博展版面に従い、表紙＋15事例×2スライド（写真スライド＋項目スライド）。
- 写真スライド：3枚（base/OpenAI/Google）を横並びで大きく配置。**AIモデル名ラベルは載せない**（客先向け）。注記は「複数案・選抜用」程度の控えめのみ（無くても可）。
- 題名：各事例、画像（イベント設営の事故）に合った**創作タイトルに刷新**（MAPのtitle活用）。表紙タイトルも内容に合わせ刷新可（例「イベント設営現場 想定事故事例集（全15事例）」）。**創作である旨は表紙に1行だけ**控えめに（各スライドに繰り返さない）。
- 項目（下段）：発生事象／原因概要（箇条書き）／対応（想定・箇条書き）／対策概要（箇条書き）。各スライドに**監修：金田 義太（登録第4840号）**。
- 出典：一次主張ではなく**「参考資料」として控えめ**に（スライド隅か巻末一括）。検証済URL（あんぜんサイト/建荷協）を小さく。創作のため「参考にした災害事例」という位置づけ。
- AI生成注記は**表紙に1行のみ**。

## ③ 動画プロンプト集 `video_prompts_v16.(md/pdf)`（別資料）
- 15事例それぞれ：採用ベース画像＋（あれば）リアル化画像を載せ、その下に〔前→事故の瞬間→後〕の3フェーズの動画プロンプトを **OpenAI(Sora 2)用** と **Google(Veo 3.1)用** の2種、**日本語と英語併記**で提示。**image-to-video前提**（この画像を開始/キーフレームに）。8秒前後・日本の会場・PPE・流血なし・危険の瞬間。
- 安全フィルタ回避の配慮（過度に残虐にしない・「安全教育用の再現」の文脈）を各プロンプトに含める。
- ①のパワポとは別ファイル（`video_prompts_v16.pdf`）として発行。

## ■QA（観点①〜⑩・最大4ラウンド・問題ゼロで早期終了）
①写真3枚が歪み/重なり/見切れ無く綺麗 ②題名がイベント設営の事故内容と整合 ③発生事象/原因/対応/対策が箇条書きで埋まり文字溢れ無し ④AIモデル名ラベル非表示 ⑤AI/創作注記は表紙に最小限・各スライドでくどくない ⑥出典は参考資料として控えめ（検証済URL） ⑦監修表記 ⑧通し番号N01〜N15が連番で没番号が残っていない ⑨動画プロンプトが15事例分・Sora2/Veo3.1・日英・3フェーズ・image-to-video前提で揃う ⑩客先体裁。
- pptx→PDF/PNG は **PowerPoint COM**（LibreOffice不在）で変換し目視。各ラウンド `QA_V2_r{n}.md` に記録。問題ゼロ or 最大4ラウンドで打ち切り、残課題は正直報告。修正は新コミットで積み各ラウンド後 push。

## ■公開・報告
- `review_v2/<ランダム32文字>/` に pptx＋そのPDF＋`video_prompts_v16.pdf`＋index.html(静的・外部読込なし・noindex・スマホ縦・各DL＋iframe縦表示) を置き Vercel hakuten-review 再デプロイ（既存URL保持・ルート/=404・HTTP200検証）。成果物を GitHub(main) push。
- `REPORT_V2.md`：公開URL/各PDF直URL＋raw・生成枚数・各事例タイトル・動画プロンプト件数・残課題 を記載し push（キー値非出力）。
