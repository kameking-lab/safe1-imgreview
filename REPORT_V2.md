# REPORT_V2 — 博展向け 想定事故事例集＋動画プロンプト集（最終報告）

イベント設営現場 想定事故事例集（全15事例）｜株式会社 博展 御中
監修：金田 義太（労働安全コンサルタント 登録第4840号）／作成日：2026-06-15

---

## 1. 公開URL（限定共有・noindex・外部読込なし・スマホ縦対応）

- レビューページ（index.html）：
  https://hakuten-review.vercel.app/fd9oal4jsc4u7wkfuoebpb0l1kdkfbp9
  - 検証：HTTP 200・text/html・8,146 B
  - ルート `/` は 404（限定共有のためトップ非公開）を実測確認

### 各成果物の直URL（Vercel・200実測）

| 成果物 | 直URL | HTTP | 種別 | サイズ |
|---|---|---|---|---|
| 事例集PDF | https://hakuten-review.vercel.app/fd9oal4jsc4u7wkfuoebpb0l1kdkfbp9/hakuten_jirei_v2.pdf | 200 | application/pdf | 5,830,089 B |
| 動画プロンプト集PDF | https://hakuten-review.vercel.app/fd9oal4jsc4u7wkfuoebpb0l1kdkfbp9/video_prompts_v16.pdf | 200 | application/pdf | 11,698,086 B |
| 事例集PowerPoint | https://hakuten-review.vercel.app/fd9oal4jsc4u7wkfuoebpb0l1kdkfbp9/hakuten_jirei_v2.pptx | 200 | pptx | 52,181,361 B |

### GitHub raw 直URL（main・200実測）

- 事例集PDF：
  https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_v2/fd9oal4jsc4u7wkfuoebpb0l1kdkfbp9/hakuten_jirei_v2.pdf
- 動画プロンプト集PDF：
  https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_v2/fd9oal4jsc4u7wkfuoebpb0l1kdkfbp9/video_prompts_v16.pdf
- 事例集pptx：
  https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_v2/fd9oal4jsc4u7wkfuoebpb0l1kdkfbp9/hakuten_jirei_v2.pptx

（リポジトリ：github.com/kameking-lab/safe1-imgreview／ブランチ main）

---

## 2. 生成枚数

- 画像：15事例 × 3案（base／OpenAI／Google）＝ **45枚**
  - base（採用画像のコピー）15枚
  - OpenAI（gpt-image-2, quality=high）15枚
  - Google（gemini-3-pro-image-preview）15枚
  - ＝ AI新規生成 **30枚** ＋ ベースコピー 15枚
- 保存先：`photos_v16/{N01..N15}/{base,openai,google}.png`＋`gen_meta.json`、索引 `img_index_v16.csv`
- スライド：表紙1＋15事例×2（写真スライド＋項目スライド）＝ **31スライド**

---

## 3. 収録15事例（創作タイトル・通し番号 N01〜N15 連番／没番号#0041・#0060は番号詰め済）

| 新No | 旧番号 | 区分 | 創作タイトル | 元採用案 |
|---|---|---|---|---|
| N01 | 0001 | TGL | 展示パネル積み下ろし中、昇降板からの墜落 | A_openai |
| N02 | 0002 | TGL | 什器の積み下ろし中、昇降板と車体の間に足を挟まれ | A_openai |
| N03 | 0003 | TGL | パワーゲートでの荷役中、昇降板から転落しかけ | D_google_event |
| N04 | 0017 | TGL | 台車を昇降装置へ移す際、台車が落下し下敷きに | D_google_event |
| N05 | 0019 | TGL | 荷下ろし中、カゴ台車が倒れ作業員が転倒 | C_openai_event |
| N06 | 0040 | 高所 | 会場天井付近の作業中、作業床手すりと上方構造物の間に挟まれ | C_openai_event |
| N07 | 0042 | 高所 | 梁下を移動中、上方の梁と操作盤の間に挟まれ | D_google_event |
| N08 | 0043 | 高所 | 養生ネットを外そうとしてバスケットから墜落 | D_google_event |
| N09 | 0044 | 高所 | 看板取付で身を乗り出し、作業床から墜落 | D_google_event |
| N10 | 0046 | 高所 | 作業床上昇中、操作盤フレームと天井の間に胸部を挟まれ | D_google_event |
| N11 | 0050 | 高所 | バスケットから移ろうとして墜落 | D_google_event |
| N12 | 0052 | 高所 | 傾斜地で旋回中、機体がバランスを崩し転倒 | D_google_event |
| N13 | 0054 | 高所 | 手すりに足をかけたダクト取付中に墜落 | D_google_event |
| N14 | 0057 | 高所 | 外周作業で作業床から身を出し、高所から墜落 | C_openai_event |
| N15 | 0071 | 高所 | 低い梁下を移動中、下がり壁と手すりの間に挟まれ | C_openai_event |

- 区分内訳：TGL（テールゲートリフター／昇降板）5事例、高所（高所作業車・MEWP等）10事例

---

## 4. 動画プロンプト件数

- ファイル：`video_prompts_v16.md` ／ `video_prompts_v16.pdf`（事例集とは別冊）
- 総数：**180プロンプト** ＝ 15事例 × 3フェーズ（前→事故の瞬間→後）× 2モデル（OpenAI Sora 2／Google Veo 3.1）× 日英2言語
  - Sora 2：90（45 JP＋45 EN）／Veo 3.1：90（45 JP＋45 EN）
- 仕様：image-to-video前提（base/OpenAI/Google を開始フレームに）・約8秒・日本の会場・PPE着用・実在ロゴ無し・流血/残虐表現なし・「安全教育用の再現」文脈を各プロンプトに明記

---

## 5. 体裁・コンプライアンス（客先向け）

- AIモデル名ラベルは写真スライドに非表示。
- AI生成・創作（フィクション）である旨は表紙に1行のみ（各スライドで繰り返さない）。
- 出典は一次主張ではなく「参考資料」として控えめに記載（職場のあんぜんサイト／建設荷役車両安全技術協会）。
- 全スライドに監修：金田 義太（登録第4840号）。

---

## 6. QA結果

- PowerPoint COM で pptx→PDF/PNG 変換し目視（LibreOffice不在環境）。
- QA1〜QA4（最大4ラウンド）すべて実施。観点①〜⑩すべて適合・検出ブロッキング問題 **0件**（3ラウンド連続ゼロ達成、記録 `QA_V2_r1〜r4.md`）。

---

## 7. 残課題

- ブロッキングの残課題なし。
- 軽微（任意対応）：`photos_v16/N03/_tmp_oai_head.png` は生成途中の一時ファイル（成果物・索引には不使用、非破壊方針のため未削除）。
- 動画は本資料がプロンプト集であり、実映像の生成（Sora 2／Veo 3.1への投入）は受領側での実行を想定。

---

（本報告は安全方針に従い作成：既存ファイル非破壊・新ファイル名のみ・APIキー値は非出力。）
