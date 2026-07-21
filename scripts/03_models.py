"""Econometric core: unit roots, OLS (with and without controls),
Engle-Granger and Johansen cointegration, Granger causality, ECM,
rolling R-squared, and safe-haven (VIX-regime) correlations.

Results are written to results/model_results.json.
"""
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint, grangercausalitytests
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
panel = pd.read_csv(ROOT / "data/processed/panel_daily.csv",
                    parse_dates=["date"]).set_index("date")

CCYS = ["aud", "zar", "cad", "chf"]
SUBSAMPLES = {
    "full_2005_2026": ("2005-01-01", "2026-02-25"),
    "pre_gfc_2005_2012": ("2005-01-01", "2012-12-31"),
    "taper_2013_2019": ("2013-01-01", "2019-12-31"),
    "recent_2020_2026": ("2020-01-01", "2026-02-25"),
}
R = {"meta": {"n_obs": len(panel),
              "start": str(panel.index.min().date()),
              "end": str(panel.index.max().date())}}

def nw_ols(y, X, lags=20):
    X = sm.add_constant(X)
    m = sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m

# ---------- 1. Unit roots ----------
ur = {}
for col in ["gold_jpy"] + [f"{c}jpy" for c in CCYS]:
    lv = np.log(panel[col].dropna())
    ur[col] = {
        "adf_level_p": round(adfuller(lv, regression="ct")[1], 3),
        "adf_diff_p": round(adfuller(lv.diff().dropna())[1], 4),
    }
R["unit_roots"] = ur

# ---------- 2. Bivariate OLS in JPY terms, by subsample ----------
biv = {}
for c in CCYS:
    biv[c] = {}
    for name, (a, b) in SUBSAMPLES.items():
        s = panel.loc[a:b]
        y, x = np.log(s[f"{c}jpy"]), np.log(s["gold_jpy"])
        m = nw_ols(y, x)
        biv[c][name] = {"beta": round(m.params.iloc[1], 3),
                        "t": round(m.tvalues.iloc[1], 1),
                        "r2": round(m.rsquared, 3), "n": int(m.nobs)}
R["bivariate_jpy"] = biv

# ---------- 2b. Same regression in USD terms (dollar-effect check) ----------
bivusd = {}
for c in CCYS:
    y, x = np.log(panel[f"{c}usd"]), np.log(panel["gold_usd"])
    m = nw_ols(y, x)
    bivusd[c] = {"beta": round(m.params.iloc[1], 3), "r2": round(m.rsquared, 3)}
R["bivariate_usd"] = bivusd

# ---------- 3. Controls model (2006+, needs usd_broad & vix) ----------
ctrl = {}
sub = panel.dropna(subset=["usd_broad", "vix"]).loc["2006-01-01":]
for c in CCYS:
    y = np.log(sub[f"{c}jpy"])
    X = pd.DataFrame({"log_gold_jpy": np.log(sub["gold_jpy"]),
                      "log_usd_broad": np.log(sub["usd_broad"]),
                      "log_vix": np.log(sub["vix"])})
    m = nw_ols(y, X)
    ctrl[c] = {"beta_gold": round(m.params["log_gold_jpy"], 3),
               "t_gold": round(m.tvalues["log_gold_jpy"], 1),
               "beta_usd": round(m.params["log_usd_broad"], 3),
               "beta_vix": round(m.params["log_vix"], 3),
               "r2": round(m.rsquared, 3)}
R["controls_model"] = ctrl

# ---------- 4. Engle-Granger cointegration ----------
eg = {}
for c in CCYS:
    t, p, _ = coint(np.log(panel[f"{c}jpy"]), np.log(panel["gold_jpy"]))
    eg[c] = {"eg_stat": round(t, 2), "p": round(p, 3)}
R["engle_granger"] = eg

# ---------- 5. Johansen ({fx, gold, usd_broad}, 2006+) ----------
jo = {}
for c in CCYS:
    d = np.log(sub[[f"{c}jpy", "gold_jpy", "usd_broad"]].dropna())
    res = coint_johansen(d, det_order=0, k_ar_diff=5)
    # trace stat vs 95% critical values
    rank = int(sum(res.lr1 > res.cvt[:, 1]))
    jo[c] = {"trace_stats": [round(x, 1) for x in res.lr1],
             "cv_95": [round(x, 1) for x in res.cvt[:, 1]],
             "rank_95": rank}
R["johansen"] = jo

# ---------- 6. Granger causality (returns, 5 lags) ----------
gc = {}
for c in CCYS:
    d = pd.DataFrame({"fx": np.log(panel[f"{c}jpy"]).diff(),
                      "gold": np.log(panel["gold_jpy"]).diff()}).dropna()
    g1 = grangercausalitytests(d[["fx", "gold"]], maxlag=5, verbose=False)
    g2 = grangercausalitytests(d[["gold", "fx"]], maxlag=5, verbose=False)
    gc[c] = {"gold_causes_fx_p": round(min(g1[l][0]["ssr_ftest"][1] for l in g1), 4),
             "fx_causes_gold_p": round(min(g2[l][0]["ssr_ftest"][1] for l in g2), 4)}
R["granger"] = gc

# ---------- 7. ECM speed of adjustment (where EG residual is used) ----------
ecm = {}
for c in CCYS:
    y, x = np.log(panel[f"{c}jpy"]), np.log(panel["gold_jpy"])
    lr = sm.OLS(y, sm.add_constant(x)).fit()
    resid = lr.resid
    dy = y.diff()
    dx = x.diff()
    X = pd.DataFrame({"ect": resid.shift(1), "dx": dx, "dy1": dy.shift(1)})
    m = nw_ols(dy, X)
    ecm[c] = {"ect_coef": round(m.params["ect"], 4),
              "ect_t": round(m.tvalues["ect"], 1),
              "half_life_days": round(np.log(0.5) / np.log(1 + m.params["ect"]), 0)
              if -1 < m.params["ect"] < 0 else None}
R["ecm"] = ecm

# ---------- 8. Rolling 250-day R2 (saved as csv for figures) ----------
roll = {}
W = 250
rr = pd.DataFrame(index=panel.index)
for c in CCYS:
    y, x = np.log(panel[f"{c}jpy"]), np.log(panel["gold_jpy"])
    r2 = y.rolling(W).corr(x) ** 2
    rr[c] = r2
    roll[c] = {"mean_roll_r2": round(float(r2.mean()), 3),
               "max_roll_r2": round(float(r2.max()), 3),
               "share_above_50pct": round(float((r2 > 0.5).mean()), 3),
               "share_above_70pct": round(float((r2 > 0.7).mean()), 3)}
rr.to_csv(ROOT / "data/processed/rolling_r2.csv")
R["rolling_r2"] = roll

# ---------- 9. Safe-haven test: return correlations by VIX regime ----------
sh = {}
d = panel.dropna(subset=["vix"])
rets = pd.DataFrame({c: np.log(d[f"{c}jpy"]).diff() for c in CCYS})
rets["gold"] = np.log(d["gold_jpy"]).diff()
hi = d["vix"] > d["vix"].quantile(0.9)
lo = d["vix"] < d["vix"].quantile(0.5)
for c in CCYS:
    sh[c] = {"corr_all": round(rets[c].corr(rets["gold"]), 3),
             "corr_low_vix": round(rets.loc[lo, c].corr(rets.loc[lo, "gold"]), 3),
             "corr_high_vix": round(rets.loc[hi, c].corr(rets.loc[hi, "gold"]), 3)}
R["safe_haven_corr"] = sh

# ---------- 10. Simple out-of-sample check: random walk vs gold model ----------
oos = {}
for c in CCYS:
    y = np.log(panel[f"{c}jpy"]).diff().dropna()
    x = np.log(panel["gold_jpy"]).diff().dropna()
    d2 = pd.concat([y, x], axis=1, keys=["dy", "dx"]).dropna()
    n = len(d2)
    split = int(n * 0.7)
    err_rw, err_gold = [], []
    # expanding-window one-step forecasts, refit every 20 obs for speed
    beta = None
    for i in range(split, n):
        if beta is None or (i - split) % 20 == 0:
            m = sm.OLS(d2["dy"].iloc[:i], sm.add_constant(d2["dx"].iloc[:i])).fit()
            beta = m.params
        f_gold = beta.iloc[0] + beta.iloc[1] * d2["dx"].iloc[i]
        err_rw.append(d2["dy"].iloc[i] ** 2)
        err_gold.append((d2["dy"].iloc[i] - f_gold) ** 2)
    mse_rw, mse_gold = np.mean(err_rw), np.mean(err_gold)
    oos[c] = {"mse_ratio_gold_vs_rw": round(mse_gold / mse_rw, 4),
              "oos_r2_pct": round(100 * (1 - mse_gold / mse_rw), 2)}
R["out_of_sample"] = oos

with open(ROOT / "results/model_results.json", "w") as f:
    json.dump(R, f, indent=1)
print(json.dumps(R, indent=0))
