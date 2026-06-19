# RULES_LAYV19 — 視点固定レイヤー合成サンプル（Googleのみ）全自動

## ■安全（厳守）
- 削除/上書き禁止（追加・新ファイル名）。**既存非破壊**（layers_v18等は触らない）。Chrome kill厳禁（taskkill厳禁）。
- **今回 OpenAI は使わない（Googleのみ＝Nano Banana Pro=gemini-3-pro-image-preview）**。APIキー値は出力しない（.env から読む・末尾マスクのみ）。
- 時刻は `powershell.exe -Command "Get-Date"`。python は `py`。push は origin main（master へ commit→push、続けて master:main を fast-forward。競合時 pull --rebase 後再push）。
- 着手前に `layers_v19/`・`sample_layers_v19.pptx`・`review_layer_v19/` の既存を確認し未生成分のみ作る（再開安全）。
- 制限到達（usage/rate/429）時は WIP を保存・push して停止（ランナーが自動再開）。

## ■核心：視点・カメラアングルを固定して「最初から角度を揃える」
- 各シチュごとに**カメラ視点を1つ決め打ち**し、背景・荷物・作業員の全パーツを**同じ視点・同じ目線高さ・同じパース・同じ光源方向**で生成する。後からパワポで回転して合わせるのではなく、生成時点で角度を一致させる。
- 視点記述は**全パーツ共通の英語フレーズを使い回す**（プロンプト末尾に必ず付ける）。
- **視点A（TGL）固定フレーズ**：`Camera: eye-level, ~3m from the subject, slightly elevated 15 degrees, viewpoint from the REAR-LEFT of the truck, 50mm lens, soft natural daylight from the upper-left. Keep this exact perspective, eye height, vanishing lines and lighting.`
- **視点B（高所作業車）固定フレーズ**：`Camera: from the ground looking slightly UP at the machine, viewpoint from the FRONT-DIAGONAL (front-left), 35mm lens, soft natural daylight from the upper-left. Keep this exact perspective, low eye height, vanishing lines and lighting.`
- パーツは**純白背景・被写体のみ・影最小**で生成し、cutout（rembg優先・無ければ Pillow）で透過PNG化。

## ■生成ツール（流用）
- 画像生成：`node gen_img.mjs google OUTPATH.png "PROMPT"`（**openai は使わない**。既存スキップ・429backoff・キー値非出力）。
- 透過化：rembg が入っていれば rembg（`py` で `rembg.remove`）、無ければ `py cutout_white.py IN OUT`。白フチ最小化・サムネ自己点検・ひどければ1回だけ再処理。

## ■シチュ1：TGL（荷崩れ・下敷き）— 全パーツ視点A
- 背景 `layers_v19/tgl/bg_tgl.png`（不透過・人物なし）：「日本の倉庫、テールゲートリフター付きトラック後部、昇降板が下りた状態、荷台に荷、ロゴ無し、**人物なし**、写真」＋視点A。
- 荷物 `layers_v19/tgl/obj_rollcage_collapsing.png`（RGBA）：「ロールボックスパレット(カゴ車)に段ボールを積み、崩れて傾いた状態、純白背景・被写体のみ・影最小」＋視点A→透過。
- 作業員 `layers_v19/tgl/worker_pinned.png`（RGBA）：「日本人作業員、あごひもヘルメット・ハイビズ・安全靴、カゴ車の下敷きになり倒れて手で防ぐポーズ、純白背景・被写体のみ・**流血なし**」＋視点A→透過。

## ■シチュ2：高所作業車（バスケットでの被災）— 全パーツ視点B
- 背景 `layers_v19/aerial/bg_aerial.png`（不透過・人物なし）：「日本の現場/会場、高所作業車（ブーム式・トラック型）が立ち上がった状態、バスケット空、ロゴ無し、**人物なし**、写真」＋視点B。
- 作業員 `layers_v19/aerial/worker_basket.png`（RGBA）：「日本人作業員、あごひもヘルメット・ハイビズ・**フルハーネス**、バスケット内で上方構造物に頭をはさまれる/墜落しかけるポーズ、純白背景・被写体のみ・**流血なし**」＋視点B→透過。
- （任意）高所の荷/看板パーツがあれば視点Bで1枚→透過。

## ■PowerPoint合成 `sample_layers_v19.pptx`（python-pptx・新規）
- (1) **素材一覧**：TGL/高所それぞれ 背景・パーツのサムネ＋ラベル＋**各パーツの「視点」を明記**（視点A/視点B）。
- (2) **合成見本（1セットでよい・TGLで可）**：背景を全面に敷き、**同じ視点で作った崩れカゴ車＋倒れ作業員を、回転は最小限（理想は無回転）でそのまま重ねて**事故シーンを1つ作る。**各パーツは個別の画像オブジェクト**（焼き込まない＝移動・回転・拡縮可能）。注記「視点固定方式の検証・たたき台」。
- PDF化は **PowerPoint COM**（LibreOffice不在）で `sample_layers_v19.pdf` に出力（Chrome不可侵）。

## ■公開・報告
- `review_layer_v19/<ランダム32文字>/` に pptx＋PDF＋index.html(静的・外部読込なし・noindex・スマホ縦・pptxダウンロード＋PDFを開く/保存＋iframe縦表示) を置き Vercel hakuten-review 再デプロイ。**過去の全レビュートークンをunionで束ね既存URLを全て200保持**。ルート/=404・HTTP200検証。pptx/PDFを GitHub(main) push。
- `REPORT_LAYV19.md`：公開URL/pptx・PDF直URL＋raw・素材数(TGL/高所)・**視点が揃ったかの所感**・残課題 を記載し push（キー値非出力）。OpenAI不使用を明記。
