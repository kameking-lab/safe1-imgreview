# REPORT_LAYG — レイヤー合成サンプル（Googleのみ）報告

作成: 2026-06-19 JST / 生成エンジン: **Google gemini-3-pro-image-preview のみ（OpenAI不使用）**

## 1. 公開URL（Vercel hakuten-review・限定公開）
- レビューページ: https://hakuten-review.vercel.app/zss71y3ce9krvhk9ipip202s2vueh0s5/
  - 静的HTML・外部読込なし・`noindex`・スマホ縦最適化・PDFを開く/保存＋PPTXダウンロード＋iframe縦表示・たたき台注記入り。
- ルート `/` は **404**（限定公開を維持）。

### 直URL（Vercel）
- PDF: https://hakuten-review.vercel.app/zss71y3ce9krvhk9ipip202s2vueh0s5/sample_layers_v18.pdf
- PPTX: https://hakuten-review.vercel.app/zss71y3ce9krvhk9ipip202s2vueh0s5/sample_layers_v18.pptx

### 直URL（GitHub raw・main）
- PDF: https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_layg/zss71y3ce9krvhk9ipip202s2vueh0s5/sample_layers_v18.pdf
- PPTX: https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_layg/zss71y3ce9krvhk9ipip202s2vueh0s5/sample_layers_v18.pptx

### HTTP実測検証（2026-06-19 JST, curl）
| URL | 結果 |
|---|---|
| `/zss71y…/` | 200 text/html 5,372B |
| `…/sample_layers_v18.pdf` | 200 application/pdf 1,548,403B |
| `…/sample_layers_v18.pptx` | 200 (pptx) 13,589,806B |
| ルート `/` | 404 text/plain |
| 既存トークン(xdctnn/lkvz/ulwv/r7nq/fd9o 他 計27件) | 全200保持（過去全トークンをunionで束ねて維持） |
| GitHub raw PDF (main/master) | 各200 1,548,403B |

## 2. 素材数（Googleのみ生成・透過RGBA）
- **背景 3点**（`layers_v18/bg/`・不透過・人物なし）: bg_warehouse1 / bg_warehouse2 / bg_venue_dock
- **荷物 4点**（`layers_v18/obj/`・透過）: rollcage_collapsing / rollcage_tipping / rollcage_normal / panelcart_sliding
- **作業員 5点**（`layers_v18/worker/`・透過）: hand_pain / foot_crouch / fallen_back / startled / stand
  - 立ち姿は既存 `worker_stand_google.png` を非破壊で再利用。
- 配置用に透明余白をアルファ境界で切り出した `*_c.png`（崩れ荷物・倒れ/痛がる作業員）を追加生成（既存非破壊）。

## 3. 成果物
- `sample_layers_v18.pptx`（13.5MB / 3スライド）: (1)素材一覧、(2)合成見本 TGL墜落、(3)合成見本 TGL荷崩れ・下敷き。
  - **各パーツは個別の移動・回転・拡縮可能な画像オブジェクト**として背景全面の上に配置（1枚に焼き込まず）。各スライドに「たたき台・最終調整はパワポ上で」注記＋ノート明記。
- `sample_layers_v18.pdf`（1.5MB / 3ページ）: **PowerPoint COM**（`ppSaveAsPDF=32`）で書き出し（LibreOffice不在のためCOM使用・Chrome不可侵）。

## 4. 透過品質の所感
- rembg（onnxruntime）で背景除去 → マゼンタ点検で白フチ/欠けを確認。被写体内部の白（ヘルメット等）は保持され自然。
- 全体に白フチは最小。作業員の細部（手指・安全靴の縁）に僅かなエッジ残りがある程度で、合成上は許容範囲。
- 配置時の透明余白は `*_c.png`（アルファ境界クロップ）で回転中心・位置決めが容易になり、見本2枚とも白フチ・配置点検OK。

## 5. 残課題
- 作業員パーツのエッジ微残り（必要なら高解像度で1点ずつ再カット）。
- 合成見本は事故イメージの「たたき台」であり、実寸スケール・遠近・接地影は未調整（パワポ上で個別調整を想定）。
- 影/光源の整合（パーツごとの陰影方向）は今回未対応。必要なら影レイヤーを別途追加。

## 6. 安全・コンプライアンス
- 生成は **Google gemini-3-pro-image-preview のみ・OpenAI不使用**。
- 全工程**非破壊**（追加は新ファイル名、既存 `layers_v18` 等は再利用のみ）。rm/move/del・Chrome kill 不使用。
- APIキー値は非出力（.env から読込・末尾マスクのみ）。実在ロゴ無し・流血なし。
