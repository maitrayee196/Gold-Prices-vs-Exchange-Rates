"""Momentum trading strategies on gold currencies.

Strategy (momentum-on-model-break):
 1. Roll a 50-day OLS of log(FX in JPY) on log(gold in JPY).
 2. The model is 'valid' only if rolling R2 >= threshold.
 3. If the actual price breaks above fit + 2 sigma -> go LONG (momentum);
    below fit - 2 sigma -> go SHORT.
 4. Exit after `hold` days, or when |PnL| >= stop (fraction of entry price).
 5. Recalibrate and repeat.

Backtest window: 2015-01-01 .. 2026-02-25. Outputs results/backtest.json,
preview/strategy_aud.png, preview/heatmap_aud.png.
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
panel = pd.read_csv(ROOT / "data/processed/panel_daily.csv",
                    parse_dates=["date"]).set_index("date")
panel = panel.loc["2014-06-01":]

W = 50
CCYS = ["aud", "zar", "cad", "chf"]

_cache = {}

def prep(ccy):
    """Precompute rolling (window W, ending at t-1) beta, fit, sigma, r2."""
    if ccy in _cache:
        return _cache[ccy]
    y = np.log(panel[f"{ccy}jpy"])
    x = np.log(panel["gold_jpy"])
    mx, my = x.rolling(W).mean(), y.rolling(W).mean()
    cov = x.rolling(W).cov(y)
    vx, vy = x.rolling(W).var(), y.rolling(W).var()
    b1 = cov / vx
    b0 = my - b1 * mx
    r2 = (cov ** 2 / (vx * vy)).clip(0, 1)
    sig = np.sqrt((vy * (1 - r2)).clip(lower=0)) * np.sqrt((W - 1) / W)
    # shift so that at index i we use the window ending at i-1
    out = (y.values, x.values,
           b1.shift(1).values, b0.shift(1).values,
           r2.shift(1).values, sig.shift(1).values, panel.index)
    _cache[ccy] = out
    return out

def run(ccy, r2_min=0.5, hold=10, stop=0.02):
    y, x, B1, B0, R2, SIG, dates = prep(ccy)
    trades = []
    pos = 0          # 0 flat, +1 long, -1 short
    entry_p = entry_i = 0
    i = W + 1
    n = len(y)
    while i < n:
        if pos == 0:
            r2, sig = R2[i], SIG[i]
            if np.isfinite(r2) and r2 >= r2_min and sig > 0:
                f = B1[i] * x[i] + B0[i]
                if y[i] > f + 2 * sig:
                    pos, entry_p, entry_i = 1, y[i], i
                elif y[i] < f - 2 * sig:
                    pos, entry_p, entry_i = -1, y[i], i
            i += 1
        else:
            pnl = pos * (y[i] - entry_p)          # log return
            if (i - entry_i) >= hold or abs(pnl) >= stop:
                trades.append({"entry": str(dates[entry_i].date()),
                               "exit": str(dates[i].date()),
                               "side": pos, "ret": pnl})
                pos = 0
            i += 1
    if not trades:
        return {"n_trades": 0, "total_ret_pct": 0.0, "win_rate": None,
                "avg_ret_pct": None}, trades
    rets = np.array([t["ret"] for t in trades])
    return {"n_trades": len(trades),
            "total_ret_pct": round(100 * rets.sum(), 2),
            "win_rate": round(float((rets > 0).mean()), 2),
            "avg_ret_pct": round(100 * rets.mean(), 3),
            "best_pct": round(100 * rets.max(), 2),
            "worst_pct": round(100 * rets.min(), 2)}, trades

# ---- headline run per currency ----
out = {"params": {"window": W, "r2_min": 0.5, "hold": 10, "stop": 0.02,
                  "backtest_start": "2015", "backtest_end": "2026-02"}}
all_trades = {}
for c in CCYS:
    stats, trades = run(c)
    out[c] = stats
    all_trades[c] = trades

# ---- parameter grid for AUD (heatmap) ----
holds = [5, 10, 15, 20]
stops = [0.01, 0.015, 0.02, 0.03]
grid = np.zeros((len(holds), len(stops)))
for a, h in enumerate(holds):
    for b_, s in enumerate(stops):
        stats, _ = run("aud", hold=h, stop=s)
        grid[a, b_] = stats["total_ret_pct"]
out["aud_grid"] = {"holds": holds, "stops": stops,
                   "total_ret_pct": grid.round(2).tolist()}

with open(ROOT / "results/backtest.json", "w") as f:
    json.dump(out, f, indent=1)

# ---- figures ----
plt.rcParams.update({"figure.dpi": 110, "font.size": 9, "axes.grid": True,
                     "grid.alpha": 0.3})
# equity curve AUD (headline params)
stats, trades = run("aud")
eq_dates = [pd.Timestamp(t["exit"]) for t in trades]
eq = 100 * np.cumsum([t["ret"] for t in trades])
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(eq_dates, eq, marker="o", ms=3, lw=1, color="darkgreen")
ax.axhline(0, color="black", lw=0.8)
ax.set_ylabel("Cumulative return (%, log-return sum)")
ax.set_title(f"AUD/JPY gold-momentum strategy: {stats['n_trades']} trades, "
             f"total {stats['total_ret_pct']}%, win rate {stats['win_rate']}")
fig.tight_layout()
fig.savefig(ROOT / "preview/strategy_aud.png"); plt.close(fig)

# heatmap
fig, ax = plt.subplots(figsize=(6.5, 4.5))
im = ax.imshow(grid, cmap="RdYlGn", aspect="auto")
ax.set_xticks(range(len(stops))); ax.set_xticklabels([f"{s:.1%}" for s in stops])
ax.set_yticks(range(len(holds))); ax.set_yticklabels(holds)
ax.set_xlabel("Stop level (abs log return)"); ax.set_ylabel("Max holding days")
for a in range(len(holds)):
    for b_ in range(len(stops)):
        ax.text(b_, a, f"{grid[a, b_]:.1f}", ha="center", va="center", fontsize=8)
ax.set_title("AUD strategy: total return (%) by holding period × stop")
fig.colorbar(im)
fig.tight_layout()
fig.savefig(ROOT / "preview/heatmap_aud.png"); plt.close(fig)

print(json.dumps({k: v for k, v in out.items() if k != "aud_grid"}, indent=0))
print("grid:", out["aud_grid"]["total_ret_pct"])
