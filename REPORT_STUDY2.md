# REPORT_STUDY2 — TGL／高所作業車 安全学習資料（図表ビジュアル中心・流し読み版）完了報告

作成日: 2026-06-16 ／ 成果物: `study_tgl_aerial_v2.pdf`（A4縦・全10ページ・図表中心・スマホ可）
※既存 `study_tgl_aerial.pdf`（章立て詳細版）は非破壊（無改変）。本資料は別名 v2 の新規追加物。

---

## 1. 公開URL（限定共有・noindex・外部読込なし）

| 区分 | URL | HTTP |
|---|---|---:|
| レビューページ（スマホ縦・PDFを開く/保存＋iframe縦表示・要点表） | https://hakuten-review.vercel.app/xdctnn75pj22u4d3xgjafz8cjm0ghfh8/ | 200 |
| PDF直URL（Vercel） | https://hakuten-review.vercel.app/xdctnn75pj22u4d3xgjafz8cjm0ghfh8/study_tgl_aerial_v2.pdf | 200 |
| ルート `/`（非公開＝404確認） | https://hakuten-review.vercel.app/ | 404 |

GitHub（main）push 済み:

| 区分 | URL | HTTP |
|---|---|---:|
| GitHub blob | https://github.com/kameking-lab/safe1-imgreview/blob/main/study_tgl_aerial_v2.pdf | 200 |
| raw 直URL | https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/study_tgl_aerial_v2.pdf | 200 |

公開トークン: `xdctnn75pj22u4d3xgjafz8cjm0ghfh8`（32文字ランダム）。

## 2. 既存URL全200保持（過去全トークンをunion）

過去レビュートークン26件＋今回新規1件＝**計27件すべて 200 を維持**（curl 検証済）。ルート `/`＝404。
- 検証サンプル（200）: `xdctnn…`（新規）, `lkvzufp4mfvwnfmgafm9pi5kbqmtejwu`（compare illust v17）, `ulwvjah0yo97ic3jnirgf6tleducsox2`（study 旧版）。
- 27トークン一覧（全32文字）:
  07k1r4wci8xbmu4erdvmyzz3yae8zam0 / 2c0q4ndbj42s3504tmb1ibfj8t7ygpr8 / 2fr3q17tidvh5xiqvs6cq9xvc1wzeh1l /
  7dg7hxbw3zzc7nz8cjz5m2zumzumy763 / 832ow1ag55z0fo77dziwoam9hy8kg79x / a4w30ttj1ib6pprrd7osbfrej73h56up /
  bh9b4d7xwc1w63sgw0h0zmrodp1dn7w1 / bzu1etpcnw1kd2j44a1po8aqv0umthgj / fd9oal4jsc4u7wkfuoebpb0l1kdkfbp9 /
  g95cf2wvdv3w9hnlf7n7yghtwrn9k5nm / gwgleketkqxdh278c12ekhe1im48zjwo / hukr6oie65oe25ph2fd578o251lju1tj /
  ics4e3york6xmz5t2hw0j7b1ugnlpq98 / lkvzufp4mfvwnfmgafm9pi5kbqmtejwu / m2doi7wo4ipuxvks0ilns7hokv1nqgb9 /
  q1j67lqz0q2ehiwq7ac24gyd0wrvwxkc / qh1lcldnryp9s4v6vwhgq6lm0blc9e2c / qn0wbzpqdzztmrfjoqw24zz98yw2ezk8 /
  r7nqosbvlanyd6htlns3nh63ay6rkr5p / rxf5i518j4x3hi5idn8qjfoqt41n245y / supt0g6y8ye1nmwhrlyb1hparplg7k0d /
  ulwvjah0yo97ic3jnirgf6tleducsox2 / w9d46l33dcmuol4pe50vaafl6dj4165q / xdctnn75pj22u4d3xgjafz8cjm0ghfh8 /
  xfkvg4py783lmjersu9r0cynp3zgazcv / xnytu5rldabeu5n0o2szkr19kfkjeq7p / ylzjop755n18k8xq06sc5jjwpknaupwd

## 3. 死亡者数（SHIBO）／死傷者数（SHISYO）— 手元一次データ実カウント

一次ソース: `data/jniosh/parsed/tgl_enriched.jsonl`・`aerial_enriched.jsonl`（1行1事故）。
集計キー: `db`（SHIBO=死亡災害DB／SHISYO=死傷災害DB）。**db未設定＝内訳不明**は分離表記。**捏造なし・内訳不明0件**で死亡/死傷を完全分離できた。

| 区分 | 総レコード | 死亡(SHIBO) | 死傷(SHISYO) | 内訳不明 | 死亡率 |
|---|---:|---:|---:|---:|---:|
| TGL（テールゲートリフター関連） | 1,878 | **121** | **1,757** | 0 | 6.4% |
| 高所作業車（AERIAL） | 1,149 | **358** | **791** | 0 | 31.2% |

→ TGL・高所とも **死亡／死傷を完全に分離できた**（内訳不明 0 件）。

## 4. 事故の型トップ3（合計＝SHIBO+SHISYO）

| 区分 | 1位 | 2位 | 3位 |
|---|---|---|---|
| TGL | はさまれ・巻き込まれ 581（30.9%） | 墜落・転落 457（24.3%） | 激突され 165（8.8%） |
| 高所作業車 | 墜落・転落 392（34.1%） | はさまれ・巻き込まれ 281（24.5%） | 転倒 84（7.3%） |

死亡(SHIBO)のみのトップは TGL=はさまれ・巻き込まれ64（52.9%）／高所=墜落・転落112（31.3%）。詳細は `stats2.md` 参照。

## 5. 確定した条文号数

**TGL操作業務の特別教育＝安衛則 第36条 第5号の4（確定）**。
e-Gov法令検索「労働安全衛生規則」を一次根拠とし、JSレンダで自動取得不可のため独立した複数二次情報源がいずれも「第36条第5号の4」で一致 → 確定（証跡 `law_egov_study2.md`）。
- 施行: 令和6年（2024）2月1日／学科4h＋実技2h／罰則6月以下の懲役 or 50万円以下の罰金。
- 関連: 昇降設備・保護帽・離脱時措置の改正＝令和5年（2023）10月1日施行（通達 基発0328第5号）。
- 高所作業車: 10m以上＝技能講習／10m未満＝特別教育。墜落制止用器具＝安衛則第194条の22。フルハーネス6.75m超で着用義務（建設5m以上）、旧規格は2022年1月使用禁止完了。
- 法令・施行日・条文号数・罰則は確定素材を VERBATIM 使用（再リサーチによる改変なし）。

## 6. 図の一覧（matplotlib・日本語フォントYuGoth登録・文字化けなし・`figs/`）

| ファイル | 内容 |
|---|---|
| figs/fig_tgl_type_rank.png | TGL 事故の型別 件数ランキング（横棒） |
| figs/fig_aerial_type_rank.png | 高所作業車 事故の型別 件数ランキング（横棒） |
| figs/fig_death_vs_injury.png | 死亡(SHIBO) vs 死傷(SHISYO) 対比 |
| figs/fig_tgl_timeline.png | TGL法制化タイムライン（H25ガイドライン→R5省令→R5/10施行→R6/2 特別教育義務化） |
| figs/fig_qual_table.png | 資格・装備の早見表（高所10m以上=技能講習/未満=特別教育・フルハーネス6.75m超 等） |
| figs/fig_danger_points.png | 危険ポイント5（墜落/はさまれ/転倒/感電/逸走） |

PDF全10ページ構成: ①30秒サマリー ②TGL事故型ランキング ③TGL法制化タイムライン ④高所事故型 ⑤資格・装備早見表 ⑥死亡vs死傷 ⑦危険ポイント5 ⑧イベント設営留意 ⑨想定問答10問 ⑩出典一覧。

## 7. コンプライアンス確認

- **非破壊**: 既存 `study_tgl_aerial.pdf`・過去 review ディレクトリは無改変（コピーのみ・削除/移動なし）。出力は別名 v2。
- **捏造なし**: 件数は手元データの実カウントのみ。確認できない数値・条文は記載していない。マクロ統計（65%・8割等）は確定素材の出典付きで「推定」併記。
- rm/Remove-Item/del/move/taskkill 不使用・Chrome kill 無し・AI画像生成無し（matplotlibグラフのみ）・APIキー値非出力。
