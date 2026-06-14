# REPORT_PHOTO — 選定17元絵 × 4枚 写真生成 最終報告

生成日: 2026-06-15（JST）

## ■公開URL
- レビューページ（静的/noindex/スマホ縦/外部読込なし）:
  https://hakuten-review.vercel.app/xfkvg4py783lmjersu9r0cynp3zgazcv/
- PDF直URL（Vercel）:
  https://hakuten-review.vercel.app/xfkvg4py783lmjersu9r0cynp3zgazcv/photos_v15_catalog.pdf
- PDF（GitHub main・raw）:
  https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/photos_v15_catalog.pdf
- PDF（GitHub main・blob）:
  https://github.com/kameking-lab/safe1-imgreview/blob/main/photos_v15_catalog.pdf

検証（2026-06-15 JST 実測）:
- ルート `/` = 404（意図どおり非公開ルート）
- レビューページ = 200（text/html）
- PDF = 200（application/pdf, 1,298,339 B）
- GitHub raw PDF = 200（1,298,339 B）

## ■生成枚数（成功/失敗）
- 元絵: 17/17
- 画像: 68/68 成功（失敗 0）
  - 各元絵 4枚: A 実写化(OpenAI) / B 実写化(Google) / C イベント設営版(OpenAI) / D イベント設営版(Google)

## ■各元絵の使用モデル（OpenAI / Google）
全元絵共通:
- OpenAI（A・C）= `gpt-image-2`
- Google（B・D）= `gemini-3-pro-image-preview`（Nano Banana Pro）

| 番号 | カテゴリ | A/C OpenAI | B/D Google | 備考 |
|---|---|---|---|---|
| 0001 | TGL | gpt-image-2 | gemini-3-pro-image-preview | |
| 0002 | TGL | gpt-image-2 | gemini-3-pro-image-preview | |
| 0003 | TGL | gpt-image-2 | gemini-3-pro-image-preview | |
| 0017 | TGL | gpt-image-2 | gemini-3-pro-image-preview | |
| 0019 | TGL | gpt-image-2 | gemini-3-pro-image-preview | |
| 0040 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0041 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0042 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0043 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0044 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0046 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0050 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | D版を no-logo 強化で再生成（ISUZUロゴ風除去） |
| 0052 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0054 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0057 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |
| 0060 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | D版を no-logo 強化で再生成（ブース看板の実在ロゴ風除去） |
| 0071 | 高所 | gpt-image-2 | gemini-3-pro-image-preview | |

## ■失敗・未生成の一覧
- なし（17/17 元絵・68/68 枚すべて成功）。
- フォールバック発動なし（OpenAI=gpt-image-2 / Google=gemini-3-pro-image-preview をそのまま使用）。
- ロゴ補正のための再生成 2件（0050 D / 0060 D）。いずれも最終版はロゴ無しで確定。

## ■成果物の所在
- 画像: `photos_v15/{番号}/A_openai.png` `B_google.png` `C_openai_event.png` `D_google_event.png`（各フォルダに `source_ref.png`・`gen_meta.json`）
- カタログ: `photos_v15_catalog.pdf`（7ページ・元絵→A/B/C/D 並べ・番号/カテゴリ/モデル名/実写・イベント版/事故機序を明記）
- 公開: `review_photo/xfkvg4py783lmjersu9r0cynp3zgazcv/`（index.html + PDF）／ Vercel hakuten-review 本番
