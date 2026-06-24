# BACKLOG_AERIAL2 — 高所作業車 事故・危険イメージ画像 収集（未完最上段を1つずつ）

- [ ] A1 収集元・検索クエリ案を洗い出しリスト作成（collect_aerial2/sources2.md）。収集方式の雛形(search_ra1.mjs)確認・anzenプロファイル疎通確認。
- [ ] A2 墜落・転落 の画像(実事例図/教育イラスト/写真/ポスター)を収集→aerial2_index.csv記録。
- [ ] A3 挟まれ・巻き込まれ の画像を収集→index記録。
- [ ] A4 転倒・横転 の画像を収集→index記録。
- [ ] A5 感電・飛来落下・不安全行動・その他 の画像を収集→index記録。
- [ ] A6 全体の重複排除(md5)・通し番号確定・index整備・出尽くし判定。
- [ ] BUILD aerial2_catalog.pdf 生成（通し番号付き一覧・1ページ6枚）。
- [ ] DEPLOY review_aerial2/<ランダム32文字>/ にPDF＋index.html(静的/noindex/スマホ縦/開く・保存＋iframe)を配置・Vercel hakuten-review再デプロイ(過去全トークンunionで既存URL全200保持・ルート/=404・HTTP200)・GitHub(master/main)へpush。
- [ ] REPORT REPORT_AERIAL2.md作成push(公開URL/PDF直URL＋raw・収集枚数(型別/種別)・出所ドメイン別内訳・出尽くし判定・残課題)。
