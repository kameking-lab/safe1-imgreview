# migration_report.md — ローカルWindows開発環境 → クラウド Claude Code 移行 現状調査

調査日時: 2026-06-23 06:30 (JST, powershell.exe Get-Date)
対象: C:\Users\kanet\20260522\safe1
方針: 今回は調査のみ。新規生成・デプロイ・ランナー起動はしていない。既存ファイルの削除/上書きなし。APIキー等の値は一切出力せず、キー名と桁数のみ記載。

================================================================
1. リポジトリ構成
================================================================

親リポジトリ
- リモート origin: https://github.com/kameking-lab/safe1-imgreview.git (fetch/push 同一)
- ブランチ: master(現在), main の2本。リモートに origin/main, origin/master。
- 現HEAD: d8f686e36b3c0bac0b824b816c4ae8c0ddebcc92 (master)
- 運用パターン: 作業は master にコミット→push→master:main を fast-forward（各 run_*.ps1 のワーカー指示に明記）。

サブモジュール(要注意)
- git submodule status はエラー終了。理由: パス "imgreview" が gitlink(モード160000, コミット 8c7fcbcc09e21e7aab6f0ea91d06c3d3fdead1c7)としてインデックスに登録されているが、.gitmodules が存在せず「マッピング無しの埋め込みリポジトリ」状態。
- imgreview/.git は実在し、リモートは親と同一の safe1-imgreview.git、ブランチ main、HEAD 8c7fcbcc。つまり自己参照的に同じリモートを指す入れ子リポジトリ。
- 影響: クラウドで普通に clone すると imgreview の中身は空ディレクトリ(gitlink)になる。移行時に「正式サブモジュール化(.gitmodules追加)」か「gitlink解除して通常ディレクトリ化」かを決める必要あり。

kameking-lab 配下の他リポジトリ(gh repo list で確認できた範囲)
- safe-ai-site, note-automation, keiba-ev, instagram-automation, safe1-imgreview,
  clipdesk-app, clipdesk, denki-kakomon, ipa-quiz-site, tsunagaru-eng, bear-map,
  app-discovery, stock-alert-app, printapp_mobile, reizoko-chef, pakupakuvideo,
  kameking-lab.github.io, reizoko-chef-web, arumonde-god, sum-calculator,
  skills-introduction-to-github, "-"(テスト)。
- 本案件に関係深いのは safe1-imgreview(本体)と instagram-automation(Gemini画像生成の流用元、メモリ参照)。

================================================================
2. 依存環境(ランタイム/ツール)
================================================================

ランタイム
- node: v24.13.1
- git: 2.46.0.windows.1
- gh: 2.89.0
- Python(注意): PATH上の python は 32bit版 Python312-32
  (C:\Users\kanet\AppData\Local\Programs\Python\Python312-32\python.exe)。
  ここには pywin32==312, PyYAML==6.0.3 の2個しか入っていない。
- 実際の作業環境は 64bit版 Python 3.12
  (C:\Users\kanet\AppData\Local\Programs\Python\Python312\python.exe, py -3.12 が既定)。
  こちらに 194パッケージ。主要:
    rembg==2.0.76, pillow==12.2.0, python-pptx==1.0.2, matplotlib==3.9.2,
    numpy==2.4.6, onnxruntime==1.27.0, opencv-python==4.10.0.84,
    opencv-python-headless==4.13.0.92, openpyxl==3.1.5, pandas==2.3.3,
    lxml==6.1.0, requests==2.32.3, playwright==1.57.0, selenium==4.39.0,
    google-generativeai==0.8.5, openai-whisper==20250625。
- 移行論点: 「python」と「py -3.12」が別環境という二重化は事故の元。クラウドでは
  requirements.txt を固定し単一の venv に集約すべき。pip freeze をエクスポートして再現する。

Windows固有に依存している処理(Linuxでは要置換)
- (a) PowerShell 自走ランナー: run_until_done.ps1, run_ppt.ps1, run_prop.ps1,
  run_collect/illust/layer/layg/layv19/photo/refs/study/study2/v2.ps1 など計14本+補助。
  各々 while(-not Test-Path DONE*.flag){ claude -p --dangerously-skip-permissions ... ; Start-Sleep }
  の無限ループでBACKLOGを完走させる構造。
  Linux代替: bash スクリプト(.sh)＋ループ、または systemd サービス/タイマー、cron、
  あるいはクラウドClaude Code側のバックグラウンドタスク/スケジュール(routines)へ移す。
- (b) 文字コード: 各ランナー冒頭の chcp 65001 と $OutputEncoding=UTF8。
  Linux代替: 既定でUTF-8のため不要(ロケール LANG=C.UTF-8 を設定する程度)。
- (c) PowerPoint COM による pptx→PDF / pptx→PNG 変換:
    export_pdf.ps1 … New-Object -ComObject PowerPoint.Application; SaveAs(...,32=ppSaveAsPDF)
    render_pptx.ps1 … 各 Slide.Export(png,1600x900)
    pptx2pdf_com.py … win32com 経由の同等処理(pywin32 が32bit側に居る理由)
  Linux代替: LibreOffice headless。
    PDF:  soffice --headless --convert-to pdf --outdir <dir> file.pptx
    PNG:  PDFをpdftoppm/ImageMagickでラスタライズ、または各スライドPNGはLibreOffice+pdftoppm。
  注意: COMとLibreOfficeでフォント/レイアウトの微差が出るため、移行後にQA再点検が必要。
- (d) 日本語フォントのハードコード: build_candidates_pdf.py / build_compare_3way.py /
  build_compare_illust_v17.py / build_img_catalog_*.py 等で
  C:\Windows\Fonts\YuGothB.ttc, meiryob.ttc, YuGothR.ttc, meiryo.ttc を直接参照。
  Linux代替: Noto Sans CJK JP / IPAexゴシック等を導入し、フォントパスを
  環境変数か設定で差し替え(Windowsフォントパスのフォールバックを追加)。matplotlibの
  fontproperties もNotoへ。これを直さないとmatplotlib/Pillow描画が全滅する。
- (e) Start-Process / Set-Location $PSScriptRoot / Start-Sleep 等PS固有制御。
  Linux代替: bash の cd "$(dirname "$0")", sleep, & での起動。
- (f) Chrome操作(Gemuseブラウザ画像生成, instagram-automation流用): 「chromeをkillしない」
  運用がローカル前提。クラウドではheadless Chromium(playwright同梱)に置換し、
  既存ブラウザ共有という概念自体が不要になる。ただしGeminiブラウザ生成はログインセッション
  依存のため、クラウドでは API キー方式へ寄せるのが現実的。

外部ツールの在/不在(クラウド設計の前提)
- soffice(LibreOffice): ローカルに無し(COMで代替しているため)。クラウドでは新規導入が必要。
- vercel CLI: 有(npm, vercel.ps1)。
- claude CLI: 有(npm, claude.ps1)。
- wsl: 有(参考)。
- .mcp.json: リポジトリ内には無し(MCPはアカウント側設定)。

================================================================
3. シークレット類(値は出さない。名前と桁数のみ)
================================================================

.env (リポジトリ直下、.gitignore対象=gitに入っていない)
- OPENAI_API_KEY = [桁数 164]
- GEMINI_API_KEY = [桁数 53]
他のキーは .env に無し。

Vercel
- .vercel ディレクトリは .gitignore 対象(gitに入っていない)。
- 実体は各 review_* 配下に多数存在(review, review2..7, review_collect, review_illust,
  review_layer_v19, review_layg, review_photo, review_ppt, review_study2 など計28箇所)。
- review_layer_v19/.vercel/project.json の中身キーは projectId / orgId / projectName のみ。
  projectName = hakuten-review。トークン(auth.json等)はこのディレクトリには保存されていない。
- Vercelの認証トークンはグローバルのCLIログイン(~/.local や %USERPROFILE% 側)に保持されており、
  リポジトリには含まれない。

クラウド移行時に「再設定が必要」なシークレット(名前のみ)
- OPENAI_API_KEY (再発行 or 既存値を環境変数/シークレットストアへ投入)
- GEMINI_API_KEY (同上)
- Vercel デプロイ用トークン(VERCEL_TOKEN として新規発行推奨。CLIログインの代わり)
- GitHub 認証(gh のOAuth or PAT。push権限)

================================================================
4. 外部サービス連携(必要な認証「種類」のみ。値不要)
================================================================
- GitHub: clone/push。種類=OAuthトークン or PAT(repo権限)。
- Vercel: project hakuten-review への vercel deploy --prod。種類=Vercelアカウントトークン。
  全 review_*/<32文字トークン> ディレクトリをunionして再デプロイし全URL 200/ルート404を維持する運用。
- OpenAI API: 画像/テキスト生成。種類=APIキー(OPENAI_API_KEY)。
- Google Gemini API: google-generativeai経由。種類=APIキー(GEMINI_API_KEY)。
  併用しているブラウザ版Gemini生成はログインセッション依存(キー不要だがクラウド非推奨)。
- MCP接続(claude.ai アカウント側、リポジトリ非依存): Canva, Gmail, Google Calendar,
  Google Drive, FMP, Figma, Zapier, Vercel, Slack, Microsoft365 等が接続済み。
  これらはアカウントに紐づくため、クラウドClaude Codeで同一アカウントを使えば再認証は各サービスのOAuthで対応。

================================================================
5. データ資産(サイズと git管理状況、移送方針)
================================================================

トップ階層の概算サイズ(MB)
- .git 1931.8 / refs2 915.1 / data 480.3 / images 375.2 / imgreview 340.2 /
  review_layer_v19 313.5 / review_layg 299.4 / review_study2 285.0 / review_compare3 283.5 /
  review_illust_sample 110.8 / review_preview_v16 109.1 / review_ppt_sample 108.5 /
  refs 98.9 / review_photo_progress 93.4 / review_pick 93.2 / v14 91.4 / photos_v15 90.0 ほか多数。
- gitで追跡中(tracked)のファイルは計 8409。多い順: refs2 3762, refs 581, images 467,
  render 231, collect2 210, runner_logs 173, v14 159, data 107, photos_v15 107 等。

ユーザ指定の各資産の追跡状況(tracked=gitに入っている数, ディスク実在)
- photos_v16: tracked 61(実在)
- illust_v17: tracked 45(実在)
- layers_v18: tracked 27(実在)  ※生成途中の raw 等は未追跡で混在
- layers_v19: tracked 11(実在)
- figs: tracked 10(実在)
- data_xlsx: tracked 3(実在)
- collect2(img含む): tracked 210(実在)
- review_layer_v19: tracked 6 だがディスクは313MB → 大半がデプロイ成果物の未追跡ファイル
- review_prop / review_layg: tracked 3 → 同上(デプロイ成果物は主に未追跡)

.gitignore の内容
- .env
- .vercel
- data/jniosh/parsed/jniosh_all.jsonl (コメントに「254MBの派生正規化データ、GitHub100MB制限超、
  parse_jniosh_b1.py で再生成可」と明記)

未追跡(untracked)の総量
- 約 630.4MB / 335エントリ(QA用PNG、_p*_check.pptx、review_* 配下の配信物、
  layers_v18/worker のraw画像など)。git status 上の変更/未追跡は計153エントリ。

移送方針(選択肢)
- 一次データ(data_xlsx, photos_v15/16, illust_v17, layers_v18/19, figs, collect2,
  refs/refs2 の素材, data): すでにgit追跡なら clone でそのまま入る。ただし .git が1.9GBと
  肥大しており clone が重い。
- jniosh_all.jsonl(254MB, gitignore, 再生成可): クラウドでは git に入れず
  parse_jniosh_b1.py で再生成 が第一候補。
- review_* のデプロイ成果物(大半untracked, 各60〜300MB): Vercel上に既に公開済みのため
  ローカル成果物は移送不要。必要なら Vercel から取得 or 再生成。
- 巨大バイナリを今後もgit管理するなら git-lfs 化(画像/pptx/pdf)を検討。
  ただしGitHubは100MB/ファイル上限、LFSは別課金。
- 推奨の優先順位: (1)再生成可能物は再生成(jniosh派生, QA PNG, review配信物)、
  (2)一次素材のみ git-lfs もしくはクラウドストレージ(GCS/S3/Drive)へ、
  (3).git肥大は移行時に履歴を浅く(shallow clone / 新規リポジトリで素材リセット)して軽量化。

================================================================
6. ランナー設計のクラウド移植論点
================================================================
現状(ローカル自走): BACKLOG_*.md(タスク列)＋ RULES_*.md(規約)＋ run_*.ps1(外部PowerShell)。
PowerShellが claude -p --dangerously-skip-permissions を無限ループで起動し、
「BACKLOGの最上位未チェックタスクを1つだけ実行→[x]に更新→git push→DONE*.flagで終了」を回す。
レート制限検知時は reset時刻をログから正規表現で読み、その時刻まで Start-Sleep する自己回復付き。

クラウドClaude Codeへの対応(論点)
- 外部PSループに相当する「常駐ドライバ」をどう持つか:
  (a) クラウドのスケジュール実行(routines/cron的)で定期キック、
  (b) バックグラウンドタスク/ワークフローで自走、
  (c) CI(GitHub Actions)からヘッドレス起動。
- レート制限の自己回復(reset時刻待ち)は、クラウド側のリトライ/スケジューラ機能で代替。
  Start-Sleep ベースの待機はクラウドでは推奨されない(課金/タイムアウト)。
- --dangerously-skip-permissions 前提の無人実行 → クラウドでは権限モデル/許可リスト
  (settings.json の allow)で安全に無人化する設計へ。
- DONE*.flag / [x]更新 / git push の完走判定はそのまま流用可(ファイルフラグは移植容易)。
- BACKLOG_*.md / RULES_*.md のタスク・規約資産は環境非依存でそのまま移植可能(最大の資産)。
- 「同一トークンをunionして毎回Vercel再デプロイ」運用はトークン一覧の管理が肥大化。
  クラウドではデプロイ対象リスト管理を明示ファイル化しておくと安全。

================================================================
7. 移行の障壁・リスクと対処
================================================================
- 障壁A: PowerPoint COM依存(pptx→PDF/PNG)。Linuxに存在しない。
  対処: LibreOffice headless(soffice --convert-to pdf, pdftoppmでPNG)に置換し、
  移行後にスライドQAを再実施(フォント/レイアウト差を吸収)。
- 障壁B: 日本語フォントのWindows絶対パス直書き。
  対処: Noto Sans CJK JP/IPAexを導入、フォント解決をフォールバック方式に改修(コード修正必須)。
- 障壁C: Python環境の二重化(32bit pywin32側 と 64bit実作業側)。
  対処: requirements.txt固定の単一venvに集約。pywin32はLinuxで不要(COM廃止に伴い除去)。
- 障壁D: .git 1.9GB＋tracked巨大バイナリで clone が重い。
  対処: shallow clone、または素材を外部ストレージ/LFSへ出して履歴を軽量化。
- 障壁E: imgreview の壊れた gitlink(.gitmodules無し・自己参照)。
  対処: 正式サブモジュール化 or 通常ディレクトリ化を移行時に決定(非破壊で別途整理)。
- 障壁F: シークレット再設定(OPENAI/GEMINI/Vercel/GitHub)。
  対処: クラウドのシークレットストア/環境変数へ投入。ブラウザ版Gemini生成はAPIキー方式へ寄せる。
- 障壁G: Vercel union再デプロイ運用の複雑さ(全トークン200維持)。
  対処: デプロイ対象トークンの台帳ファイル化＋CIで検証(curl 200/ルート404)。
- 障壁H: 無人実行の権限(--dangerously-skip-permissions)。
  対処: 許可リスト(settings.json allow)で必要コマンドのみ許可し安全に無人化。
- 障壁I: コスト面。クラウドの常時稼働/大容量ストレージ/LFS課金/レート制限待ちの実行時間。
  対処: 再生成可能物はgit/ストレージに置かず都度生成、スケジュール実行で稼働時間を圧縮。

================================================================
推奨移行ステップ(番号付き)
================================================================
1. リポジトリ整理: imgreview の gitlink を正式サブモジュール化 or 通常化を決定(非破壊で別ブランチ検証)。
2. 依存固定: 64bit Python 3.12 の pip freeze を requirements.txt 化。pywin32 はCOM廃止後に除外。
3. Linuxツール導入: LibreOffice, poppler(pdftoppm), Noto/IPAexフォント, Node, gh, vercel CLI をDockerfile化。
4. Windows依存コード改修: (a)COM変換を soffice ラッパに、(b)フォント絶対パスをフォールバック化、
   (c)run_*.ps1 を bash 化 or クラウドのスケジュール/バックグラウンド機構へ移植。
5. シークレット投入: OPENAI_API_KEY / GEMINI_API_KEY / VERCEL_TOKEN / GitHub認証をクラウドのシークレットへ(値は安全経路で)。
6. データ移送: 一次素材のみ移送(LFS or 外部ストレージ)、jniosh派生・QA・review配信物は再生成/Vercel側で済ます。
   .git肥大は shallow/履歴軽量化。
7. 動作検証: 1タスク分(例: pptxビルド→soffice PDF→PNG QA)をクラウドで通し、フォント/レイアウトを目視確認。
8. 自走化: BACKLOG/RULES資産を流用し、許可リスト＋スケジュール実行で無人ループを再現。Vercelデプロイのunion検証を組込む。
9. 切替: 旧ローカルは非破壊で保持(リードオンリーのバックアップ)し、クラウドを主系へ。

================================================================
確認事項
================================================================
- 既存非破壊: 本調査では読み取り専用コマンドのみ実行。ファイルの削除/上書き/移動・Chrome killは行っていない。
  新規生成・デプロイ・ランナー起動も実施していない。本レポート migration_report.md の新規作成のみ。
- キー値非出力: APIキー等の値は一切出力していない。記載は名前と桁数(OPENAI_API_KEY=164, GEMINI_API_KEY=53)のみ。
