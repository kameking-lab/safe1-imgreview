# RULES_LAYG — レイヤー合成サンプル（Googleのみ）全自動

## ■安全（厳守）
- 削除/上書き禁止（追加・新ファイル名）。**既存非破壊**（既存の `layers_v18/worker/worker_stand_google.png` 等は再利用可・壊さない）。Chrome kill厳禁（taskkill厳禁）。
- **今回 OpenAI は使わない（Googleのみ＝Nano Banana Pro=gemini-3-pro-image-preview）**。APIキー値は出力しない（.env から読む・末尾マスクのみ）。
- 時刻は `powershell.exe -Command "Get-Date"`。python は `py`。push は origin main（master へ commit→push、続けて master:main を fast-forward。競合時 pull --rebase 後再push）。
- 着手前に `layers_v18/`・`sample_layers_v18.pptx`・`review_layer/` の既存を確認し未生成分のみ作る（再開安全）。
- 制限到達（usage/rate/429）時は WIP を保存・push して停止（ランナーが自動再開）。

## ■生成ツール（流用）
- 画像生成：`node gen_img.mjs google <out.png> "<prompt>"`（Google=gemini-3-pro-image-preview。**openai は使わない**。既存スキップ・429backoff・キー値非出力）。
- 透過化：まず `py -m pip install rembg onnxruntime`（数分）を試行し、入れば rembg で背景除去、不可なら `py cutout_white.py <in> <out>`（純白背景→外周連結白のみ透過・輪郭フェザー）。白フチ最小化・サムネで自己点検。

## ■生成する素材（2シチュ：TGL墜落／TGL荷崩れ・下敷き）
### A. 背景 `layers_v18/bg/bg_*.png`（不透過・人物なし）
- 倉庫TGL×2〜3：「日本の倉庫/物流現場、テールゲートリフター付きトラック後部、昇降板が下りた状態、荷台に荷、周囲に什器、自然光、実在ロゴ無し、**人物なし**、写真」。
- 会場搬入口×1：「日本の展示会・イベント会場の搬入口、テールゲートリフター付きトラック、昇降板が下りた状態、自然光、ロゴ無し、人物なし、写真」。
- ファイル名例：bg_warehouse1.png / bg_warehouse2.png / bg_venue_dock.png。

### B. 荷物パーツ `layers_v18/obj/obj_*.png`（透過RGBA）
- ロールボックスパレット(カゴ車)＋段ボール/什器の **崩れかけ/転倒中/正常**、展示パネル台車が傾き滑落しかけ。**純白背景・被写体のみ・影最小**で生成→透過化。ファイル名例：obj_rollcage_collapsing.png / obj_rollcage_tipping.png / obj_rollcage_normal.png / obj_panelcart_sliding.png。

### C. 作業員パーツ `layers_v18/worker/worker_*.png`（透過RGBA）
- 日本人作業員、あごひもヘルメット・ハイビズ・安全靴（必要に応じフルハーネス）、ポーズ＝手を押さえて痛がる/足を押さえてしゃがむ/仰向けに倒れて意識なし/驚いて後方へバランスを崩す/普通に立つ。**純白背景・被写体のみ・流血なし**→透過化。ファイル名例：worker_hand_pain.png / worker_foot_crouch.png / worker_fallen_back.png / worker_startled.png / worker_stand.png（**worker_stand_google.png は既存を再利用してよい**）。

## ■透過品質
- 白フチ・欠け最小化。cutout_white.py は外周連結白のみ抜くので被写体内部の白（ヘルメット等）は残る。ひどい白フチ/欠けは**1回だけ**再生成/再処理。RGBAで保存。

## ■PowerPoint合成 `sample_layers_v18.pptx`（python-pptx・新規）
- (1) **素材一覧**：背景・荷物・作業員のサムネ＋ラベル。
- (2) **合成見本**（**2シチュ：TGL墜落／TGL荷崩れ**）：背景を全面に敷き、その上に「崩れ荷物パーツ＋倒れる/痛がる作業員パーツ」を事故に見える位置・サイズ・**回転角(rotation)** で配置。**各パーツは個別の画像オブジェクト**（1枚に焼き込まない＝移動・回転・拡縮可能）。
- 各スライドに注記「これはレイヤー合成のたたき台。各部品は移動・回転・拡縮可能。最終調整はパワポ上で」。
- PDF化は **PowerPoint COM**（LibreOffice不在）で `sample_layers_v18.pdf` に出力（Chrome不可侵）。

## ■公開・報告
- `review_layer/<ランダム32文字>/` に pptx＋PDF＋index.html(静的・外部読込なし・noindex・スマホ縦・pptxダウンロード＋PDFを開く/保存＋iframe縦表示) を置き Vercel hakuten-review 再デプロイ。**過去の全レビュートークンをunionで束ね既存URLを全て200保持**（compare3/illust/study/study2 等）。ルート/=404・HTTP200検証。pptx/PDFを GitHub(main) push。
- `REPORT_LAYG.md`：公開URL/pptx・PDF直URL＋raw・素材数(背景/荷物/作業員)・透過品質の所感・残課題 を記載し push（キー値非出力）。OpenAI不使用を明記。
