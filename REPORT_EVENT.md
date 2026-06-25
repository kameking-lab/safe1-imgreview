# REPORT_EVENT — 展示会場 設営中の事故事例イラスト 生成 最終レポート

作成日時: 2026-06-25 17:31 (+09:00, `Get-Date`)
対象成果物: `gen_event_v20/`（生成画像100枚＋索引）/ `compare_event_v20.pdf`（25元絵×1頁・A4横の対比PDF）

## ■公開URL
- 公開ページ（限定／noindex・スマホ縦・「開く/保存」＋iframe縦表示）:
  `https://hakuten-review.vercel.app/9wz8nqi5y1g5tfjf601id0yu8y2d2m0i/`
- PDF直URL:
  `https://hakuten-review.vercel.app/9wz8nqi5y1g5tfjf601id0yu8y2d2m0i/compare_event_v20.pdf`
- PDF raw（GitHub）:
  `https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/review_event/9wz8nqi5y1g5tfjf601id0yu8y2d2m0i/compare_event_v20.pdf`

実測検証（本レポート作成時 2026-06-25 JST, curl）:
- 公開ページ `/9wz8…/` = **200**（text/html・4,306B）
- PDF直URL = **200**（application/pdf・6,651,972B）
- PDF raw（GitHub）= **200**（6,651,972B・直URLとサイズ一致）
- ルート `/` = **404**（text/plain）
- 既存含む全32トークン = **200**（non-200=0）※直近DEPLOYタスクで実測済

## ■生成枚数
**合計 100枚**（元絵25番号 × 4枚＝OpenAI 2案＋Google 2案）。
- 内訳: OpenAI `gpt-image-2`（quality=high・images/edits）50枚 ＋ Google `gemini-3-pro-image-preview`（generateContent inlineData）50枚。
- 索引 `gen_event_v20/event_index_v20.csv` = 25行（ヘッダ除く）。全番号で `openai_1/2.png` `google_1/2.png` 4枚を確認。
- 補助ファイル `_ref_openai.png`（64・497＝.gif元絵をOpenAI editsへ渡すためのPNG変換）2件は成果物カウント外。

### 対象番号（事故の型別）
| 事故の型 | 番号 | 件数 |
|---|---|---|
| 墜落・転落 | 1,2,3,45,64,91,93,94,97,100,104,112,114,137,138,196,215 | 17 |
| 挟まれ・巻き込まれ | 372,379 | 2 |
| 転倒・横転 | 497,518,519,520,597 | 5 |
| その他 | 914 | 1 |
| **合計** | | **25** |

各番号は `collect_aerial2/aerial2_index.csv` で元ファイル名・事故の型を引き、その元画像を参照画像として渡して生成。
舞台＝展示会場ブース設営現場、高所作業車はシザース型に統一、事故の瞬間、文字/矢印/キャプション無し・流血/実在ロゴ無し・PPE適切を各画像で自己点検し合格。

## ■特定できなかった番号
- **なし**（対象25番号すべて `collect_aerial2/img/` に実体を確認し生成完了）。

## ■残課題
- なし（生成・対比PDF・限定公開デプロイ・本レポートまで完了）。BACKLOG_EVENT.md 全項目消化済。
