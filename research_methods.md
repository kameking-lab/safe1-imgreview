# 事故の「因果が正しく伝わる図」を作る手法・サービス比較（一次情報調査）

調査日 2026-06-13 / 用途：テールゲートリフター・高所作業車の事故を「荷と人の向き・接触点・危険点（＝物理の因果）が正しく一目で伝わる」図にすること。**重要なのは因果を“制御”できること。写実っぽさは不要かつ有害になり得る。**
評価軸：①因果/向きの制御性 ②物理的正しさの再現性 ③商標・AI破綻リスク ④日本仕様/日本語 ⑤費用 ⑥量産・改訂しやすさ ⑦学習/構築コスト。
検証：各候補の公式URLを実際に開き **HTTP 200** と内容を確認。価格・商用可否・日本語は公式ページで裏取り。確認できない項目は「未確認」と明記（捏造なし）。

## 比較表（スマホは横スクロール）

| 手法/サービス | カテゴリ | ①因果制御 | ②物理再現 | ③破綻/商標リスク | ④日本語 | ⑤費用 | ⑥量産性 | ⑦構築コスト | 出典URL(200確認) |
|---|---|---|---|---|---|---|---|---|---|
| **SVG（コード/生成）** | C 作図 | **高(座標で100%)** | 高 | 無 | 可(UTF-8) | 無料・商用可 | 高 | 中 | https://www.w3.org/Graphics/SVG/ |
| **matplotlib** | C 作図 | **高(100%)** | 高 | 無 | 可(日本語フォント設定) | 無料・商用可 | **高(連鎖図量産最速)** | 中 | https://github.com/matplotlib/matplotlib/blob/main/LICENSE/LICENSE |
| **Pillow(PIL)** | C 作図 | 高(やや手間) | 高 | 無 | 可 | 無料・商用可(MIT-CMU) | 高 | 中 | https://pillow.readthedocs.io/en/stable/about.html |
| **Blender(3D)** | F 3D | **高(最も物理正確・剛体シミュ可)** | 高 | 無 | 可(UI日本語化) | 無料・作品は商用可(GPLはアプリのみ) | 中(重い) | **高** | https://www.blender.org/about/license/ ※本文403,内容は公式スニペットで確認 |
| **ControlNet(openpose+depth)＋ComfyUI** | B 構造制御 | **高(向きは固定/接触点は領域マスク併用)** | 中〜高 | 低〜中(制御で低減) | UI英語・日本語情報は非公式 | 無料(OSS)＋クラウド従量(RunPod RTX4090 $0.69/h 等) | 中 | 中 | https://github.com/lllyasviel/ControlNet ／ https://github.com/comfyanonymous/ComfyUI |
| 領域制御(Regional/Set Mask) | B | 中〜高(配置固定/姿勢は別) | 中 | 低〜中 | 未確認 | 無料 | 中 | 中 | https://docs.comfy.org/ |
| GLIGEN(box指定) | B | 中(位置固定/向き不可) | 中 | 低 | なし | 無料(MIT,依存モデル制約) | 中 | 中〜高 | https://github.com/gligen/GLIGEN |
| draw.io | C 作図 | 中(連鎖の矢印は得意/各コマ物理は弱) | 中 | 無 | 可 | 無料(Apache2.0) | 中 | 低 | https://www.drawio.com/ |
| Figma | C 作図 | 中〜高(手作業精密/数値量産弱) | 中 | 無 | 可 | 無料枠/有料$16月〜 | 中 | 中 | https://www.figma.com/pricing/ |
| PowerPoint | C 作図 | 中 | 中 | 無 | 可 | Web版無料/365 $99.99年 | 中 | 低 | https://www.microsoft.com/en-us/microsoft-365/powerpoint |
| Illustrator | C 作図 | 中〜高 | 中 | 無 | 可 | 有料サブスクのみ(月額**未確認**) | 中 | 中〜高 | https://www.adobe.com/products/illustrator/pricing-info.html |
| **GPT Image(OpenAI)** | A 生成 | **中〜低(公式が"レイアウト配置苦手"明記)** | 低 | 中(AI破綻) | 未確認 | API $0.006〜0.211/枚 | 高 | 低 | https://developers.openai.com/api/docs/guides/image-generation |
| **Imagen 4/Ultra(Google)** | A 生成 | 中〜低(配置"occasional variations"明記) | 低 | 中 | 未確認 | API $0.02〜0.06/枚 | 高 | 低 | https://ai.google.dev/gemini-api/docs/imagen |
| **FLUX.2(Black Forest Labs)** | A 生成 | 中(最大10枚参照併用で中上/出力商用可) | 低〜中 | 中 | 未確認 | API from $0.03〜0.07/枚 | 高 | 低〜中 | https://docs.bfl.ai/quick_start/pricing |
| Ideogram 4.0 | A 生成 | **低(画像内テキスト特化・本用途最不向き)** | 低 | 中 | 未確認 | 未確認 | 高 | 低 | https://docs.ideogram.ai/ |
| Seedream 4.5(ByteDance) | A 生成 | 中(多画像編集で対象識別/価格・規約**未確認**) | 低 | 中 | 未確認 | 未確認 | 高 | 低 | https://seed.bytedance.com/en/seedream4_5 |
| Adobe Stock(既製素材) | D 素材 | 中(部品取り/事故系の当たり最良だが標準ライセンスは大幅改変不可) | — | — | 可 | 無制限17,380円/月 等 | — | — | https://stock.adobe.com/jp/license-terms |
| イラストAC(既製素材) | D 素材 | 中(部品取り・改変自由/AI学習禁止/素材は車両どまり) | — | — | 可 | 無料〜プレミアム | — | — | https://www.ac-illust.com/main/terms.php |
| PIXTA(既製素材) | D 素材 | 中〜低(TGL素材2件のみ) | — | — | 可 | 定額 月1,980円相当〜 | — | — | https://pixta.jp/about-license |
| いらすとや | D 素材 | 低(事故系なし・20点まで無料) | — | — | 可 | 無料 | — | — | https://www.irasutoya.com/p/terms.html |
| photoAC(写真) | D 素材 | 低(背景止まり) | — | — | 可 | 無料〜 | — | — | https://www.photo-ac.com/ |
| ココナラ(外注) | E 外注 | **高(指示次第・要安全実績者選別)** | — | — | 可 | 1点 数千円〜数万円 | 低(都度) | — | https://coconala.com/services/1423956 |
| ランサーズ(外注) | E 外注 | 高(コンペ可/譲渡明示要) | — | — | 可 | 数千円〜20万円 | 低 | — | https://www.lancers.jp/faq/l1016/107 |
| クラウドワークス(外注) | E 外注 | 中〜高(公式ガイド3万円〜・譲渡デフォルトOFF) | — | — | 可 | 3万円〜(目安) | 低 | — | https://crowdworks.jp/pages/guides/employer/pricing |

注：D素材・E外注は「②物理再現/⑥量産性/⑦構築」が手法性質上当てはまらない欄を「—」とした。

## 各カテゴリの要点
- **A 高精度生成モデル**：GPT Image/Imagen 4 は公式自身が「レイアウト依存の正確な配置は苦手／配置に occasional variations」と限界を明記。テキスト指示だけで“荷と人の倒れる向き・接触点”を保証できない。FLUX.2（最大10枚参照）・Seedream 4.5（多画像編集）は参照画像/スケッチ併用の編集ワークフロー前提なら制御性が上がるが、純生成では不確実。Ideogram は画像内テキスト特化で本用途は最不向き。→ **v4〜v12が全滅した轍そのもの。低評価。**
- **B 構造制御（ControlNet系）**：棒人間ポーズ(openpose)＋深度(depth)で「人が右へ倒れる」「荷が右・接触点が手前」の向き・前後をほぼ確実に固定できる＝AI内で因果を制御する唯一現実的な道。ただし接触点のピクセル固定は領域マスク(ComfyUI内蔵 Set Mask)併用が前提。商用は重みライセンス注意（schnell/Z-Image-Turbo/xinsir union = Apacheで安全、FLUX.1[dev]は重み非商用だが**生成画像の商用利用は許諾**）。
- **C 作図/模式図（コード）**：SVG・matplotlib・Pillow は作者が座標で向き・接触・危険点を100%制御。無料・商用可・日本語可・再現性と量産が最強。多コマの因果連鎖図に最適。draw.io/Figma/PowerPoint は連鎖の矢印は作りやすいが各コマ内の物理精密制御は弱く「中」。
- **D 既製素材**：そのまま因果が正しい素材は期待薄。Adobe Stock が事故系の当たり最良、イラストAC が改変自由で部品取り向き。いずれも“部品”として配置し、向き・矢印は別途自作で足す前提。
- **E 人手外注**：指示が正確なら因果を最も正しく描ける可能性が高いが、1点数千円〜3万円〜・納期約10日・著作権譲渡は別料金、改訂のたび再発注コストが課題。安全教育/KYT実績者の選別が必須。
- **F 3D（Blender）**：最も物理的に正確（剛体シミュで倒れる向きを物理法則どおりに再現可）。無料・作品は商用可。ただし習得コスト高で単純模式図には過剰。表紙級の決定カット向き。

## CLIの推奨（最終判断は人間）
**1位：C コード作画（matplotlib もしくは SVG生成）。**
本資料の核心要件「因果・向き・危険点が正確に一目で」を最も確実・安価（無料）・再現可能に満たす。座標で100%制御でき、AI破綻・商標・向きの誤りが原理的に出ない。多コマの因果連鎖図（過積載→後傾→滑落→下敷き）も最速で量産・改訂できる。評価軸①②③⑤⑥で最高、⑦も中。前回のプロトタイプ(M1模式図)が最良だった結論を、一次情報が裏付けている。

**2位：B ControlNet（openpose棒人間＋depth＋領域マスク）on ComfyUI。**
「写実寄りの見栄え」も欲しい場合に、AIに“配置を固定して描かせる”唯一現実的な道。因果制御性は高いが、接触点ピクセル精度は領域マスク併用前提で、GPU/クラウドと構築コスト(中)・重みライセンス確認が要る。コード作図ほどの確実性・手軽さはない。

補助的に：D（Adobe Stock/イラストAC）を“部品取り”、F（Blender）を表紙級の物理正確カット、E（ココナラ/ランサーズ）を決定版イラストの外注、に使い分けるのが現実的。

## 結論：「物理の因果を最も確実に制御できるのはどれか」
**作者が向き・接触・危険点を完全に定義できる C コード作画（SVG/matplotlib）と F 3D（Blender）が最も確実**（曖昧さゼロ）。実用・コスト・量産まで含めると **C（コード作画）が最有力**。AIの内側で制御するなら **B（ControlNet pose+depth+領域マスク）** が唯一現実的だが、純生成モデル（A）に力学の正しさを委ねるのは構造上不可（公式自身が配置の限界を認めている）。

## 検証メモ（HTTP 200 と 未確認事項）
- 上表の各出典URLは担当リサーチで実アクセスし HTTP 200 と内容を確認（一部はbot遮断403のため公式ドメイン内検索/公式スニペットで代替確認＝該当箇所に明記）。
- **未確認（公式200本文を取得できず／捏造回避のため空欄化）**：OpenAIの商用条項・日本語（policyページが403）／各生成モデルの日本語UIの公式明示／Ideogram実価格・Seedream価格と商用規約（公式200取得不可）／Adobe Illustrator の正確な月額／Blender・matplotlib等一部公式ページの本文(403、ライセンス内容はGitHub LICENSEや公式スニペットで確認)／MakeHuman・Fab・Shutterstock・photoAC個別規約・件数。
- 価格は調査時点・為替・プラン改定で変動。採用前に各公式ページで最新を再確認のこと。
