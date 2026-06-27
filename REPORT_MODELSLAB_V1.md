# REPORT_MODELSLAB_V1 — ModelsLab API 高所作業車（シザースリフト）墜落 安全教育イラスト 方式別比較（最終報告）

作成日時: 2026-06-27 16:00（JST）

## ■成果サマリ
- ModelsLab API で「高所作業車（シザースリフト）からの人の墜落」安全教育イラストを **方式A/B/C1/C2 の4方式・計30枚** 生成（再起動前に生成・有効・push済。本作業では再生成なし）。
- 4方式の比較PDF `compare_modelslab_v1.pdf`（1,858,956B）をビルド済。方式B/C1/C2は **左=ベース（本物の災害イラスト）／自作下書き・右=生成画像** の対比、方式A=text2imgグリッド。
- 限定公開（noindex・スマホ縦・「開く/保存」＋iframe縦表示）を Vercel `hakuten-review` に **過去全トークンの union 再デプロイ** で追加。既存URLは全保持。
- 安全教材の従来手順を踏襲し、**Vercel デプロイは safe1 外のステージング複製から実行**（safe1 リポジトリ非破壊）。

## ■方式別枚数・使用モデルID
- 方式A（text2img・ベース無し）: **10枚**（A_01〜A_10）／モデルID **flat-2d-animerge**。
- 方式B（img2img・本物の災害イラストをベース）: **10枚**（B_01〜B_10）／モデルID **realtime-default(SDXL)**・prompt_strength=0.55。
- 方式C1（img2img・自作下書きベース・拘束ゆるめ）: **5枚**（C1_01〜C1_05）／モデルID **flat-2d-animerge**・prompt_strength=0.72。
- 方式C2（img2img・自作下書きベース・拘束つよめ）: **5枚**（C2_01〜C2_05）／モデルID **flat-2d-animerge**・prompt_strength=0.5。controlnet エンドポイントは本APIプランで利用不可（POST非対応）のため、低 strength で代替。
- 合計 **30枚**。記録CSV `gen_modelslab_v1/index.csv`（方式/連番/モデルID/手法/ベース下書き/prompt_strength/原因状況/プロンプト要約/ファイル名・30行）。

## ■公開URL / PDF直URL / GitHub raw（実測検証済み）
- 限定公開ページ（noindex・スマホ縦・「開く/保存」＋iframe縦表示）:
  https://hakuten-review.vercel.app/k4ibxx8xfm469no49p3jgw3v7kg57awf/
- PDF 直URL（1,858,956B）:
  https://hakuten-review.vercel.app/k4ibxx8xfm469no49p3jgw3v7kg57awf/compare_modelslab_v1.pdf
- GitHub raw（PDF実体を同梱）:
  https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/master/review_modelslab_v1/k4ibxx8xfm469no49p3jgw3v7kg57awf/compare_modelslab_v1.pdf
- 公開パストークン: `k4ibxx8xfm469no49p3jgw3v7kg57awf`（32文字・既存 `.deploy_token.txt` を再利用）。デプロイ実体は `review_layer_v19/<token>/`、GitHub同梱（raw用）は `review_modelslab_v1/<token>/`。

### curl 実測（2026-06-27）
- 新ページ `/<token>/` = **200**
- 新PDF `/<token>/compare_modelslab_v1.pdf` = **200**（size=1,858,956B、ローカルと一致）
- ルート `/` = **404**（意図通り。トークンを知る者のみ到達）
- GitHub raw PDF = **200**（size=1,858,956B 一致）
- 既存トークン: Vercel hakuten-review を過去全トークンの union（既存35実トークン＋stray img＋新1）で再デプロイ。**過去35実トークンページ=全200保持（non200=0）**。

## ■コスト概算
- ModelsLab API 呼び出し: 本生成 **30件**（OK 30）＋ smoke/モデル探索・i2i/controlnet テスト等 **約5〜8件** ＝ 合計 **約35〜38リクエスト**。
- 単価はプラン依存（ModelsLab の realtime / community 画像エンドポイントは概ね1枚あたり低単価）。概算で **総額 おおよそ $0.15〜$0.4 程度**（プラン・解像度により変動。正確な課金額は ModelsLab ダッシュボードの実績を参照）。エラー（クレジット上限/課金/認証/レート/HTMLスタブ）の記録は無し。

## ■画像の有効性・C1/C2 拡張子の注記
- 30枚すべて有効な画像バイト。A_01〜A_10・B_01〜B_10（20枚）は正規PNG。
- **C1_01〜C1_05・C2_01〜C2_05（10枚）は拡張子 `.png` だが中身は有効なJPEG（先頭 FFD8FF・JFIF）。** HTMLスタブ・破損・欠けは無し。ModelsLab が当該方式でJPEGを返したもので、画像としては正常。比較PDF（Pillow読込）も正常に取り込めており、表示・公開に支障なし。
- 拡張子と中身の不整合を厳密に揃える整合修正（.jpg へのリネーム＋リンク張替え）は **任意（必須でない）** ため本作業では未実施。PDF・公開ページとも現状で正しく機能する。

## ■デプロイ運用（厳守事項の遵守）
- Vercel `hakuten-review`（projectName=hakuten-review）への本番再デプロイは **safe1 外のステージング複製**（`C:\Users\kanet\20260522\_ml_deploy_staging`）に union を robocopy 複製し、そこから `vercel deploy --prod --yes` を実行 → `hakuten-review.vercel.app` へ alias。safe1 リポジトリ自体は非破壊。
- 非破壊（追加は新ファイル名／新トークンのみ・既存トークン非削除/非改変）。`rm`/`Remove-Item`/`del`/`move`/`taskkill` 不使用。Chrome kill 無し。
- APIキー・認証トークンは非出力／非コミット（`.env`・`.secrets/`・`.vercel`・`gen_modelslab_v1/.deploy_token.txt` は gitignore）。公開パストークンは限定共有URLの構成要素として記載。
- 新規画像生成なし（既存30枚を使用）。

## ■残課題
- 必須の残課題なし（コミット確定・限定公開・URL検証・本REPORT 完了）。
- 任意改善（必須でない）: ①C1/C2 の `.png`（中身JPEG）拡張子を `.jpg` に揃える整合修正、②方式横断で「最も忠実/高品質な代表1枚」を人が最終選定する選別工程、③controlnet 対応プランでの C 方式（構図拘束）の再検証。いずれも今回要件外のため未実施。
