# REPORT_STUDY — テールゲートリフター／高所作業車 安全 学習資料（理論武装メモ）

> 打合せ前の「理論武装 学習資料」PDF（全9章・A4縦・日本語）の作成・公開完了報告。
> 作成日：2026-06-16（`powershell.exe -Command "Get-Date"` 基準）。非破壊・新ファイルのみ・捏造なし。APIキー/認証値は本書に一切記載しない。

---

## 1. 公開URL（HTTP200検証済・2026-06-16）

| 種別 | URL | HTTP |
|---|---|---:|
| レビューページ（スマホ縦・noindex・外部読込なし） | https://hakuten-review.vercel.app/ulwvjah0yo97ic3jnirgf6tleducsox2/ | 200 |
| PDF直URL（Vercel） | https://hakuten-review.vercel.app/ulwvjah0yo97ic3jnirgf6tleducsox2/study_tgl_aerial.pdf | 200 |
| PDF raw（GitHub main） | https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/study_tgl_aerial.pdf | 200 |
| ルート `/`（公開しない＝404確認） | https://hakuten-review.vercel.app/ | 404 |

- ランダム32文字フォルダ：`ulwvjah0yo97ic3jnirgf6tleducsox2`
- 既存の公開URL（過去デプロイ分）は保持。今回はサブパス追加のみで上書きなし。

---

## 2. 成果物・章立てと総ページ数

- ファイル：`study_tgl_aerial.pdf`（py＋PILで生成・**新規ファイル名・既存PDF非上書き**）
- 体裁：A4縦・日本語・全**40ページ**・各章末に出典URL・スマホでも読める版面
- 章の素材：`study/*.md`（stats / tgl / tgl_law / aerial / aerial_law / cross / qa / summary）を先に執筆し BUILD で統合

| 章 | 内容 | 素材 |
|---|---|---|
| 第1章 | エグゼクティブ要点（最多の型・最初に言う危険3つ・法令要点） | summary.md |
| 第2章 | 事故データ集計（事故の型別 件数ランキング：TGL／高所） | stats.md |
| 第3章 | TGL編 危険ポイント・機序・実事故事例（検証URL付） | tgl.md |
| 第4章 | TGL編 法令・規則（特別教育義務化ほか） | tgl_law.md |
| 第5章 | 高所作業車編 危険ポイント・機序・実事故事例（検証URL付） | aerial.md |
| 第6章 | 高所作業車編 法令・規則（運転資格／フルハーネス／離隔距離） | aerial_law.md |
| 第7章 | 横断管理＋イベント設営現場の留意 | cross.md |
| 第8章 | 想定問答10問＋模範回答（根拠付き） | qa.md |
| 第9章 | 用語集＋引用URL一覧 | summary.md |

---

## 3. 事故の型別 件数トップ3（手元一次データの実数）

データ源：`data_xlsx/accidents_TGL.xlsx`（n=1,878）・`accidents_AERIAL.xlsx`（n=1,149）・`data_xlsx/b5_summary.json`。
走査規模：厚労省 死亡災害DB（1991–2018）＋死傷DB（2006–2017）の**約42万件**走査。TGL内訳＝JNIOSH 1,386＋あんぜん 492／高所内訳＝JNIOSH 916＋あんぜん 233。

| 区分 | 1位 | 2位 | 3位 |
|---|---|---|---|
| **TGL（n=1,878）** | はさまれ・巻き込まれ **581**（30.9%） | 墜落・転落 **457**（24.3%） | 激突され **165**（8.8%） |
| **高所作業車（n=1,149）** | 墜落・転落 **392**（34.1%） | はさまれ・巻き込まれ **281**（24.5%） | 転倒 **84**（7.3%） |

- TGLは上位3型で全体の約64%（1,203/1,878）。高所は上位3型で約66%（757/1,149）。
- 感電30件は高所作業車に特徴的（TGLには感電カテゴリ自体が出ない）。
- TGLは**貨物自動車のテールゲートリフターに限定**（塵芥車・トラッククレーン・フォークリフト等は混入させていない）。高所は**起因物＝小分類コード146のみ**。

---

## 4. 引用した主要法令・規則と出典URL（施行日付き・全件HTTP200＋本文一致を確認）

| 項目 | 要点（施行日・条文） | 出典URL |
|---|---|---|
| TGL操作の特別教育 義務化 | **令和6年（2024）2月1日施行**・学科4h＋実技2h（安衛則第36条第5号の2／根拠 基発0328第5号）。昇降設備・保護帽の対象拡大は令和5年（2023）10月1日（第151条の67・第151条の74） | 基発0328第5号（JAISH）：https://www.jaish.gr.jp/anzen/hor/hombun/hor1-64/hor1-64-12-1-0.htm ／ 富山労働局：https://jsite.mhlw.go.jp/toyama-roudoukyoku/annsenntorakkuhoukaisei.html |
| 高所作業車の運転資格 | 作業床高さ**10m以上＝技能講習**（安衛令第20条第15号・就業制限）／**10m未満（2m以上）＝特別教育**（第36条第10号の5） | 安衛則第36条（JAISH）：https://www.jaish.gr.jp/anzen/hor/hombun/hor1-2/hor1-2-1-1h4-0.htm ／ 安衛令 t_doc：https://www.mhlw.go.jp/web/t_doc?dataId=74002000&dataType=0&pageNo=1 |
| 作業計画・作業指揮者・転倒防止 | 作業計画（第194条の9）／作業指揮者（第194条の10）／転倒・転落防止（第194条の11）／作業床フルハーネス（第194条の22、垂直昇降式は例外） | 安衛則 建設機械等（JAISH）：https://www.jaish.gr.jp/anzen/hor/hombun/hor1-2/hor1-2-1-2h2-0.htm |
| フルハーネス型墜落制止用器具 | 「安全帯→墜落制止用器具」改正＝**平成31年（2019）2月1日施行**。実務目安5m超／理論上6.75m超で必須（基発0622第2号）。旧規格「安全帯」は2022年1月1日以降 販売・使用不可 | 厚労省報道発表：https://www.mhlw.go.jp/stf/houdou/0000212834.html ／ ガイドラインPDF：https://www.mhlw.go.jp/file/04-Houdouhappyou-11302000-Roudoukijunkyokuanzeneiseibu-Anzenka/0000212917.pdf ／ 新規格告示：https://www.mhlw.go.jp/stf/newpage_03290.html |
| 充電電路への接近限界（離隔距離） | 特別高圧2m／高圧1.2m／低圧1m（**基発第759号**・昭和50年12月17日）。**対象＝移動式クレーン等**で、高所作業車は機種差を明記のうえ実務目安として援用 | 基発759号（JAISH）：https://www.jaish.gr.jp/anzen/hor/hombun/hor1-28/hor1-28-94-1-0.htm |

実事故事例の取得元：JNIOSH 公表ページ（https://www.jniosh.johas.go.jp/publication/houkoku/houkoku_2022_01.html ）・あんぜんサイト ヒヤリハット（https://anzeninfo.mhlw.go.jp/hiyari/hiy_0448.html ）。個別事例の機序・教訓は `study/tgl.md`・`study/aerial.md` 参照。

---

## 5. 出典確認できず（要確認）として本資料が断定を避けた項目

- **「死亡につながりやすい型」の数値断定**：一次データに死亡/非死亡の区分列が無いため件数断定不可（一般傾向のみ記載）。
- **技能講習・特別教育の科目別時間数**（高所作業車側）の逐語確認は未実施。
- **リスクアセスメントの根拠条文**（安衛法第28条の2と解されるが逐語200確認は未実施）。
- **高所作業車を名指しした離隔距離専用の告示・通達**（基発759号は移動式クレーン等向けを援用）。
- **高所作業車の形式分類の網羅的呼称**（メーカー名称等）の出典確認は未実施。
- **e-Gov原文（elaws.e-gov.go.jp）の逐語確認**：JavaScript描画のため未実施（条文はJAISH収録本文・厚労省 t_doc で200確認）。

---

## 6. 確認チェック（QA／安全）

- [x] 公開URL・PDF直URL・raw(main) を **2026-06-16 に全件HTTP200確認**（ルート `/` は404確認）。
- [x] 出典URLは web_fetch/curl で **HTTP200＋本文一致**を確認したもののみ採用。施行日・条文番号は厚労省（mhlw.go.jp）・JAISH本文・mhlw t_doc で確認。
- [x] 件数は手元xlsxの**実数**（`stats.md`／`b5_summary.json` と一致）。推測値は記載していない。
- [x] TGLに塵芥車・トラッククレーン・フォークリフト等を混入させていない／高所は起因物コード146のみ。
- [x] 確認できない事項は「出典確認できず（要確認）」と明記し断定していない（第5節）。
- [x] **非破壊**：既存成果物/テンプレ/data_xlsx は不変更。追加は新ファイル名のみ（PDF・index.html・本書）。rm/Remove-Item/del/move/taskkill 不使用。Chrome kill なし。今回は**画像生成なし**。
- [x] APIキー/認証値は本書および公開物に一切出力していない。
- [x] PDF は GitHub main へ push 済（raw(main) 200 で確認）。

---

*Generated 2026-06-16. 限定共有用（noindex・外部読込なし）。*
