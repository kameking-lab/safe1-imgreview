# RULES_LAYER — レイヤー合成方式の試作（背景＋透過パーツ→PowerPoint合成・全自動）

## ■安全（厳守）
- 削除/上書き禁止（追加・新ファイル名）。**既存成果物/テンプレ/photos は非破壊**。Chrome kill厳禁（taskkill厳禁）。
- **APIキー/認証値は出力しない**（.env から読む・末尾マスクのみ）。`.env` は触らない。
- 時刻は `powershell.exe -Command "Get-Date"`。python は `py`。push は origin main（master へ commit→push、続けて master:main を fast-forward。競合時 pull --rebase 後再push）。
- 着手前に `layers_v18/`・`sample_layers_v18.pptx`・`review_layer/` の既存を確認し未生成分のみ作る（再開安全）。
- 制限到達（usage/rate/429）時は WIP を保存・push して停止（ランナーが自動再開）。

## ■目的（方式検証）
背景＋透過パーツ（荷物/作業員）を生成し、PowerPointに個別オブジェクトとして貼付・回転・配置した「事故の瞬間」のたたき台を作る。まず **TGL墜落** と **TGL荷崩れ/下敷き** の2シチュで方式を検証。最終微調整はユーザーがパワポ上で行う前提（パーツは1枚に焼き込まず個別配置）。

## ■生成ツール（流用）
- 画像生成：`node gen_img.mjs <openai|google> <out.png> "<prompt>" [transparent]`（OpenAI=gpt-image-2 / Google=gemini-3-pro-image-preview。OpenAIは `transparent` 指定で背景透過PNGをネイティブ生成。既存スキップ・429backoff・キー値非出力）。両モデルで素材を作り見比べる。
- 透過化：`py cutout_white.py <in.png> <out.png>`（純白背景→外周連結白のみ透過・輪郭フェザー。rembg不在のためPillowフォールバック）。Google素材や白背景生成物に適用。OpenAIは `transparent` でネイティブ透過が得られるためそのまま使用可（必要なら cutout も可）。

## ■生成する素材（2シチュ分）
### A. 背景 `layers_v18/bg/bg_*.png`（不透過・人物なし）
- 倉庫/物流現場×2〜3：「日本の倉庫/物流現場、テールゲートリフター付きトラック後部、昇降板が下りた状態、荷台に荷、周囲に什器、自然光、実在ロゴ無し、**人物なし**、写真」。
- 会場搬入口×1：「日本の展示会・イベント会場の搬入口、テールゲートリフター付きトラック、昇降板が下りた状態、自然光、実在ロゴ無し、人物なし、写真」。
- 各 OpenAI版・Google版を作って見比べてよい（ファイル名に provider を含める：例 bg_warehouse1_openai.png）。

### B. 荷物パーツ `layers_v18/obj/obj_*.png`（透過RGBA）
- 「ロールボックスパレット(カゴ車)に段ボール/什器を積んだもの」の **崩れかけ/転倒中/正常** 各1〜2、「展示パネルを積んだ台車が傾いて滑落しかけ」等。**純白背景・被写体のみ・影最小**で生成→透過化。ファイル名に状態（obj_rollcage_collapsing.png 等）。

### C. 作業員パーツ `layers_v18/worker/worker_*.png`（透過RGBA）
- 「日本人作業員、あごひもヘルメット・ハイビズ・安全靴、必要に応じフルハーネス」、ポーズ＝①手を押さえて痛がる ②足を押さえてしゃがむ ③仰向けに倒れて意識なし ④驚いて後方へバランスを崩す ⑤普通に立つ。**純白背景・被写体のみ・流血なし**→透過化。ファイル名にポーズ（worker_hand_pain.png / worker_foot_crouch.png / worker_fallen_back.png / worker_startled.png / worker_stand.png）。

## ■透過品質
- 白フチ・欠けが残らないよう処理（cutout_white.py は外周連結白のみ抜くので被写体内部の白＝ヘルメット等は残る）。サムネで白フチ/欠けを自己点検し、ひどければ**1回だけ**再生成/再処理。透過済みは RGBA で保存。

## ■PowerPoint合成 `sample_layers_v18.pptx`（python-pptx・新規）
- シチュごとに2種スライド：
  (1) **素材一覧**：背景・荷物・作業員のサムネを並べ、どんな部品があるかラベル表示。
  (2) **合成見本**：背景写真を全面に敷き、その上に「崩れかけ荷物パーツ＋痛がる/倒れる作業員パーツ」を、事故に見える位置・サイズ・**回転角(rotation)** で配置（例＝昇降板付近に傾いたパレット＋その下/脇に倒れた作業員）。**各パーツは個別の画像オブジェクトとして配置**（1枚に焼き込まない＝後から移動・回転・拡縮可能）。
  - 各合成見本は **OpenAI素材版・Google素材版の2枚**作り、どちらの素材が合成に向くか見比べ可能に。配置はラフでよい。
- 注記「これはレイヤー合成のたたき台。各部品は移動・回転・拡縮可能。最終調整はパワポ上で」を各スライドに。
- PDF化は **PowerPoint COM**（LibreOffice不在）で `sample_layers_v18.pdf` に出力（Chrome不可侵）。

## ■公開・報告
- `review_layer/<ランダム32文字>/` に pptx＋PDF＋index.html(静的・外部読込なし・noindex・スマホ縦・各DL＋iframe縦表示) を置き Vercel hakuten-review 再デプロイ。**過去の全レビュートークンをunionで束ね既存URLを全て200保持**（compare3/illust lkvz/study ulwv/study2 xdct 等）。ルート/=404・HTTP200検証。pptx/PDFを GitHub(main) push。
- `REPORT_LAYER.md`：公開URL/pptx・PDF直URL＋raw・生成素材数(背景/荷物/作業員)・透過品質の所感・OpenAI vs Google素材の所感・残課題 を記載し push（キー値非出力）。
