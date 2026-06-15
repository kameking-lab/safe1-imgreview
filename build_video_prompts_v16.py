# -*- coding: utf-8 -*-
"""
build_video_prompts_v16.py — 動画プロンプト集 video_prompts_v16.(md/pdf) を生成（新規・非破壊）。

RULES_V2 ③:
- 15事例それぞれ：採用ベース画像＋リアル化画像（base/openai/google 3枚）を載せ、
  その下に〔前→事故の瞬間→後〕の3フェーズの動画プロンプトを
  OpenAI(Sora 2)用 と Google(Veo 3.1)用 の2種、日本語と英語併記で提示。
- image-to-video前提（この画像を開始/キーフレームに）。8秒前後・日本の会場・PPE・流血なし・危険の瞬間。
- 安全フィルタ回避の配慮（過度に残虐にしない・「安全教育用の再現」の文脈）を各プロンプトに含める。
- パワポとは別ファイル（.md と .pdf）として発行。

データは gen_v16.mjs の MAP（機序 mech / 設営文脈 event）と cases_v2 の創作タイトルに準拠。
PDF は PIL で各ページをラスタ描画して多ページPDF化（日本語フォント安全・既存 build_v13_pdf.py 流儀）。
キー値は一切扱わない。既存ファイルは上書きしない（新ファイル名のみ）。
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\kanet\20260522\safe1"
PHOTOS = os.path.join(BASE, "photos_v16")
OUT_MD = os.path.join(BASE, "video_prompts_v16.md")
OUT_PDF = os.path.join(BASE, "video_prompts_v16.pdf")

SUPERVISOR = "監修：金田 義太（労働安全コンサルタント 登録第4840号）"
TODAY = "2026年6月15日"

# 新No -> 創作タイトル / カテゴリ / 日本語シーン・瞬間 / 英語シーン(event)・瞬間(mech)
CASES = [
 dict(n="N01", cat="TGL", title="展示パネル積み下ろし中、昇降板からの墜落",
      scene_jp="展示会場の搬入口。トラックのテールゲートリフター（昇降板）で展示パネル・什器を積み下ろししている。",
      moment_jp="荷台から降りようとした作業員が、昇降板が荷台の高さまで上がり切っていない段差に気づかずバランスを崩し、地面側へ墜落する瞬間。",
      scene_en="unloading exhibition panels and display fixtures from a truck tail-gate lifter at an event hall loading bay",
      moment_en="a worker stepping off the truck bed misjudges the gap/step to the lift platform, loses balance and falls toward the ground"),
 dict(n="N02", cat="TGL", title="什器の積み下ろし中、昇降板と車体の間に足を挟まれ",
      scene_jp="会場搬入口。昇降板の上に立ち、什器の積み下ろしのため昇降板を操作している。",
      moment_jp="上昇する昇降板と車体（荷台フレーム）の間に、作業員の足が挟まれそうになる瞬間。",
      scene_en="loading exhibition fixtures with a truck tail-gate lifter at a venue loading dock",
      moment_en="a worker on the platform operates it and a foot gets pinched between the rising lift gate and the truck body"),
 dict(n="N03", cat="TGL", title="パワーゲートでの荷役中、昇降板から転落しかけ",
      scene_jp="展示会場でトラックのパワーゲート（昇降板）に乗り、荷役作業を行っている。",
      moment_jp="昇降板の開いた縁で作業員が体勢を崩し、外側へ転落しかける瞬間。",
      scene_en="handling event cargo on a truck power-gate (tail-gate lifter) at an exhibition hall",
      moment_en="the worker on the platform overbalances at the open edge and nearly falls off"),
 dict(n="N04", cat="TGL", title="台車を昇降装置へ移す際、台車が落下し下敷きに",
      scene_jp="荷台から積み荷を載せた展示用台車を、昇降板へ移そうとしている。",
      moment_jp="台車が昇降板から傾いて落下し、作業員が下敷きになりそうになる瞬間。",
      scene_en="transferring a loaded display cart from the truck bed onto a tail-gate lifter at a venue",
      moment_en="the loaded cart tips and drops off the platform and the worker is struck/pinned under it"),
 dict(n="N05", cat="TGL", title="荷下ろし中、カゴ台車が倒れ作業員が転倒",
      scene_jp="会場搬入口で、展示資材を積んだカゴ台車（ロールボックス）を荷下ろししている。",
      moment_jp="カゴ台車が別の台車と接触して倒れ、支えようとした作業員が押されて転倒する瞬間。",
      scene_en="unloading roll-cages of exhibition materials at an event loading bay",
      moment_en="a cargo roll-cage collides with another cart, topples, and the worker bracing it is knocked down"),
 dict(n="N06", cat="高所", title="会場天井付近の作業中、作業床手すりと上方構造物の間に挟まれ",
      scene_jp="展示会場の天井付近。高所作業車のバケット（作業床）に乗り、配線・吊り作業のためバケットを旋回・移動させている。",
      moment_jp="据付け地盤の凹凸で車体が揺れ、バケットの手すりと頭上の天井レール・梁の間に作業者の腰部が挟まれそうになる瞬間。",
      scene_en="overhead work at an exhibition hall (ceiling rail/truss) using an aerial work platform",
      moment_en="the worker in the basket is pinched at the waist between the basket top rail and an overhead structure as the basket moves on uneven ground"),
 dict(n="N07", cat="高所", title="梁下を移動中、上方の梁と操作盤の間に挟まれ",
      scene_jp="会場の天井梁の下で、高所作業車のバケットを移動させている。",
      moment_jp="上方の梁と作業床の操作盤の間に、作業者の身体が挟まれそうになる瞬間。",
      scene_en="moving an aerial work platform under a ceiling beam/truss at a venue",
      moment_en="the worker is pinched between the overhead beam and the platform control panel"),
 dict(n="N08", cat="高所", title="養生ネットを外そうとしてバスケットから墜落",
      scene_jp="トラス付近で引っ掛かった養生ネット・シートを外そうと、バスケットから手を伸ばしている。",
      moment_jp="バスケットの手すりに足をかけて手を伸ばした際、足を滑らせてバスケットから墜落する瞬間。",
      scene_en="removing a snagged rigging sheet/net near a truss from an aerial work platform at a venue",
      moment_en="reaching to a beam, the worker steps on the basket rail, the foot slips and the worker falls from the basket"),
 dict(n="N09", cat="高所", title="看板取付で身を乗り出し、作業床から墜落",
      scene_jp="会場の看板・サイン取付作業を、高所作業車の作業床から行っている。",
      moment_jp="手すりから大きく身を乗り出した作業者がバランスを崩し、作業床から墜落する瞬間。",
      scene_en="fixing venue signage while leaning out of an aerial work platform",
      moment_en="reaching out and leaning over the guardrail too far, the worker falls from the work floor"),
 dict(n="N10", cat="高所", title="作業床上昇中、操作盤フレームと天井の間に胸部を挟まれ",
      scene_jp="ホールの天井ダクト・照明の取付のため、高所作業車の作業床を上昇させている。",
      moment_jp="天井の段差に気づかず上昇し、操作盤フレームと天井の間に作業者の胸部が挟まれそうになる瞬間。",
      scene_en="installing ceiling ductwork/lighting from an aerial work platform at a hall",
      moment_en="raising the platform without noticing a ceiling step, the worker's chest is pinched between the control-panel frame and the ceiling"),
 dict(n="N11", cat="高所", title="バスケットから移ろうとして墜落",
      scene_jp="ブース・構造物付近で、高所作業車のバスケットから隣接する構造物へ移ろうとしている。",
      moment_jp="バスケットから移ろうとして足を踏み外し、数メートル下の地面へ墜落する瞬間。",
      scene_en="transferring from an aerial work platform basket near a booth/structure at a venue",
      moment_en="trying to transfer from the basket to an adjacent structure, the worker falls a few meters to the ground"),
 dict(n="N12", cat="高所", title="傾斜地で旋回中、機体がバランスを崩し転倒",
      scene_jp="屋外会場の傾斜地で、高所作業車のブームを旋回させている。",
      moment_jp="傾斜地で左へ旋回した際、機体がバランスを崩して転倒する瞬間。",
      scene_en="outdoor venue ground; an aerial work platform slewing on a slope",
      moment_en="on sloped ground, swinging the boom left, the machine loses balance and the whole platform tips over"),
 dict(n="N13", cat="高所", title="手すりに足をかけたダクト取付中に墜落",
      scene_jp="会場天井のダクト・機材の取付を、高所作業車のバスケットから行っている。",
      moment_jp="バスケットの手すりに足をかけた状態でバランスを崩し、作業床から墜落する瞬間。",
      scene_en="installing ceiling ducts/equipment from an aerial work platform at a venue",
      moment_en="with a foot on the basket guardrail during overhead duct fixing, the worker loses balance and falls from the platform"),
 dict(n="N14", cat="高所", title="外周作業で作業床から身を出し、高所から墜落",
      scene_jp="会場の外周・ファサードの作業を、高所作業車の作業床から行っている。",
      moment_jp="作業床が壁面に接触し、確認のため作業床から身を乗り出した作業者がバランスを崩し、高所から墜落する瞬間。",
      scene_en="facade/perimeter work at a venue using an aerial work platform",
      moment_en="the work floor contacts a facade and the worker climbs out to check, loses balance and falls from height"),
 dict(n="N15", cat="高所", title="低い梁下を移動中、下がり壁と手すりの間に挟まれ",
      scene_jp="会場の地下・搬入路の低い開口部を、高所作業車で通過しようとしている。",
      moment_jp="低い下がり壁・梁と作業床の手すりの間に、作業者の身体が挟まれそうになる瞬間。",
      scene_en="moving an aerial work platform under a low hanging beam in a venue basement/back area",
      moment_en="driving through a low opening, the worker is pinched between a hanging wall/low beam and the platform handrail"),
]

PHOTO_FILES = ["base.png", "openai.png", "google.png"]


def ppe_jp(cat):
    base = "あごひも付きヘルメット・ハイビズ（高視認性ベスト）・安全靴"
    return base + ("・フルハーネス型安全帯" if cat == "高所" else "")


def ppe_en(cat):
    base = "hard hat with chin strap, hi-vis vest, safety boots"
    return base + (", full-body safety harness" if cat == "高所" else "")


def machine_jp(cat):
    return "トラックのテールゲートリフター（昇降板／パワーゲート）" if cat == "TGL" \
        else "高所作業車（ブーム式／シザー式・作業床付き）"


def machine_en(cat):
    return "a truck tail-gate lifter / power-gate (rear lift platform)" if cat == "TGL" \
        else "a Japanese aerial work platform / MEWP (boom or scissor lift with a work basket)"


def phases(c):
    """各事例の3フェーズ（前/瞬間/後）の日英記述を返す。"""
    return [
        ("前（事故直前）", "Phase 1 — Before (lead-up)",
         f"{c['scene_jp']}作業員は通常どおり準備・作業を進めており、まだ異常は起きていない平穏な場面。",
         f"{c['scene_en']}; workers proceed with the build-up task normally — a calm moment, no incident yet."),
        ("事故の瞬間", "Phase 2 — The moment",
         f"{c['moment_jp']}危険の一瞬を捉える（流血・残虐表現なし）。",
         f"{c['moment_en']} — capture the dangerous instant (no blood, no gore)."),
        ("後（直後の対応）", "Phase 3 — After (response)",
         "直ちに作業を中断し、周囲の作業員が駆け寄って安全を確認する。大きな外傷描写はなく、再発防止を促す静かな余韻で終える。",
         "work stops immediately; nearby workers rush in and check on safety. No graphic injury; end on a quiet beat that stresses prevention."),
    ]


def sora_jp(c, ph_jp, desc_jp):
    return (f"【Sora 2／日本語】この画像を開始フレームとして動かす（image-to-video）。"
            f"ドキュメンタリー調・自然光・手持ちカメラのリアルな実写映像。場面：{ph_jp}。{desc_jp} "
            f"舞台は日本の展示会・イベント設営会場、登場人物は日本人作業員、{machine_jp(c['cat'])}を使用。"
            f"服装・保護具は{ppe_jp(c['cat'])}。実在ロゴや可読文字は映さない。"
            f"これは安全教育用の事故再現映像であり、流血・残虐・苦痛の誇張は描かない。約8秒・16:9。")


def sora_en(c, ph_en, desc_en):
    return (f"[Sora 2 / English] Use the provided image as the starting keyframe (image-to-video). "
            f"Photorealistic documentary footage, natural light, handheld camera. Scene: {ph_en}. {desc_en} "
            f"Set at a Japanese exhibition / event build-up venue with Japanese workers using {machine_en(c['cat'])}. "
            f"Workers wear {ppe_en(c['cat'])}. No real logos or readable text. "
            f"This is a safety-education re-enactment; no blood, gore or exaggerated suffering. About 8 seconds, 16:9.")


def veo_jp(c, ph_jp, desc_jp):
    return (f"【Veo 3.1／日本語】開始キーフレーム＝この画像（image-to-video）。"
            f"被写体：{ppe_jp(c['cat'])}を着けた日本人作業員と{machine_jp(c['cat'])}。"
            f"場面：{ph_jp}。アクション：{desc_jp} "
            f"カメラ：ゆっくりとした寄り（緩やかなプッシュイン）／手持ちの微振動。"
            f"ライティング：会場内の自然な照明。スタイル：リアルなドキュメンタリー写真調、実在ロゴ・可読文字なし。"
            f"安全教育用の再現であり流血・残虐表現は含めない。約8秒・16:9。")


def veo_en(c, ph_en, desc_en):
    return (f"[Veo 3.1 / English] First keyframe = the provided image (image-to-video). "
            f"Subject: Japanese workers in {ppe_en(c['cat'])} with {machine_en(c['cat'])}. "
            f"Scene: {ph_en}. Action: {desc_en} "
            f"Camera: slow push-in with slight handheld motion. "
            f"Lighting: natural indoor venue light. Style: realistic documentary photography, no real logos or readable text. "
            f"A safety-education re-enactment with no blood or gore. About 8 seconds, 16:9.")


# ---------------- Markdown ----------------
def build_md():
    L = []
    L.append("# 事故再現 動画プロンプト集 video_prompts_v16")
    L.append("")
    L.append("イベント設営現場 想定事故事例集（全15事例）｜株式会社 博展 御中")
    L.append("")
    L.append(f"{SUPERVISOR}　／　作成日：{TODAY}")
    L.append("")
    L.append("> 各事例の採用ベース画像＋リアル化画像（base / OpenAI / Google）を開始フレームに用いる **image-to-video** 前提のプロンプト集です。")
    L.append("> 1事例につき〔前 → 事故の瞬間 → 後〕の3フェーズを、**OpenAI Sora 2** 用と **Google Veo 3.1** 用の2種、**日本語・英語併記**で掲載します。")
    L.append("> 約8秒・日本の会場・PPE着用・実在ロゴなし・**流血/残虐表現なし**・「安全教育用の再現」という文脈を各プロンプトに明記しています（生成フィルタ配慮）。")
    L.append("> ※本映像は生成AIによる創作（再現）であり、特定の事故・人物・企業を示すものではありません。")
    L.append("")
    for c in CASES:
        L.append("---")
        L.append("")
        L.append(f"## 事故事例 {c['n']}　{c['title']}")
        L.append("")
        L.append(f"- カテゴリ：{c['cat']}（{machine_jp(c['cat'])}）")
        L.append(f"- 開始フレーム画像：`photos_v16/{c['n']}/base.png` ／ `openai.png` ／ `google.png`（3案いずれかを開始/キーフレームに使用）")
        L.append(f"- {SUPERVISOR}")
        L.append("")
        # 画像参照（md上は相対パスで表示）
        for fn in PHOTO_FILES:
            L.append(f"![{c['n']} {fn}](photos_v16/{c['n']}/{fn})")
        L.append("")
        for ph_jp, ph_en, desc_jp, desc_en in phases(c):
            L.append(f"### {ph_jp} / {ph_en}")
            L.append("")
            L.append("**OpenAI Sora 2**")
            L.append("")
            L.append("- " + sora_jp(c, ph_jp, desc_jp))
            L.append("- " + sora_en(c, ph_en, desc_en))
            L.append("")
            L.append("**Google Veo 3.1**")
            L.append("")
            L.append("- " + veo_jp(c, ph_jp, desc_jp))
            L.append("- " + veo_en(c, ph_en, desc_en))
            L.append("")
    L.append("---")
    L.append("")
    L.append(f"合計：15事例 × 3フェーズ × （Sora 2 + Veo 3.1）× 日英 = {15*3*2*2} プロンプト。")
    L.append("")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return 15 * 3 * 2 * 2


# ---------------- PDF (PIL multipage) ----------------
PW, PH = 1240, 1754  # A4 @150dpi
M = 60


def font(sz, b=False):
    cands = ([r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc"] if b
             else [r"C:\Windows\Fonts\YuGothR.ttc", r"C:\Windows\Fonts\meiryo.ttc"])
    for p in cands:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


F_TITLE = font(40, True)
F_H1 = font(30, True)
F_H2 = font(24, True)
F_LBL = font(22, True)
F_BODY = font(21, False)
F_SMALL = font(18, False)
F_FOOT = font(16, False)

RED = (192, 57, 43)
DARK = (30, 30, 30)
GRAY = (110, 110, 110)
BLUE = (11, 102, 195)


def wrap(d, text, f, mw):
    out = []
    cur = ""
    for ch in text:
        if ch == "\n":
            out.append(cur)
            cur = ""
            continue
        if d.textlength(cur + ch, font=f) <= mw:
            cur += ch
        else:
            out.append(cur)
            cur = ch
    out.append(cur)
    return out


class PDF:
    def __init__(self):
        self.pages = []
        self.new_page()

    def new_page(self):
        self.im = Image.new("RGB", (PW, PH), "white")
        self.d = ImageDraw.Draw(self.im)
        self.y = M
        self.pages.append(self.im)

    def space(self, h):
        self.y += h

    def ensure(self, h):
        if self.y + h > PH - 70:
            self.footer()
            self.new_page()

    def footer(self):
        self.d.text((M, PH - 50), SUPERVISOR + "　｜　video_prompts_v16", font=F_FOOT, fill=GRAY)
        self.d.text((PW - 140, PH - 50), "p.%d" % len(self.pages), font=F_FOOT, fill=GRAY)

    def text(self, s, f, fill=DARK, mw=None, lh=None, indent=0):
        mw = mw or (PW - 2 * M - indent)
        lh = lh or (f.size + 8)
        for ln in wrap(self.d, s, f, mw):
            self.ensure(lh)
            self.d.text((M + indent, self.y), ln, font=f, fill=fill)
            self.y += lh

    def rule(self, color=(210, 210, 210)):
        self.ensure(14)
        self.d.line([(M, self.y), (PW - M, self.y)], fill=color, width=2)
        self.y += 14


def cover_page(pdf):
    d = pdf.d
    d.rectangle([0, 0, PW, 150], fill=RED)
    d.text((M, 48), "事故再現 動画プロンプト集", font=F_TITLE, fill="white")
    pdf.y = 200
    pdf.text("イベント設営現場 想定事故事例集（全15事例）", F_H1, DARK)
    pdf.space(6)
    pdf.text("video_prompts_v16　｜　株式会社 博展 御中", F_H2, DARK)
    pdf.space(10)
    pdf.text(SUPERVISOR, F_BODY, GRAY)
    pdf.text("作成日：" + TODAY, F_BODY, GRAY)
    pdf.space(20)
    intro = [
        "本資料は、各事例の採用ベース画像＋リアル化画像（base / OpenAI / Google の3案）を",
        "開始フレームに用いる image-to-video 前提の動画プロンプト集です。",
        "1事例につき〔前 → 事故の瞬間 → 後〕の3フェーズを、OpenAI Sora 2 用と Google Veo 3.1 用の",
        "2種、日本語・英語を併記して掲載します。",
        "約8秒・日本の会場・PPE着用・実在ロゴなし・流血/残虐表現なし・「安全教育用の再現」という",
        "文脈を各プロンプトに明記しています（生成フィルタへの配慮）。",
    ]
    for s in intro:
        pdf.text(s, F_BODY, DARK)
    pdf.space(16)
    pdf.text("※本映像は生成AIによる創作（再現）であり、特定の事故・人物・企業を示すものではありません。",
             F_SMALL, RED)
    pdf.space(8)
    pdf.text("※プロンプト件数：15事例 × 3フェーズ × （Sora 2＋Veo 3.1）× 日英 ＝ 180 プロンプト。",
             F_SMALL, GRAY)


def case_images(pdf, c):
    """3枚を横並びで配置。"""
    gap = 24
    iw = (PW - 2 * M - 2 * gap) // 3
    ih = int(iw / 1.4)
    pdf.ensure(ih + 40)
    x = M
    for fn in PHOTO_FILES:
        fp = os.path.join(PHOTOS, c["n"], fn)
        try:
            im = Image.open(fp).convert("RGB")
            # center-crop to ratio
            r = 1.4
            w, h = im.size
            if w / h > r:
                nw = int(h * r)
                im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = int(w / r)
                im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
            im = im.resize((iw, ih))
            pdf.im.paste(im, (x, pdf.y))
            pdf.d.rectangle([x, pdf.y, x + iw, pdf.y + ih], outline=(180, 180, 180), width=1)
        except Exception as e:
            pdf.d.rectangle([x, pdf.y, x + iw, pdf.y + ih], outline=(180, 180, 180), width=1)
            pdf.d.text((x + 8, pdf.y + 8), "(img)", font=F_SMALL, fill=GRAY)
        x += iw + gap
    pdf.y += ih + 6
    pdf.text("※開始フレーム候補（左：base／中：OpenAI／右：Google）。いずれか1案を image-to-video の開始/キーフレームに使用。",
             F_SMALL, GRAY)
    pdf.space(8)


def build_pdf():
    pdf = PDF()
    cover_page(pdf)
    pdf.footer()
    for c in CASES:
        pdf.new_page()
        # 見出し帯
        pdf.d.rectangle([0, pdf.y, PW, pdf.y + 56], fill=RED)
        pdf.d.text((M, pdf.y + 12), "事故事例 %s" % c["n"], font=F_H1, fill="white")
        pdf.y += 70
        pdf.text(c["title"], F_H2, DARK)
        pdf.space(4)
        pdf.text("カテゴリ：%s（%s）" % (c["cat"], machine_jp(c["cat"])), F_SMALL, GRAY)
        pdf.text(SUPERVISOR, F_SMALL, GRAY)
        pdf.space(10)
        case_images(pdf, c)
        pdf.rule()
        for ph_jp, ph_en, desc_jp, desc_en in phases(c):
            pdf.ensure(60)
            pdf.text("■ %s / %s" % (ph_jp, ph_en), F_LBL, RED)
            pdf.space(4)
            pdf.text("◆ OpenAI Sora 2", F_LBL, DARK)
            pdf.text(sora_jp(c, ph_jp, desc_jp), F_BODY, DARK, indent=14)
            pdf.space(2)
            pdf.text(sora_en(c, ph_en, desc_en), F_SMALL, (70, 70, 70), indent=14)
            pdf.space(8)
            pdf.text("◆ Google Veo 3.1", F_LBL, DARK)
            pdf.text(veo_jp(c, ph_jp, desc_jp), F_BODY, DARK, indent=14)
            pdf.space(2)
            pdf.text(veo_en(c, ph_en, desc_en), F_SMALL, (70, 70, 70), indent=14)
            pdf.space(14)
        pdf.footer()
    pdf.pages[0].save(OUT_PDF, save_all=True, append_images=pdf.pages[1:])
    return len(pdf.pages)


def main():
    nprompts = build_md()
    npages = build_pdf()
    print("SAVED", os.path.basename(OUT_MD), "/", os.path.basename(OUT_PDF),
          "| prompts=", nprompts, "| pdf_pages=", npages)


if __name__ == "__main__":
    main()
