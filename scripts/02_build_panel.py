"""Build the daily analysis panel: JPY-based crosses + controls.

Convention in the source file (datasets/exchange-rates, from Fed H.10):
  ALL series are quoted as local currency per 1 USD (verified against
  2011 and 2026 values for AUD, EUR, GBP).
All crosses are expressed as JPY per unit of the currency, so that the
numeraire (JPY) is neutral with respect to gold production.
"""
import pandas as pd
import numpy as np
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT = Path(__file__).resolve().parents[1] / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# --- FX (H.10, long format) ---
fx = pd.read_csv(RAW / "h10_fx_daily.csv", parse_dates=["Date"])
fx = fx.pivot_table(index="Date", columns="Country", values="Exchange rate")
fx = fx.rename(columns={
    "Australia": "aud_per_usd", "Japan": "jpy_per_usd",
    "South Africa": "zar_per_usd", "Canada": "cad_per_usd",
    "Switzerland": "chf_per_usd", "Euro": "eur_per_usd",
    "United Kingdom": "gbp_per_usd", "Sweden": "sek_per_usd",
})

# --- Gold (LBMA PM fix, USD) ---
gold = pd.read_csv(RAW / "lbma_gold_daily.csv", parse_dates=["date"]).set_index("date")
gold = gold[["gold_pm_usd"]].rename(columns={"gold_pm_usd": "gold_usd"})
gold = gold[gold["gold_usd"] > 0]

# --- VIX ---
vix = pd.read_csv(RAW / "vix-daily.csv", parse_dates=["DATE"]).set_index("DATE")
vix = vix[["CLOSE"]].rename(columns={"CLOSE": "vix"})

# --- Broad dollar (FRED DTWEXBGS, 2006+) ---
usd = pd.read_csv(RAW / "fred_usd_broad_index.csv", parse_dates=["observation_date"])
usd = usd.set_index("observation_date").rename(columns={"DTWEXBGS": "usd_broad"})

# --- Merge ---
df = fx.join(gold, how="inner").join(vix, how="left").join(usd, how="left")

# JPY crosses (JPY per unit of currency)
for ccy in ["aud", "zar", "cad", "chf"]:
    df[f"{ccy}jpy"] = df["jpy_per_usd"] / df[f"{ccy}_per_usd"]
df["gold_jpy"] = df["gold_usd"] * df["jpy_per_usd"]

# USD crosses (for the dollar-effect comparison)
for ccy in ["aud", "zar", "cad", "chf"]:
    df[f"{ccy}usd"] = 1 / df[f"{ccy}_per_usd"]

cols = ["gold_usd", "gold_jpy", "audjpy", "zarjpy", "cadjpy", "chfjpy",
        "audusd", "zarusd", "cadusd", "chfusd", "jpy_per_usd", "vix", "usd_broad"]
panel = df[cols].dropna(subset=["gold_usd", "audjpy", "zarjpy", "cadjpy", "chfjpy"])
panel = panel.loc["2005-01-01":]
panel.index.name = "date"
panel.to_csv(OUT / "panel_daily.csv")
print("panel:", panel.shape, panel.index.min().date(), "->", panel.index.max().date())
print(panel.tail(2).round(2).to_string())
