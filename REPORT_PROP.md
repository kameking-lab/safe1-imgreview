# REPORT_PROP — proposal_hakuten 提案資料 完成報告

- 作成日時：2026-06-21 14:04（JST）
- 資料：`proposal_hakuten.pptx`（python-pptx・py3.12）／`proposal_hakuten.pdf`（PowerPoint COM 変換）
- 方針：メラビアン重視（ビジュアル7割・文字最小・1スライド1メッセージ・安全色・日本語フォント・16:9）
- **スライド数：11枚**
- **QAラウンド数：4（QA1〜QA4・実際にPNGレンダして目視点検／qa_prop/）**

## 1. 公開URL（Vercel hakuten-review・限定公開／noindex）
- レビューページ：https://hakuten-review.vercel.app/6brfn5sp7mu9jcs4y9th39l9el752dwt/
- トークン：`6brfn5sp7mu9jcs4y9th39l9el752dwt`（32文字）

## 2. 成果物 直URL（実測HTTPステータス）

| 種別 | URL | HTTP |
|---|---|---|
| レビューページ | https://hakuten-review.vercel.app/6brfn5sp7mu9jcs4y9th39l9el752dwt/ | 200 |
| PDF（Vercel） | https://hakuten-review.vercel.app/6brfn5sp7mu9jcs4y9th39l9el752dwt/proposal_hakuten.pdf | 200 |
| PPTX（Vercel） | https://hakuten-review.vercel.app/6brfn5sp7mu9jcs4y9th39l9el752dwt/proposal_hakuten.pptx | 200 |
| ルート `/`（非公開確認） | https://hakuten-review.vercel.app/ | 404 |

### GitHub(main) 直URL（raw・実測200）
- PDF（root）：https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/proposal_hakuten.pdf
- PPTX（root）：https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/proposal_hakuten.pptx
- PDF（review_prop）：https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_prop/6brfn5sp7mu9jcs4y9th39l9el752dwt/proposal_hakuten.pdf
- PPTX（review_prop）：https://raw.githubusercontent.com/kameking-lab/safe1-imgreview/main/review_prop/6brfn5sp7mu9jcs4y9th39l9el752dwt/proposal_hakuten.pptx
- blob（PDF）：https://github.com/kameking-lab/safe1-imgreview/blob/main/proposal_hakuten.pdf
- blob（PPTX）：https://github.com/kameking-lab/safe1-imgreview/blob/main/proposal_hakuten.pptx

## 3. スライド構成（11枚）
1. 表紙（データに基づく安全管理＋AIによる自動化／株式会社 博展 御中／監修：金田 義太）
2. 課題提起（従来の安全教育は属人的・再現性がない）
3. 解決アプローチ（事故データ分析→危険を科学的に特定→教材化→AIで量産・矢印図）
4. データ分析①（約42万件規模＋TGL/高所 型別ランキング横棒）
5. データ分析②（死亡vs死傷の対比・致死率を大きな数字で）
6. 科学的対策（墜落/はさまれ/感電 等のアイコン＋短句・法令小さく）
7. 自動化の価値（AIで事例教材を量産・人手×日→AI×時間の対比・3アイコン）
8. 成果物サンプル（これまで作った事例集／学習資料の見た目・AI再現イメージ注記）
9・10. 指定フォーマット事故事例（博展テンプレ template_spec.md／photos_v16＋cases_v2本文／出典小さく・監修・AI再現イメージ注記）
11. まとめ＋提案（科学的安全×自動化・連絡先/監修者名・価値1行）

## 4. 使用データ（確定素材のみ・捏造なし）
- 走査規模：約42万件（死亡DB 1991-2018＋死傷DB 2006-2017）
- TGL（計1,878）：はさまれ581(30.9%)最多／死亡のみはさまれ52.9%
- 高所（計1,149）：墜落392(34.1%)最多／高所は致死率が高い
- 法令：TGL特別教育義務化＝令和6年(2024)2月1日施行（学科4h＋実技2h・罰則6月以下or50万円以下）／高所作業車＝作業床10m以上技能講習・フルハーネス6.75m超着用義務（安衛則第194条の22）
- 出典は参考として小さく添付。監修：金田 義太（労働安全コンサルタント 登録第4840号）

## 5. 残課題
- なし（QA4まで完了・問題ゼロ・明日そのまま提示可能）。

## 6. 付記
- **新規画像生成なし**：既存figs/・既存生成画像・既存図表のみ使用。画像生成API（OpenAI/Gemini）は未使用。
- **捏造なし**：RULES_PROP.md の確定素材以外の数値・法令・日付・出典は不使用。
- **非破壊**：既存ファイルの削除・上書きなし。追加は新ファイル名のみ。APIキー値は非出力。
- Vercel 再デプロイは過去全レビュートークンをunionで束ね、既存URLは全200保持・ルート/=404 を実測。
