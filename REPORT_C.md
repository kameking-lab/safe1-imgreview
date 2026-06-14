# REPORT_C — 事故イラスト収集(A) ＋ 事故情報Excel化(B) 成果報告

作成日: 2026-06-14 (JST)

## 1. 公開URL（Vercel `hakuten-review`／既存URL保持・noindex・スマホ縦・外部読込なし）

| 種別 | URL |
|---|---|
| レビューページ | https://hakuten-review.vercel.app/ics4e3york6xmz5t2hw0j7b1ugnlpq98/ |
| イラスト一覧PDF | https://hakuten-review.vercel.app/ics4e3york6xmz5t2hw0j7b1ugnlpq98/img_catalog.pdf |
| 事故情報Excel(TGL) | https://hakuten-review.vercel.app/ics4e3york6xmz5t2hw0j7b1ugnlpq98/accidents_TGL.xlsx |
| 事故情報Excel(高所) | https://hakuten-review.vercel.app/ics4e3york6xmz5t2hw0j7b1ugnlpq98/accidents_AERIAL.xlsx |

ルート `/` = 404、各成果物 = HTTP 200 を検証済（2026-06-14 20:11 JST／PDF 2,182,727 B・TGL 328,502 B・AERIAL 230,064 B）。

## 2. GitHub raw直URL（`kameking-lab/safe1-imgreview` @ master）

| 種別 | raw URL |
|---|---|
| イラスト一覧PDF | https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/review_collect/ics4e3york6xmz5t2hw0j7b1ugnlpq98/img_catalog.pdf |
| 事故情報Excel(TGL) | https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/review_collect/ics4e3york6xmz5t2hw0j7b1ugnlpq98/accidents_TGL.xlsx |
| 事故情報Excel(高所) | https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/review_collect/ics4e3york6xmz5t2hw0j7b1ugnlpq98/accidents_AERIAL.xlsx |
| index.html | https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/review_collect/ics4e3york6xmz5t2hw0j7b1ugnlpq98/index.html |

リポジトリ内の作業データ（連番イラスト・index）:
- `collect2/img/0001.jpg …`（連番4桁・通し番号）
- `collect2/img_index.csv`（通し番号,ファイル名,カテゴリ,事故種類,出所URL,md5,説明）
- `data_xlsx/accidents_TGL.xlsx` / `data_xlsx/accidents_AERIAL.xlsx`

## 3. イラスト総数（被りなし・通し番号）

- **総数: 73点**
  - TGL（テールゲートリフター/パワーゲート等）: **39点**
  - 高所（高所作業車/ブーム/作業床等）: **34点**
- 重複排除: md5 による重複排除済（`collect2/A6_dedup_report.md` 参照）

## 4. 事故情報 件数（被りなし・出典URL付）

| 群 | 件数 | データ源内訳 |
|---|---|---|
| TGL | **1,878件** | JNIOSH 1,386 / あんぜんサイト 492 |
| 高所(AERIAL) | **1,149件** | JNIOSH 916 / あんぜんサイト 233 |
| 合計 | **3,027件** | — |

各群とも目標1000件を達成（TGLは目標比約1.9倍、高所は約1.1倍）。
重複排除キー: (発生年月日+業種+事故の型+災害発生状況) のハッシュ。出典は全件付与。

## 5. カテゴリ別件数（事故の型）

### TGL群（計1,878件）

| 事故の型 | 件数 |
|---|---|
| はさまれ、巻き込まれ | 581 |
| 墜落、転落 | 457 |
| 激突され | 165 |
| 飛来、落下 | 158 |
| 転倒 | 145 |
| 崩壊、倒壊 | 142 |
| 動作の反動、無理な動作 | 121 |
| 激突 | 88 |
| 交通事故（道路） | 9 |
| 切れ、こすれ | 9 |
| その他 | 2 |
| 高温・低温の物との接触 | 1 |

### 高所群（計1,149件）

| 事故の型 | 件数 |
|---|---|
| 墜落、転落 | 392 |
| はさまれ、巻き込まれ | 281 |
| 転倒 | 84 |
| 交通事故（道路） | 78 |
| 激突され | 69 |
| 飛来、落下 | 56 |
| 激突 | 54 |
| 切れ、こすれ | 33 |
| 感電 | 30 |
| 動作の反動、無理な動作 | 30 |
| 崩壊、倒壊 | 16 |
| 高温・低温の物との接触 | 15 |
| 火災 | 6 |
| その他 | 4 |
| 有害物等との接触 | 1 |

## 6. データ出典

- JNIOSH 労働災害データベース（死亡災害DB H3-H30 / 死傷災害DB H18-H29）整形CSV
- あんぜんサイト 死亡災害DB / 死傷災害DB（起因物・事故の型で絞り込み）
- イラスト: 陸災防/建災防/中災防/林災防・各労働局・KYT教材・災害事例イラスト集・メーカー取説の警告図・安全ポスター等（出所URLは `collect2/img_index.csv` に全件記録）
