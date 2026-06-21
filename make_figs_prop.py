# -*- coding: utf-8 -*-
# proposal_hakuten 用 不足コンセプト図の生成 (matplotlib / 日本語フォント / 安全色)
# ※ AI画像生成ではない(matplotlibの作図)。捏造数値は使わず概念図のみ。
#    既存figは流用(型別/死亡vs死傷/法制化/資格/危険ポイント)。本スクリプトは不足分のみ新ファイル名 figs/prop_*.png で追加。
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

FONT_R = r"C:\Windows\Fonts\YuGothR.ttc"
FONT_B = r"C:\Windows\Fonts\YuGothB.ttc"
for fp in (FONT_R, FONT_B):
    if os.path.exists(fp):
        font_manager.fontManager.addfont(fp)
NAME_R = font_manager.FontProperties(fname=FONT_R).get_name()
NAME_B = font_manager.FontProperties(fname=FONT_B).get_name() if os.path.exists(FONT_B) else NAME_R
plt.rcParams["font.family"] = NAME_R
plt.rcParams["axes.unicode_minus"] = False

# 安全色
RED = "#D7261E"      # 危険
YELLOW = "#F2B705"   # 注意
GREEN = "#2E9E5B"    # 対策
NAVY = "#1F3A5F"     # ベース
GRAY = "#6B7280"
LIGHT = "#EEF2F7"

OUT = "figs"
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("WROTE", path)


# ============================================================
# 1) 解決アプローチ 矢印フロー図
#    事故データ分析 → 危険を科学的に特定 → 教材化 → AIで量産
# ============================================================
def fig_approach_flow():
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    steps = [
        ("01", "事故データ分析", "約42万件を走査", NAVY),
        ("02", "危険を科学的に特定", "型別・致死率で可視化", RED),
        ("03", "教材化", "対策をコンテンツへ", YELLOW),
        ("04", "AIで量産", "速く・安く更新", GREEN),
    ]
    n = len(steps)
    bw, bh = 2.45, 1.7
    gap = (12 - n * bw) / (n + 1)
    y = 0.85
    centers = []
    for i, (num, title, sub, col) in enumerate(steps):
        x = gap + i * (bw + gap)
        box = FancyBboxPatch((x, y), bw, bh, boxstyle="round,pad=0.04,rounding_size=0.12",
                             linewidth=2.4, edgecolor=col, facecolor="white", zorder=3)
        ax.add_patch(box)
        cx = x + bw / 2
        centers.append((x, x + bw, cx))
        ax.add_patch(Circle((x + 0.42, y + bh - 0.42), 0.3, color=col, zorder=4))
        ax.text(x + 0.42, y + bh - 0.42, num, ha="center", va="center",
                color="white", fontsize=11, fontweight="bold", fontfamily=NAME_B, zorder=5)
        ax.text(cx, y + bh - 0.78, title, ha="center", va="center",
                fontsize=13.5, fontweight="bold", color=col, fontfamily=NAME_B, zorder=5)
        ax.text(cx, y + 0.42, sub, ha="center", va="center",
                fontsize=10.5, color="#333333", zorder=5)
    for i in range(n - 1):
        x0 = centers[i][1]
        x1 = centers[i + 1][0]
        arr = FancyArrowPatch((x0 + 0.02, y + bh / 2), (x1 - 0.02, y + bh / 2),
                              arrowstyle="-|>", mutation_scale=24,
                              linewidth=3.2, color=GRAY, zorder=2)
        ax.add_patch(arr)
    ax.text(6, 2.95, "解決アプローチ：データから対策を導き、AIで量産する",
            ha="center", va="center", fontsize=14.5, fontweight="bold",
            color=NAVY, fontfamily=NAME_B)
    save(fig, "prop_approach_flow.png")


# ============================================================
# 2) 自動化の対比図 (概念) 従来=人手 / AI
#    数値は使わず "日単位 → 時間単位" の相対イメージのみ
# ============================================================
def fig_automation_compare():
    fig, ax = plt.subplots(figsize=(11, 4.4))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    ax.text(5.5, 4.05, "教材づくりの比較（概念イメージ）",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=NAVY, fontfamily=NAME_B)

    # 従来 (人手) : 長いバー
    y_top, y_bot = 2.85, 1.35
    bh = 0.78
    ax.text(0.3, y_top + bh / 2, "従来", ha="left", va="center",
            fontsize=13, fontweight="bold", color=GRAY, fontfamily=NAME_B)
    ax.text(0.3, y_bot + bh / 2, "AI活用", ha="left", va="center",
            fontsize=13, fontweight="bold", color=GREEN, fontfamily=NAME_B)
    x0 = 2.0
    ax.add_patch(FancyBboxPatch((x0, y_top), 7.2, bh, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=GRAY, edgecolor="none", zorder=3))
    ax.text(x0 + 3.6, y_top + bh / 2, "人手で手作り（日単位）", ha="center", va="center",
            color="white", fontsize=12.5, fontweight="bold", fontfamily=NAME_B, zorder=4)
    ax.add_patch(FancyBboxPatch((x0, y_bot), 2.0, bh, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=GREEN, edgecolor="none", zorder=3))
    ax.text(x0 + 1.0, y_bot + bh / 2, "量産（時間単位）", ha="center", va="center",
            color="white", fontsize=12, fontweight="bold", fontfamily=NAME_B, zorder=4)

    arr = FancyArrowPatch((x0 + 7.2, y_top - 0.05), (x0 + 2.0, y_bot + bh + 0.05),
                          arrowstyle="-|>", mutation_scale=26,
                          linewidth=3.2, color=RED, zorder=5,
                          connectionstyle="arc3,rad=-0.15")
    ax.add_patch(arr)
    ax.text(6.9, 2.25, "大幅に短縮", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=RED, fontfamily=NAME_B)
    ax.text(5.5, 0.5, "※ 相対的な概念イメージ（具体的な所要時間は案件により異なる）",
            ha="center", va="center", fontsize=9, color=GRAY)
    save(fig, "prop_automation_compare.png")


# ============================================================
# 3) 自動化の価値 3アイコン
#    属人化しない / 更新が速い / 低コスト
# ============================================================
def fig_value_icons():
    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    items = [
        ("人", "属人化しない", "ベテランの勘に\n依存しない", NAVY),
        ("速", "更新が速い", "最新の事例へ\nすぐ反映", GREEN),
        ("円", "低コスト", "量産で1点あたり\nを抑える", YELLOW),
    ]
    cx_list = [2.0, 5.5, 9.0]
    for (mark, title, sub, col), cx in zip(items, cx_list):
        ax.add_patch(Circle((cx, 2.5), 0.62, facecolor=col, edgecolor="none", zorder=3))
        ax.text(cx, 2.5, mark, ha="center", va="center", color="white",
                fontsize=22, fontweight="bold", fontfamily=NAME_B, zorder=4)
        ax.text(cx, 1.55, title, ha="center", va="center",
                fontsize=14, fontweight="bold", color=col, fontfamily=NAME_B)
        ax.text(cx, 0.75, sub, ha="center", va="center",
                fontsize=10.5, color="#333333", linespacing=1.4)
    save(fig, "prop_value_icons.png")


# ============================================================
# 4) 科学的対策 アイコン (墜落 / はさまれ / 感電)
#    安全色：危険(赤)→対策(緑)
# ============================================================
def fig_measures_icons():
    fig, ax = plt.subplots(figsize=(11, 3.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.8)
    ax.axis("off")
    ax.text(5.5, 3.5, "データから導く 科学的な対策",
            ha="center", va="center", fontsize=15, fontweight="bold",
            color=NAVY, fontfamily=NAME_B)
    items = [
        ("墜落", "フルハーネス着用・\n手すり/開口部養生", RED),
        ("はさまれ", "立入管理・\n動力源の停止確認", YELLOW),
        ("感電", "絶縁・停電確認・\n保護具の徹底", GREEN),
    ]
    cx_list = [2.0, 5.5, 9.0]
    for (risk, measure, col), cx in zip(items, cx_list):
        # 危険(上) → 対策(下)
        ax.add_patch(FancyBboxPatch((cx - 1.35, 2.05), 2.7, 0.78,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=col, edgecolor="none", zorder=3))
        ax.text(cx, 2.44, risk, ha="center", va="center", color="white",
                fontsize=15, fontweight="bold", fontfamily=NAME_B, zorder=4)
        arr = FancyArrowPatch((cx, 2.0), (cx, 1.62), arrowstyle="-|>",
                              mutation_scale=20, linewidth=2.6, color=GRAY, zorder=4)
        ax.add_patch(arr)
        ax.add_patch(FancyBboxPatch((cx - 1.45, 0.45), 2.9, 1.1,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor="white", edgecolor=GREEN, linewidth=2.2, zorder=3))
        ax.text(cx, 1.0, measure, ha="center", va="center", color="#1f3a2f",
                fontsize=10.5, fontweight="bold", linespacing=1.4, zorder=4)
    save(fig, "prop_measures_icons.png")


if __name__ == "__main__":
    fig_approach_flow()
    fig_automation_compare()
    fig_value_icons()
    fig_measures_icons()
    print("DONE prop figs")
