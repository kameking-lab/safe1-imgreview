# REPORT_LAYV19 — 視点固定レイヤー合成サンプル（Googleのみ）報告

作成: 2026-06-19 JST / 生成エンジン: **Google gemini-3-pro-image-preview のみ（Nano Banana Pro・OpenAI不使用）**

## 1. 公開URL（Vercel hakuten-review・限定公開）
- レビューページ: https://hakuten-review.vercel.app/rmxvfbydhhjmtns3s0tdqgw7fnm8romw/
  - 静的HTML・外部読込なし・`noindex`・スマホ縦最適化・PDFを開く/保存＋PPTXダウンロード＋iframe縦表示・「視点固定方式の検証・たたき台」注記入り。
- ルート `/` は **404**（限定公開を維持）。

### 直URL（Vercel）
- PDF: https://hakuten-review.vercel.app/rmxvfbydhhjmtns3s0tdqgw7fnm8romw/sample_layers_v19.pdf
- PPTX: https://hakuten-review.vercel.app/rmxvfbydhhjmtns3s0tdqgw7fnm8romw/sample_layers_v19.pptx

### 直URL（GitHub raw・main）
- PDF: https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_layer_v19/rmxvfbydhhjmtns3s0tdqgw7fnm8romw/sample_layers_v19.pdf
- PPTX: https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_layer_v19/rmxvfbydhhjmtns3s0tdqgw7fnm8romw/sample_layers_v19.pptx

### HTTP実測検証（2026-06-19 JST, curl）
| URL | 結果 |
|---|---|
| `/rmxvfb…/` | 200 text/html 5,658B |
| `…/index.html` | 200 text/html 5,658B |
| `…/sample_layers_v19.pdf` | 200 application/pdf 949,106B |
| `…/sample_layers_v19.pptx` | 200 (pptx) 3,067,185B |
| ルート `/` | 404 |
| 既存トークン（zss71y / xdctnn / lkvzuf / r7nqos 他・計29件） | 全200保持（過去全トークンをunionで束ねて維持） |
| GitHub raw main PDF / PPTX | 各200（949,106B / 3,067,185B） |

## 2. 素材数（Googleのみ生成・視点固定）
**核心：シチュごとにカメラ視点を1つ決め打ちし、背景・荷物・作業員を同一視点・同一目線高さ・同一パース・同一光源で生成（生成時点で角度を一致）。**

- **シチュ1 TGL（荷崩れ・下敷き）= 全パーツ視点A**（`layers_v19/tgl/`・3点）
  - `bg_tgl.png`（不透過・人物なし・TGL付きトラック後部、昇降板降下）
  - `obj_rollcage_collapsing.png`（透過RGBA・崩れて傾いたカゴ車）
  - `worker_pinned.png`（透過RGBA・下敷きで手で防ぐポーズ・流血なし）
- **シチュ2 高所作業車（バスケット被災）= 全パーツ視点B**（`layers_v19/aerial/`・2点）
  - `bg_aerial.png`（不透過・人物なし・ブーム立上）
  - `worker_basket.png`（透過RGBA・フルハーネス・バスケット内被災ポーズ・流血なし）
- 配置用に透明余白をアルファ境界で切り出した `*_c.png`（崩れカゴ車・倒れ作業員・バスケット作業員）を追加生成（既存非破壊）。
- 視点フレーズ（プロンプト末尾で全パーツ共通使い回し）: 視点A=REAR-LEFT・eye-level・15°仰角・50mm、視点B=FRONT-DIAGONAL・低位置から見上げ・35mm。光源はいずれも upper-left で統一。

## 3. 成果物
- `sample_layers_v19.pptx`（3.0MB / 2スライド）: (1)素材一覧（TGL/高所の背景・パーツに**視点A/視点Bを明記**）、(2)合成見本（TGL1セット）。
  - 合成見本は `bg_tgl` を全面に敷き、**同じ視点Aで生成した崩れカゴ車＋下敷き作業員を回転0°でそのまま重ねて**事故シーンを1つ作成。**各パーツは個別の移動・回転・拡縮可能な画像オブジェクト**（焼き込まず）。注記「視点固定方式の検証・たたき台」。
- `sample_layers_v19.pdf`（949KB / 2ページ）: **PowerPoint COM**（`ppSaveAsPDF=32`）で書き出し（LibreOffice不在のためCOM使用・Chrome不可侵）。

## 4. 視点が揃ったかの所感
- **視点固定方式は有効**。背景・荷物・作業員を最初から同一フレーズ（目線高さ・パース・光源方向）で生成したため、TGL合成見本では**ほぼ無回転（回転0°）で重ねても破綻せず**、消失線・接地の感覚が概ね一致した。従来の「後からパワポで回転して合わせる」手間が大幅に減った。
- 光源を upper-left に統一したことで、各パーツの陰影方向の食い違いが目立たない。
- 一方、**スケール（被写体の大きさ）と接地点（足元・カゴ車底面の床位置）は生成任せでは完全一致しない**ため、合成見本では位置・拡縮の微調整を行った（個別オブジェクトのまま）。視点B（高所）は今回カタログ掲載のみで合成見本は未作成。

## 5. 残課題
- スケール・接地影は視点固定でも自動一致しないため、最終はパワポ上で個別微調整が前提（今回はたたき台）。
- 視点B（高所作業車）の合成見本は未作成。必要なら同方式で1セット追加。
- 透過パーツのエッジ微残り（必要なら高解像度で1点ずつ再カット）。
- 影/接地影レイヤーは未付与。リアリティを上げるなら別途影レイヤーを追加。

## 6. 安全・コンプライアンス
- 生成は **Google gemini-3-pro-image-preview のみ・OpenAI不使用**。
- 全工程**非破壊**（追加は新ファイル名、既存 `layers_v18` 等は再利用のみ）。rm/move/del・Chrome kill 不使用。
- APIキー値は非出力（.env から読込・末尾マスクのみ）。実在ロゴ無し・流血なし。
