# BACKLOG_PROP — proposal_hakuten 作成タスク（上から1つずつ）

- [x] P1 既存figs/データ棚卸し＋不足グラフをmatplotlibで生成(日本語フォント・型別/死亡vs死傷/解決アプローチ矢印図/自動化対比図・新ファイル名 figs/prop_*.png・捏造数値なし)
- [x] P2 表紙＋課題提起＋解決アプローチ(矢印図)スライド作成(文字最小・安全色)
- [x] P3 データ分析①②スライド作成(大きな数字＋グラフ)
- [x] P4 科学的対策＋自動化の価値＋成果物サンプル スライド作成(アイコン/対比図)
- [x] P5 指定フォーマット事故事例1〜2枚(博展テンプレ template_spec.md・photos_v16＋cases_v2本文流用・監修・AI注記・出典小さく)
- [x] P6 まとめ＋提案スライド作成(連絡先/監修者名・価値1行)
- [x] BUILD proposal_hakuten.pptx を python-pptx で組み上げ→PowerPoint COM で proposal_hakuten.pdf へ変換
- [x] QA1 PNGレンダ目視(qa_prop/)→文字削減/見やすさ/歪み修正→新コミットpush
- [x] QA2 再点検→修正→push
- [ ] QA3 再点検→修正(問題ゼロならスキップ)→push
- [ ] QA4 最終点検→push
- [ ] DEPLOY review_prop/<ランダム32文字>/ にpptx＋PDF＋index.html(静的/noindex/スマホ縦/各DL＋iframe)・Vercel hakuten-review再デプロイ(過去全トークンunionで既存URL全200保持・ルート/=404・HTTP200実測)・GitHub(main)push
- [ ] REPORT REPORT_PROP.md作成push(公開URL/pptx・PDF直URL＋raw/スライド数/QAラウンド数/残課題・新規画像生成なし・捏造なし明記)
