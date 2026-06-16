# make_figs_study2.py — V2: 事故型別ランキング / 死亡vs死傷 の図を figs/ に出力
# 一次ソース: data/jniosh/parsed/tgl_enriched.jsonl / aerial_enriched.jsonl
# db: SHIBO=死亡 / SHISYO=死傷 / 未設定=内訳不明、type=事故の型。捏造なし(実カウントのみ)。
import json, os, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# --- 日本語フォント登録(文字化け回避) ---
FONT_R = r"C:\Windows\Fonts\YuGothR.ttc"
FONT_B = r"C:\Windows\Fonts\YuGothB.ttc"
for fp in (FONT_R, FONT_B):
    if os.path.exists(fp):
        font_manager.fontManager.addfont(fp)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT_R).get_name()
plt.rcParams["axes.unicode_minus"] = False

OUT = "figs"
os.makedirs(OUT, exist_ok=True)
PARSED = os.path.join("data", "jniosh", "parsed")

RED, ORANGE, GRAY, BLUE = "#c0392b", "#e67e22", "#95a5a6", "#2c6fbb"


def load(name):
    recs = []
    with open(os.path.join(PARSED, name), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def tally(recs):
    total = collections.Counter()
    shibo = collections.Counter()
    shisyo = collections.Counter()
    n_shibo = n_shisyo = n_unknown = 0
    for r in recs:
        t = (r.get("type") or "不明").strip() or "不明"
        db = r.get("db")
        total[t] += 1
        if db == "SHIBO":
            shibo[t] += 1; n_shibo += 1
        elif db == "SHISYO":
            shisyo[t] += 1; n_shisyo += 1
        else:
            n_unknown += 1
    return total, shibo, shisyo, n_shibo, n_shisyo, n_unknown


def rank_chart(title, total, shibo, shisyo, n_total, fname):
    """事故の型別ランキング(横棒・死亡/死傷を積み上げ)"""
    types = [t for t, _ in total.most_common()]
    types = types[::-1]  # 最多を上に
    s_v = [shibo.get(t, 0) for t in types]
    h_v = [shisyo.get(t, 0) for t in types]
    u_v = [total[t] - shibo.get(t, 0) - shisyo.get(t, 0) for t in types]
    fig, ax = plt.subplots(figsize=(9, 0.52 * len(types) + 1.6))
    ax.barh(types, s_v, color=RED, label="死亡(SHIBO)")
    ax.barh(types, h_v, left=s_v, color=ORANGE, label="死傷(SHISYO)")
    if sum(u_v):
        ax.barh(types, u_v, left=[a + b for a, b in zip(s_v, h_v)], color=GRAY, label="内訳不明")
    for i, t in enumerate(types):
        tot = total[t]
        ax.text(tot + n_total * 0.008, i, f"{tot}  ({tot/n_total*100:.1f}%)",
                va="center", ha="left", fontsize=9)
    ax.set_xlim(0, max(total.values()) * 1.18)
    ax.set_title(title, fontsize=15, fontweight="bold", pad=10)
    ax.set_xlabel("件数")
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150)
    plt.close(fig)
    print("wrote", fname)


def death_injury_chart(tgl, aerial, fname):
    """死亡(SHIBO) vs 死傷(SHISYO) 対比(TGL/高所)"""
    cats = ["TGL\n(テールゲートリフター)", "高所作業車"]
    shibo = [tgl[0], aerial[0]]
    shisyo = [tgl[1], aerial[1]]
    import numpy as np
    x = np.arange(len(cats)); w = 0.38
    fig, ax = plt.subplots(figsize=(8, 5.2))
    b1 = ax.bar(x - w / 2, shibo, w, color=RED, label="死亡(SHIBO)")
    b2 = ax.bar(x + w / 2, shisyo, w, color=ORANGE, label="死傷(SHISYO)")
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(),
                f"{int(b.get_height())}", ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=11)
    ax.set_ylabel("件数")
    ax.set_title("死亡(SHIBO) vs 死傷(SHISYO) 件数対比", fontsize=15, fontweight="bold", pad=10)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.25)
    ax.set_ylim(0, max(shisyo) * 1.15)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150)
    plt.close(fig)
    print("wrote", fname)


tgl = load("tgl_enriched.jsonl")
aer = load("aerial_enriched.jsonl")
t_total, t_shibo, t_shisyo, t_ns, t_nh, t_nu = tally(tgl)
a_total, a_shibo, a_shisyo, a_ns, a_nh, a_nu = tally(aer)

print(f"TGL  total={len(tgl)} SHIBO={t_ns} SHISYO={t_nh} unknown={t_nu}")
print(f"AER  total={len(aer)} SHIBO={a_ns} SHISYO={a_nh} unknown={a_nu}")

rank_chart("TGL 事故の型別ランキング（死亡/死傷 内訳）", t_total, t_shibo, t_shisyo, len(tgl), "fig_tgl_type_rank.png")
rank_chart("高所作業車 事故の型別ランキング（死亡/死傷 内訳）", a_total, a_shibo, a_shisyo, len(aer), "fig_aerial_type_rank.png")
death_injury_chart((t_ns, t_nh), (a_ns, a_nh), "fig_death_vs_injury.png")
print("DONE")
