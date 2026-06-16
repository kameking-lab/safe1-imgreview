# make_figs_study2_v3.py — V3: 確定素材ベースの説明図 3点を figs/ に出力
#   ① TGL法制化タイムライン図   fig_tgl_timeline.png
#   ② 資格・装備 早見表        fig_qual_table.png
#   ③ 危険ポイント アイコン表   fig_danger_points.png
# ※ AI画像生成ではない(matplotlibの作図)。法令・日付・条文・罰則は RULES_STUDY2「確定素材」をVERBATIM使用。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

# --- 日本語フォント登録(文字化け回避) ---
FONT_R = r"C:\Windows\Fonts\YuGothR.ttc"
FONT_B = r"C:\Windows\Fonts\YuGothB.ttc"
for fp in (FONT_R, FONT_B):
    if os.path.exists(fp):
        font_manager.fontManager.addfont(fp)
NAME_R = font_manager.FontProperties(fname=FONT_R).get_name()
NAME_B = font_manager.FontProperties(fname=FONT_B).get_name() if os.path.exists(FONT_B) else NAME_R
plt.rcParams["font.family"] = NAME_R
plt.rcParams["axes.unicode_minus"] = False

OUT = "figs"
os.makedirs(OUT, exist_ok=True)

RED, ORANGE, GREEN, BLUE, GRAY = "#c0392b", "#e67e22", "#27ae60", "#2c6fbb", "#7f8c8d"
LIGHT = "#f4f6f8"


# =========================================================
# ① TGL法制化タイムライン
# =========================================================
def timeline():
    steps = [
        ("平成25年(2013)3月", "荷役作業安全対策\nガイドライン(基発第1号)", GRAY),
        ("令和5年(2023)3月28日", "省令改正 → 通達\n基発0328第5号", BLUE),
        ("令和5年(2023)10月1日\n施行", "①昇降設備設置の範囲拡大\n②保護帽着用範囲拡大\n③運転位置離脱時の措置", ORANGE),
        ("令和6年(2024)2月1日\n施行", "④テールゲートリフター\n操作業務の特別教育 義務化", RED),
    ]
    n = len(steps)
    fig, ax = plt.subplots(figsize=(11.0, 5.6))
    ax.set_xlim(0, n)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.text(n / 2, 9.5, "TGL（テールゲートリフター）法制化の流れ",
            ha="center", va="center", fontsize=19, fontweight="bold", fontfamily=NAME_B)

    y_line = 5.4
    ax.plot([0.35, n - 0.35], [y_line, y_line], color="#bdc3c7", lw=4, zorder=1)
    for i, (date, body, col) in enumerate(steps):
        x = i + 0.5
        ax.add_patch(Circle((x, y_line), 0.16, color=col, zorder=3))
        # 日付(線の上) / 内容(線の下) を交互配置
        if i % 2 == 0:
            ax.text(x, y_line + 0.55, date, ha="center", va="bottom",
                    fontsize=11, fontweight="bold", color=col)
            box = FancyBboxPatch((x - 0.46, y_line - 2.55), 0.92, 1.95,
                                 boxstyle="round,pad=0.04,rounding_size=0.12",
                                 fc=LIGHT, ec=col, lw=1.6, zorder=2)
            ax.add_patch(box)
            ax.text(x, y_line - 1.55, body, ha="center", va="center", fontsize=10)
        else:
            ax.text(x, y_line - 0.55, date, ha="center", va="top",
                    fontsize=11, fontweight="bold", color=col)
            box = FancyBboxPatch((x - 0.46, y_line + 0.62), 0.92, 1.95,
                                 boxstyle="round,pad=0.04,rounding_size=0.12",
                                 fc=LIGHT, ec=col, lw=1.6, zorder=2)
            ax.add_patch(box)
            ax.text(x, y_line + 1.6, body, ha="center", va="center", fontsize=10)

    ax.text(n / 2, 0.55,
            "TGL特別教育：学科4時間＋実技2時間 ／ 罰則：6月以下の懲役 or 50万円以下の罰金 ／ 緑・白ナンバー・積載量問わず対象",
            ha="center", va="center", fontsize=10.5, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", fc="#fdecea", ec=RED, lw=1.2))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_tgl_timeline.png"), dpi=150)
    plt.close(fig)
    print("wrote fig_tgl_timeline.png")


# =========================================================
# ② 資格・装備 早見表
# =========================================================
def qual_table():
    fig, ax = plt.subplots(figsize=(11.0, 6.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.text(6, 11.4, "資格・装備 早見表（高所作業車 ／ フルハーネス ／ TGL）",
            ha="center", va="center", fontsize=18, fontweight="bold", fontfamily=NAME_B)

    def card(x, y, w, h, title, lines, col):  # noqa
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                     boxstyle="round,pad=0.05,rounding_size=0.18",
                     fc="white", ec=col, lw=2.2, zorder=2))
        ax.add_patch(FancyBboxPatch((x, y + h - 0.95), w, 0.95,
                     boxstyle="round,pad=0.05,rounding_size=0.18",
                     fc=col, ec=col, lw=2.2, zorder=3))
        ax.text(x + w / 2, y + h - 0.48, title, ha="center", va="center",
                fontsize=13, fontweight="bold", color="white", zorder=4)
        ax.text(x + 0.3, y + h - 1.35, lines, ha="left", va="top", fontsize=10.5, zorder=4)

    # 高所作業車 資格(作業床高さで分岐)
    card(0.4, 6.2, 5.5, 4.4, "高所作業車の運転資格", col=BLUE, lines=(
        "■ 作業床高さ 10m 以上\n"
        "   ＝ 運転技能講習\n"
        "   （学科11h＋実技6h＋学科試験1h）\n\n"
        "■ 作業床高さ 10m 未満\n"
        "   ＝ 特別教育"))
    # フルハーネス/墜落制止用器具
    card(6.1, 6.2, 5.5, 4.4, "墜落制止用器具・フルハーネス", col=ORANGE, lines=(
        "■ 高さ 6.75m 超 ＝ フルハーネス着用義務\n"
        "   （6.75m以下は胴ベルト一本つり可／\n"
        "    建設は 5m 以上）\n\n"
        "■ 2022年1月：旧規格安全帯 使用禁止\n"
        "   → フルハーネス義務化 完了\n\n"
        "■ 安衛則 第194条の22\n"
        "  （垂直昇降式を除く作業床上で使用義務）"))
    # TGL特別教育
    card(0.4, 1.4, 5.5, 4.2, "TGL 操作業務 特別教育", col=RED, lines=(
        "■ 令和6年(2024)2月1日 義務化\n\n"
        "■ 学科 4時間 ＋ 実技 2時間\n\n"
        "■ 罰則：6月以下の懲役\n"
        "   or 50万円以下の罰金\n\n"
        "■ 緑・白ナンバー／積載量問わず対象"))
    # バスケット内補足
    card(6.1, 1.4, 5.5, 4.2, "高所作業車 バスケット内の扱い", col=GREEN, lines=(
        "■ バスケット内は通常「作業床あり」\n"
        "   → 墜落制止用器具の特別教育は対象外\n\n"
        "■ ただし 6.75m 超では\n"
        "   フルハーネス使用義務\n\n"
        "※ 高さ基準で装備・教育が変わる点に注意"))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_qual_table.png"), dpi=150)
    plt.close(fig)
    print("wrote fig_qual_table.png")


# =========================================================
# ③ 危険ポイント アイコン表
# =========================================================
def danger_points():
    # シンプルな図形でアイコン的表現(AI画像ではない)
    items = [
        ("墜落・転落", RED, "高所作業車・荷台から。\n6.75m超はフルハーネス必須",
         "fall"),
        ("はさまれ・巻き込まれ", ORANGE, "TGL最多。荷とゲート・\n機械の間に挟まれる",
         "pinch"),
        ("転倒", "#16a085", "不安定な姿勢・段差。\n保護帽未着用が重症化要因",
         "trip"),
        ("感電", BLUE, "高所作業車作業中の\n架空電線への接触",
         "shock"),
        ("逸走（いっそう）", "#8e44ad", "運転位置離脱時の措置。\n車両の不意の動き出し",
         "runaway"),
    ]
    fig, ax = plt.subplots(figsize=(11.0, 5.6))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.text(7.5, 9.4, "現場の危険ポイント 5（墜落／はさまれ／転倒／感電／逸走）",
            ha="center", va="center", fontsize=18, fontweight="bold", fontfamily=NAME_B)

    cw = 2.9
    for i, (name, col, desc, kind) in enumerate(items):
        cx = 0.35 + i * cw + cw / 2 - 0.1
        # アイコン円
        cy = 6.2
        ax.add_patch(Circle((cx, cy), 0.95, fc=col, ec="white", lw=2, zorder=3))
        _draw_icon(ax, kind, cx, cy)
        # 名称
        ax.text(cx, 4.7, name, ha="center", va="center", fontsize=12.5,
                fontweight="bold", color=col)
        # 説明枠
        ax.add_patch(FancyBboxPatch((cx - 1.25, 1.7), 2.5, 2.5,
                     boxstyle="round,pad=0.05,rounding_size=0.15",
                     fc=LIGHT, ec=col, lw=1.4, zorder=2))
        ax.text(cx, 2.95, desc, ha="center", va="center", fontsize=9.5, zorder=3)

    ax.text(7.5, 0.5,
            "死亡・重傷者の半数以上がヘルメット未着用（陸運）。保護帽・墜落制止用器具・離脱時措置を徹底。",
            ha="center", va="center", fontsize=10.5, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#fdecea", ec=RED, lw=1.0))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_danger_points.png"), dpi=150)
    plt.close(fig)
    print("wrote fig_danger_points.png")


def _draw_icon(ax, kind, cx, cy):
    """白色の簡易ピクトグラム(図形のみ)"""
    W = "white"
    if kind == "fall":
        # 下向き矢印(落下)
        ax.add_patch(FancyArrowPatch((cx, cy + 0.45), (cx, cy - 0.5),
                     arrowstyle="-|>", mutation_scale=26, color=W, lw=4))
    elif kind == "pinch":
        # 内向き2矢印(はさまれ)
        ax.add_patch(FancyArrowPatch((cx - 0.55, cy), (cx - 0.12, cy),
                     arrowstyle="-|>", mutation_scale=20, color=W, lw=4))
        ax.add_patch(FancyArrowPatch((cx + 0.55, cy), (cx + 0.12, cy),
                     arrowstyle="-|>", mutation_scale=20, color=W, lw=4))
    elif kind == "trip":
        # 斜め矢印(転倒)
        ax.add_patch(FancyArrowPatch((cx - 0.4, cy + 0.45), (cx + 0.45, cy - 0.45),
                     arrowstyle="-|>", mutation_scale=24, color=W, lw=4))
    elif kind == "shock":
        # 稲妻(感電) ジグザグ線
        zx = [cx + 0.18, cx - 0.16, cx + 0.08, cx - 0.2]
        zy = [cy + 0.5, cy + 0.05, cy + 0.0, cy - 0.5]
        ax.plot(zx, zy, color=W, lw=4, solid_joinstyle="miter")
    elif kind == "runaway":
        # 右向き矢印(逸走/動き出し)
        ax.add_patch(FancyArrowPatch((cx - 0.5, cy), (cx + 0.5, cy),
                     arrowstyle="-|>", mutation_scale=26, color=W, lw=4))


timeline()
qual_table()
danger_points()
print("DONE")
