# (A)イラスト収集
- [x] A1 収集計画 collect_plan.md 作成
- [x] A2 TGL事故イラスト収集 バッチ1（重複排除・連番保存・index更新）
- [x] A3 TGL事故イラスト収集 バッチ2
- [x] A4 高所事故イラスト収集 バッチ1
- [x] A5 高所事故イラスト収集 バッチ2
- [x] A6 全体重複再排除・通し番号確定・img_index.csv確定（計50〜100）
# (B)事故情報1000件×2
- [x] B1 JNIOSH CSV群DL・パース（data/jniosh/・既存流用）
- [x] B2 TGL抽出・重複排除・カテゴリ付与（目標1000）
- [ ] B3 高所抽出・重複排除・カテゴリ付与（目標1000）
- [ ] B4 あんぜんサイトDB等で出典URL補完・件数積み増し
- [ ] B5 Excel生成（TGL/AERIAL＋集計）
# まとめ・発行
- [ ] C1 img_catalog.pdf 作成（全イラストを通し番号付き一覧＝後から選べる）
- [ ] C2 review_collect/<ランダム32文字>/ に PDF＋index.html(静的/noindex/スマホ縦)＋Excel配置・Vercel hakuten-review再デプロイ(既存URL保持・ルート/=404・HTTP200)・GitHub(main)へ push
- [ ] C3 REPORT_C.md 作成・push（公開URL/PDF/Excel直URL＋raw・イラスト総数・事故件数(TGL/高所)・カテゴリ別件数）
