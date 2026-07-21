"""Generate all figures for the README and working paper (saved to preview/)."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "preview"
PRE.mkdir(exist_ok=True)
panel = pd.read_csv(ROOT / "data/processed/panel_daily.csv",
                    parse_dates=["date"]).set_index("date")
rr = pd.read_csv(ROOT / "data/processed/rolling_r2.csv",
                 parse_dates=["date"]).set_index("date")

plt.rcParams.update({"figure.dpi": 110, "font.size": 9,
                     "axes.grid": True, "grid.alpha": 0.3})
CCYS = {"aud": "AUD/JPY", "zar": "ZAR/JPY", "cad": "CAD/JPY", "chf": "CHF/JPY"}

# 1. Gold vs broad dollar
d = panel.dropna(subset=["usd_broad"])
fig, ax1 = plt.subplots(figsize=(9, 4))
ax1.plot(d.index, d["gold_usd"], color="goldenrod", lw=1.2, label="Gold (USD/oz, LBMA PM)")
ax1.set_ylabel("Gold USD/oz", color="goldenrod")
ax2 = ax1.twinx()
ax2.plot(d.index, d["usd_broad"], color="navy", lw=1, label="Broad USD index")
ax2.set_ylabel("Broad USD index", color="navy")
ax2.grid(False)
ax1.set_title("Gold price and the broad US dollar index, 2006-2026")
fig.tight_layout()
fig.savefig(PRE / "gold_vs_usd.png"); plt.close(fig)

# 2. Co-movement, normalized logs (full sample)
fig, axes = plt.subplots(2, 2, figsize=(11, 6), sharex=True)
for ax, (c, label) in zip(axes.ravel(), CCYS.items()):
    z1 = np.log(panel[f"{c}jpy"]); z1 = (z1 - z1.mean()) / z1.std()
    z2 = np.log(panel["gold_jpy"]); z2 = (z2 - z2.mean()) / z2.std()
    ax.plot(panel.index, z1, lw=0.8, label=label)
    ax.plot(panel.index, z2, lw=0.8, color="goldenrod", label="Gold in JPY")
    ax.set_title(f"{label} vs gold (normalized logs)")
    ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(PRE / "comovement.png"); plt.close(fig)

# 3. Rolling 250-day R2
fig, ax = plt.subplots(figsize=(10, 4.5))
for c, label in CCYS.items():
    ax.plot(rr.index, rr[c], lw=0.9, label=label)
ax.axhline(0.7, color="red", ls="--", lw=0.8)
ax.axhline(0.5, color="gray", ls="--", lw=0.8)
ax.text(rr.index[50], 0.72, "70% model-validity threshold", color="red", fontsize=7)
ax.set_title("Rolling 250-day R²: currency (in JPY) vs gold (in JPY)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(PRE / "rolling_r2.png"); plt.close(fig)

# 4. Sub-sample betas
import json
res = json.load(open(ROOT / "results/model_results.json"))
subs = ["pre_gfc_2005_2012", "taper_2013_2019", "recent_2020_2026"]
sub_labels = ["2005-2012", "2013-2019", "2020-2026"]
x = np.arange(len(CCYS)); w = 0.25
fig, ax = plt.subplots(figsize=(9, 4))
for i, (s, sl) in enumerate(zip(subs, sub_labels)):
    betas = [res["bivariate_jpy"][c][s]["beta"] for c in CCYS]
    ax.bar(x + (i - 1) * w, betas, w, label=sl)
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(x); ax.set_xticklabels([l for l in CCYS.values()])
ax.set_ylabel("Gold beta (log-log)")
ax.set_title("Gold elasticity of each currency by sub-period: the sign flips")
ax.legend()
fig.tight_layout()
fig.savefig(PRE / "subsample_beta.png"); plt.close(fig)

# 5. AUD rolling-model fit with bands (last 4 years)
W = 50
d = panel.loc["2022-01-01":].copy()
y, xg = np.log(d["audjpy"]), np.log(d["gold_jpy"])
fit, sig = pd.Series(index=d.index, dtype=float), pd.Series(index=d.index, dtype=float)
for i in range(W, len(d)):
    ys, xs = y.iloc[i - W:i], xg.iloc[i - W:i]
    b = np.polyfit(xs, ys, 1)
    f = np.polyval(b, xg.iloc[i])
    fit.iloc[i] = f
    sig.iloc[i] = (ys - np.polyval(b, xs)).std()
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(d.index, y, lw=1, label="AUD/JPY (log)", color="steelblue")
ax.plot(d.index, fit, lw=1, label="Fitted from gold (rolling 50d)", color="darkorange")
ax.fill_between(d.index, fit - 2 * sig, fit + 2 * sig, alpha=0.2, color="darkorange",
                label="±2σ band")
ax.set_title("AUD/JPY vs rolling gold-model fit, 2022-2026")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(PRE / "aud_fit.png"); plt.close(fig)

# 6. Dollar effect: ZAR vs gold in USD terms and in JPY terms
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, (fx, gold, ttl) in zip(axes, [
        ("zarusd", "gold_usd", "Both priced in USD"),
        ("zarjpy", "gold_jpy", "Both priced in JPY")]):
    z1 = np.log(panel[fx]); z1 = (z1 - z1.mean()) / z1.std()
    z2 = np.log(panel[gold]); z2 = (z2 - z2.mean()) / z2.std()
    ax.plot(panel.index, z1, lw=0.8, label="ZAR")
    ax.plot(panel.index, z2, lw=0.8, color="goldenrod", label="Gold")
    ax.set_title(ttl); ax.legend(fontsize=8)
fig.suptitle("The dollar effect: ZAR's 'gold link' depends on the numeraire", y=1.02)
fig.tight_layout()
fig.savefig(PRE / "dollar_effect_zar.png", bbox_inches="tight"); plt.close(fig)
print("figures done:", sorted(p.name for p in PRE.glob("*.png")))
