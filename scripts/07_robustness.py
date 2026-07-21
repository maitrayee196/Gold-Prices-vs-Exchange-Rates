"""Robustness checks requested by review:

1. Multi-numeraire: re-estimate the key AUD and ZAR results with the euro,
   the Swiss franc, and an equal-weight USD/EUR/JPY/GBP basket as the
   measuring stick (in addition to the yen used in the main text).
2. Returns-based regressions (log first differences), which sidestep the
   non-stationarity of price levels entirely.
3. A formal structural-break search (Quandt-Andrews sup-F over all candidate
   dates with 15% trimming) instead of the hand-picked 2020 sample split.
4. Institutional backtest metrics for the AUD strategy: annualized return
   and volatility, Sharpe ratio, and maximum drawdown from a daily P&L series.

Writes results/robustness.json.
"""
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
panel = pd.read_csv(ROOT / "data/processed/panel_daily.csv",
                    parse_dates=["date"]).set_index("date")

R = {}

def nw(y, X, lags=20):
    X = sm.add_constant(X)
    return sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": lags})

# ---------- numeraire construction ----------
# All raw rates are local-per-USD. Value of currency c in numeraire n:
#   c in USD = 1 / c_per_usd ; USD in n = n_per_usd ; so c_in_n = n_per_usd / c_per_usd
# Basket numeraire: equal-weight log basket of USD, EUR, JPY, GBP
def in_numeraire(ccy_per_usd, num_per_usd):
    return num_per_usd / ccy_per_usd

num_defs = {
    "JPY": panel["jpy_per_usd"],
    "EUR": panel["eur_per_usd"],
    "CHF": panel["chf_per_usd"],
}
# basket: log price of USD in basket = -(1/4)(log eur_pu + log jpy_pu + log gbp_pu + 0)
# value of currency c in basket units (log): log(1/c_per_usd) + log(USD in basket)
log_usd_in_basket = -(np.log(panel["eur_per_usd"]) + np.log(panel["jpy_per_usd"])
                      + np.log(panel["gbp_per_usd"])) / 4.0

def log_in_basket(ccy_per_usd):
    return -np.log(ccy_per_usd) + log_usd_in_basket

def log_gold_in(num):
    if num == "BASKET":
        return np.log(panel["gold_usd"]) + log_usd_in_basket
    return np.log(panel["gold_usd"]) + np.log(num_defs[num])

def log_fx_in(ccy, num):
    if num == "BASKET":
        return log_in_basket(panel[f"{ccy}_per_usd"])
    return np.log(in_numeraire(panel[f"{ccy}_per_usd"], num_defs[num]))

# ---------- 1 & 2: numeraire robustness for AUD and ZAR ----------
res_num = {}
for ccy in ["aud", "zar"]:
    res_num[ccy] = {}
    for num in ["JPY", "EUR", "CHF", "BASKET"]:
        if ccy == "chf" and num == "CHF":
            continue
        y = log_fx_in(ccy, num)
        x = log_gold_in(num)
        # levels, 2020-26
        s = slice("2020-01-01", "2026-02-25")
        m_lv = nw(y.loc[s], x.loc[s])
        # returns, 2020-26
        dy, dx = y.diff().loc[s], x.diff().loc[s]
        m_rt = nw(dy, dx, lags=5)
        # controls model, full 2006+ (controls only defined vs USD; still valid regressors)
        sub = panel.dropna(subset=["usd_broad", "vix"]).index
        yc = y.loc[y.index.intersection(sub)]
        Xc = pd.DataFrame({"gold": x, "usd": np.log(panel["usd_broad"]),
                           "vix": np.log(panel["vix"])}).loc[yc.index]
        m_ct = nw(yc, Xc)
        res_num[ccy][num] = {
            "levels_2020_26": {"beta": round(m_lv.params.iloc[1], 3),
                               "t": round(m_lv.tvalues.iloc[1], 1),
                               "r2": round(m_lv.rsquared, 3)},
            "returns_2020_26": {"beta": round(m_rt.params.iloc[1], 3),
                                "t": round(m_rt.tvalues.iloc[1], 1),
                                "r2": round(m_rt.rsquared, 3)},
            "controls_full": {"beta_gold": round(m_ct.params["gold"], 3),
                              "t_gold": round(m_ct.tvalues["gold"], 1)},
        }
R["numeraire_robustness"] = res_num

# ---------- 3: Quandt-Andrews sup-F break search (AUD vs gold, JPY terms) ----------
def sup_f(y, x, step=5, trim=0.15):
    d = pd.concat([y, x], axis=1, keys=["y", "x"]).dropna()
    n = len(d)
    yv = d["y"].values
    X = sm.add_constant(d["x"].values)
    ssr_full = sm.OLS(yv, X).fit().ssr
    k = 2
    lo, hi = int(n * trim), int(n * (1 - trim))
    best_f, best_i = -1, None
    fs = []
    for i in range(lo, hi, step):
        ssr1 = sm.OLS(yv[:i], X[:i]).fit().ssr
        ssr2 = sm.OLS(yv[i:], X[i:]).fit().ssr
        f = ((ssr_full - ssr1 - ssr2) / k) / ((ssr1 + ssr2) / (n - 2 * k))
        fs.append((str(d.index[i].date()), round(f, 1)))
        if f > best_f:
            best_f, best_i = f, i
    return str(d.index[best_i].date()), round(best_f, 1), fs

breaks = {}
for ccy in ["aud", "zar", "cad", "chf"]:
    y = np.log(panel[f"{ccy}jpy"])
    x = np.log(panel["gold_jpy"])
    date_lv, f_lv, _ = sup_f(y, x)
    date_rt, f_rt, _ = sup_f(y.diff().dropna(), x.diff().dropna())
    breaks[ccy] = {"levels_break": date_lv, "levels_supF": f_lv,
                   "returns_break": date_rt, "returns_supF": f_rt}
R["quandt_andrews"] = breaks

# ---------- 4: institutional metrics for the AUD strategy ----------
W = 50
def daily_strategy_pnl(ccy, r2_min=0.5, hold=10, stop=0.02):
    y = np.log(panel[f"{ccy}jpy"])
    x = np.log(panel["gold_jpy"])
    mx, my = x.rolling(W).mean(), y.rolling(W).mean()
    cov = x.rolling(W).cov(y); vx, vy = x.rolling(W).var(), y.rolling(W).var()
    b1 = (cov / vx); b0 = my - b1 * mx
    r2 = (cov ** 2 / (vx * vy)).clip(0, 1)
    sig = np.sqrt((vy * (1 - r2)).clip(lower=0)) * np.sqrt((W - 1) / W)
    B1, B0, R2_, SIG = b1.shift(1), b0.shift(1), r2.shift(1), sig.shift(1)
    d = panel.loc["2014-06-01":].index
    yv, xv = y.loc[d].values, x.loc[d].values
    B1v, B0v, R2v, SIGv = (s.loc[d].values for s in (B1, B0, R2_, SIG))
    pos = np.zeros(len(d))
    cur, entry_p, entry_i = 0, 0, 0
    i = W + 1
    while i < len(d):
        if cur == 0:
            if np.isfinite(R2v[i]) and R2v[i] >= r2_min and SIGv[i] > 0:
                f = B1v[i] * xv[i] + B0v[i]
                if yv[i] > f + 2 * SIGv[i]: cur, entry_p, entry_i = 1, yv[i], i
                elif yv[i] < f - 2 * SIGv[i]: cur, entry_p, entry_i = -1, yv[i], i
        else:
            pos[i] = cur
            pnl = cur * (yv[i] - entry_p)
            if (i - entry_i) >= hold or abs(pnl) >= stop:
                cur = 0
        i += 1
    dy = pd.Series(yv, index=d).diff().fillna(0)
    strat = pd.Series(pos, index=d).shift(0) * dy   # position held during day i return
    eq = strat.cumsum()
    years = (d[-1] - d[W]).days / 365.25
    ann_ret = strat.sum() / years
    ann_vol = strat.std() * np.sqrt(252)
    sharpe = (strat.mean() * 252) / ann_vol if ann_vol > 0 else None
    dd = (eq - eq.cummax()).min()
    return {"ann_return_pct": round(100 * ann_ret, 2),
            "ann_vol_pct": round(100 * ann_vol, 2),
            "sharpe": round(sharpe, 2),
            "max_drawdown_pct": round(100 * dd, 2),
            "total_log_ret_pct": round(100 * strat.sum(), 2),
            "years": round(years, 1)}

R["aud_strategy_metrics"] = daily_strategy_pnl("aud")

with open(ROOT / "results/robustness.json", "w") as f:
    json.dump(R, f, indent=1)
print(json.dumps(R, indent=0))
