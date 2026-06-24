# REPORT_AERIAL2 — 高所作業車 事故・危険イメージ画像 収集 最終レポート

作成日時: 2026-06-25 08:34 (+09:00, `Get-Date`)
対象成果物: `collect_aerial2/aerial2_index.csv`（924件）/ `aerial2_catalog.pdf`（全924点・155頁・36.7MB）

## ■公開URL
- 公開ページ（限定／noindex・スマホ縦）:
  `https://hakuten-review.vercel.app/c0516d27c5b75fe7cd0b6c5b58bf171c/`
- PDF直URL:
  `https://hakuten-review.vercel.app/c0516d27c5b75fe7cd0b6c5b58bf171c/aerial2_catalog.pdf`
- PDF raw（GitHub）:
  `https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/review_aerial2/c0516d27c5b75fe7cd0b6c5b58bf171c/aerial2_catalog.pdf`

実測検証（DEPLOYタスク 2026-06-25 JST, curl）:
- 新規ページ `/c0516…/` = **200**（text/html 4,944B）
- PDF直URL = **200**（application/pdf 36,731,537B・md5一致）
- ルート `/` = **404**（text/plain）
- 既存含む全31トークン = **200**（non-200=0）・root `img/` = 200

## ■収集枚数
**合計 924点**（索引924行 = `img/` 実体924件・過不足ゼロ・md5全924ユニーク・通し番号1〜924連番）。

### 事故の型別（カテゴリ）
| カテゴリ | 枚数 |
|---|---|
| 墜落・転落 | 236 |
| 挟まれ・巻き込まれ | 204 |
| 転倒・横転 | 179 |
| 不安全行動 | 94 |
| 感電 | 88 |
| 飛来・落下 | 86 |
| その他 | 37 |
| **合計** | **924** |

### 種別 内訳
| 種別 | 枚数 |
|---|---|
| 教育イラスト | 523 |
| 実事例図/写真 | 183 |
| 注意喚起ポスター | 121 |
| KYT教材 | 71 |
| ヒヤリハット挿絵 | 26 |
| **合計** | **924** |

## ■主な出所ドメイン別 内訳（上位）
| ドメイン | 枚数 | 区分 |
|---|---|---|
| www.dreamstime.com | 68 | ストック素材 |
| www.shutterstock.com | 55 | ストック素材 |
| pixta.jp | 51 | ストック素材 |
| www.ac-illust.com | 48 | フリーイラスト |
| www.istockphoto.com | 36 | ストック素材 |
| www.vecteezy.com | 31 | ストック素材 |
| www.rodo.co.jp | 22 | 安全衛生団体/出版 |
| cartoondealer.com | 18 | ストック素材 |
| www.youtube.com | 17 | 動画サムネ（教育/事例） |
| www.rent.co.jp | 17 | 機材レンタル（安全啓発） |
| www.slideshare.net | 16 | 資料共有 |
| www.alamy.com | 16 | ストック素材 |
| stock.adobe.com | 16 | ストック素材 |
| anzeninfo.mhlw.go.jp | 15 | 公的DB（厚労省 職場のあんぜんサイト） |
| www.conger.com | 14 | 海外メーカー（安全資料） |
| ec.midori-anzen.com | 14 | 安全用品EC |
| ranmeishi.com | 12 | 解説記事 |
| www.kensaibou.or.jp | 10 | 建災防（建設業労働災害防止協会） |
| www.freepik.com | 10 | フリーイラスト |
| www.sacl.or.jp | 8 | 安全衛生団体 |

※全924件の出所URL/ドメインは `collect_aerial2/aerial2_index.csv` に1件ずつ記録。公的DB（anzeninfo.mhlw.go.jp）・団体資料（kensaibou.or.jp / sacl.or.jp / jisha.or.jp）・解説記事・素材サイトを中心に収集（RULES準拠）。

## ■出尽くし判定
- 実行済みクエリ総数: **86**（`collect_aerial2/queries_done.txt`、再実行なし）。
  - A2 墜落・転落: 16クエリ
  - A3 挟まれ・巻き込まれ: 20クエリ
  - A4 転倒・横転: 20クエリ
  - A5 感電/飛来落下/不安全行動/その他: 30クエリ
- 判定: 各カテゴリとも計画クエリを全走査済み。RULESの「8クエリ連続で新規ゼロ→カテゴリ終了」に該当する連続ゼロ区間は発生せず（=早期打ち切りではなく全クエリ消化での走査完了）。Bing画像 a.iusc 由来の追加新規は逓減。
- 重複排除: md5でカテゴリ横断重複0件（A2〜A5各スクリプトが保存前にmd5照合・逐次排除）。

## ■残課題
- 追加収集余地: ストック素材サイト依存が高めのため、公的DB（anzeninfo事例詳細ページ）・建災防/中災防の教材PDF図版を WebFetch/page.goto で直接取得すれば、実事例図/写真の比率を高められる。
- pHash併用: 現状はmd5のみ（実体一致のみ統合）。pHash併用で「リサイズ/再圧縮で別md5の実質同一画像」をさらに統合できる（RULESで「可能なら併用」とされた任意項目）。
- ライセンス: ストック素材は透かし付きサムネが含まれ得るため、二次利用時は各出所URLでライセンス確認が必要（収集・選抜用途のカタログとして記録）。
- 全体は確定素材のみ・捏造なし・新規画像生成なし・APIキー値非出力。非破壊（追加は全て新ファイル名）。

---
本レポートで AERIAL2 全タスク（A1〜A6 / BUILD / DEPLOY / REPORT）完了。
