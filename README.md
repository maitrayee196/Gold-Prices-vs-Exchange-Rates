# Gold Money

*Do gold prices really move currencies? A plain-English empirical deep dive into 21 years of daily data.*

&nbsp;

## Table of Contents

* [Intro](#intro)
* [Data](#data)
* [The dollar effect](#the-dollar-effect)
* [Australian Dollar](#australian-dollar)
* [South African Rand](#south-african-rand)
* [Canadian Dollar and Swiss Franc](#canadian-dollar-and-swiss-franc)
* [Long-run anchors and who moves first](#long-run-anchors-and-who-moves-first)
* [Trading strategy](#trading-strategy)
* [Discussion](#discussion)
* [Reproduce](#reproduce)
* [Further reading](#further-reading)

&nbsp;

## Intro

Market commentary routinely calls the Australian dollar and the South African rand "gold currencies": when gold rallies, they are supposed to rally too, because gold is a large share of these countries' exports. It sounds sensible. This project tests whether the data actually agrees.

Gold is a tricky commodity to test, because it is not just a commodity — it is also a form of money. Its price is driven by US real interest rates, the strength of the US dollar, and safe-haven demand in anxious times. Those are the very same global forces that drive commodity currencies. So a naive correlation between gold and AUD may reflect nothing but the dollar and risk appetite. Our design deals with this in two ways:

1. **Neutral numeraire.** Every price is re-denominated in **Japanese yen** — Japan is a deep, free-floating currency market and a negligible gold producer. Results are cross-checked in USD terms to expose the dollar effect.
2. **Controls.** The broad USD index (FRED DTWEXBGS) and the VIX enter as controls, so gold's coefficient measures gold, not the dollar or risk sentiment wearing a gold costume.

Sample: daily, **2005-01-04 to 2026-02-25** (5,146 observations). Currencies: AUD and ZAR (the alleged gold currencies), CAD (a large but diversified exporter, our control case), CHF (a safe-haven currency with no mines, to expose the look-alike channel).

&nbsp;

## Data

| Series | Source (mirror) | Range used |
|---|---|---|
| Gold PM fix, USD (daily) | LBMA via `forex-centuries` | 2005 – 2026-02 |
| Fed H.10 daily FX (all quoted local-per-USD) | `datasets/exchange-rates` | 2005 – 2026-02 |
| Broad USD index (DTWEXBGS) | FRED via `forex-centuries` | 2006 – 2025-12 |
| VIX daily close | CBOE via `datasets/finance-vix` | 2005 – 2026-02 |
| Gold monthly average | LBMA via `datasets/gold-prices` | context only |

Crosses are built as `JPY per unit of currency` (e.g. AUDJPY = (JPY/USD)/(AUD/USD)); gold in yen = gold USD × JPY/USD. Everything enters models in natural logs.

&nbsp;

## The dollar effect

Before any modelling, the single most important chart in this project. In USD terms the rand looks strongly (negatively!) related to gold; re-priced in yen, most of that relationship is revealed as the rand's long depreciation trend against a rising gold trend — two trends, one spurious regression waiting to happen.

![alt text](preview/dollar_effect_zar.png)

The full-sample log-log regression makes the same point numerically. In USD terms, ZAR "explains" gold with R² = 0.53 — with a **negative** beta of −0.57, the opposite sign of the gold-currency story. Anyone who ran this regression in levels and stopped there would conclude the rand is an *anti*-gold currency.

&nbsp;

## Australian Dollar

Australia is a top-three gold producer and gold is consistently among its top export earners — the cleanest candidate. The full-sample bivariate regression of log AUDJPY on log gold-in-JPY is unimpressive: beta 0.07, R² 0.11. But split the sample and the story changes completely:

| Period | Gold beta | Newey-West t | R² |
|---|---|---|---|
| 2005–2012 | −0.02 | −1.3 | 0.00 |
| 2013–2019 | −0.51 | −3.2 | 0.11 |
| **2020–2026** | **+0.23** | **11.0** | **0.63** |

The AUD became a gold currency in the 2020s — the decade of the great gold bull market ($1,500 → $5,000+) and record central-bank buying. Before that, nothing, or even the wrong sign during the 2013 taper era.

![alt text](preview/subsample_beta.png)

Crucially, the link **survives controls**. With the broad dollar index and VIX in the regression (2006–2025), gold keeps a positive coefficient of **0.16 with t = 12.2**. For AUD, gold is not just the dollar in disguise.

![alt text](preview/comovement.png)

&nbsp;

## South African Rand

The rand is the historic "gold currency" — and the data retire the title. Full sample in JPY terms: beta **−0.37**, R² 0.50, the wrong sign. With controls, gold's coefficient stays negative (−0.15) while the broad dollar absorbs everything (beta −1.22): the rand is a **dollar-beta and risk currency, not a gold currency**. The reason is structural: South African gold output has declined for two decades (from world #1 to outside the top five), while platinum-group metals, coal and — above all — global risk appetite dominate the rand. The 2020–2026 sub-sample does turn positive (beta 0.20, t = 10.5), but so does everything in that regime; the controls model says the dollar owns the rand.

&nbsp;

## Canadian Dollar and Swiss Franc

**CAD (control case).** Canada is a large but diversified exporter. As expected, gold effects are small (full sample beta 0.07, R² 0.09), yet — surprisingly — with controls the gold coefficient is positive and significant (0.11, t = 5.2), and 2020–2026 R² hits 0.60. The loonie was a better gold currency than the rand in the 2020s.

**CHF (safe-haven case).** The franc posts the *highest* full-sample fit of all (beta 0.36, R² 0.78; with controls t = 24). No Swiss gold mines exist — this is the **portfolio channel**: gold and CHF are the two classic safe-haven assets and trend together against everything else. CHF is the proof that a big gold R² does not require a single gram of gold exports — exactly why exporter regressions need controls.

&nbsp;

## Long-run anchors and who moves first

* **Unit roots:** all log levels are I(1), all returns I(0) (ADF).
* **Long run:** *no cointegration anywhere.* Engle-Granger fails for all four (AUD closest, p = 0.07; ZAR p = 0.88). Johansen trace on {FX, gold, broad USD} selects rank 0 in every case. There is no rubber band pulling any of these currencies back toward gold; divergences can persist for years.
* **Error correction (indicative, given no cointegration):** adjustment speeds are glacial — half-lives of 190–350 trading days.
* **Short-run Granger causality (5 lags, daily returns):** a clean split. **Gold → AUD (p = 0.0006) and gold → CAD (p = 0.011)**: gold moves first for the producer currencies. **ZAR → gold (p = 0.004) and CHF → gold (p = 0.007)**: for the risk/safe-haven currencies the information flows the other way. The direction of prediction identifies the currency type.
* **Out-of-sample (realized-fundamental exercise):** using *realized* same-day gold returns, the gold model beats the random walk by 9–12% in MSE at daily frequency. This is contemporaneous fit, not a tradable ex-ante forecast — the daily link is real, but it is not a crystal ball.

![alt text](preview/rolling_r2.png)

The rolling chart is the honest summary: every currency's gold link is **episodic**. Rolling 250-day R² exceeds a 70% validity threshold only 7–16% of the time, in clusters (2008–09, 2011–13, 2022–2026).

&nbsp;

## Trading strategy

A momentum-on-model-break rule: rolling 50-day regression of FX on gold (both in JPY); trade only when rolling R² ≥ 50%; enter in the direction of a ±2σ break; exit after 10 days or at a ±2% stop. Backtest 2015–2026.

| Currency | Trades | Total return | Win rate |
|---|---|---|---|
| AUD | 43 | **+4.5%** | 53% |
| ZAR | 45 | −29.0% | 36% |
| CAD | 40 | −5.0% | 53% |
| CHF | 45 | −8.9% | 44% |

![alt text](preview/aud_fit.png)
![alt text](preview/strategy_aud.png)

Only AUD is net positive, and modestly. The parameter grid (holding period × stop) peaks at +9.2% total (hold 10 days, 3% stop) but is sign-unstable — several cells are negative:

![alt text](preview/heatmap_aud.png)

Verdict: **gold-currency relationships flip regimes too often for a fixed-parameter rule.** A commodity-currency strategy needs stable single-commodity dependence, and no currency depends on gold that way. Trade this only with a regime filter (e.g. only in high rolling-R² clusters), or don't trade it at all.

&nbsp;

## Discussion

1. **"Gold currency" is a regime, not an identity.** AUD earns the label only after 2020; ZAR lost it a decade ago; CHF fakes it via the safe-haven channel.
2. **The dollar effect is the great illusion-maker.** Every USD-denominated gold-FX chart overstates (or sign-flips) the relationship. Neutral-numeraire pricing plus a broad-dollar control is the minimum honest specification.
3. **No long-run anchor.** The absence of cointegration means gold-FX divergences are not mean-reverting on any horizon a trader (or central bank) cares about.
4. **Causality direction identifies currency type.** Gold leads producer currencies (AUD, CAD); risk currencies lead gold (ZAR, CHF). This is a testable classification rule for any other candidate currency (PEN, GHS next).
5. **Limitations.** No TIPS real-rate control at daily frequency (data availability); PEN/GHS not yet included; broad-dollar series starts 2006 and ends 2025-12; LBMA daily fix ends 2026-02 in the mirror used.

&nbsp;

## Reproduce

```bash
pip install -r requirements.txt
python scripts/01_download_data.py   # shallow-clones public dataset mirrors
python scripts/02_build_panel.py     # builds data/processed/panel_daily.csv
python scripts/03_models.py          # writes results/model_results.json
python scripts/04_figures.py         # writes preview/*.png
python scripts/05_backtest.py        # writes results/backtest.json + figures
```

&nbsp;

## Further reading

1. Sjaastad L, Scacciavillani F (1996), *The Price of Gold and the Exchange Rate.*
2. Baur D, Lucey B (2010), *Is Gold a Hedge or a Safe Haven?*
3. Pukthuanthong K, Roll R (2011), *Gold and the Dollar (and the Euro, Pound, and Yen).*
4. Apergis N (2014), *Can Gold Prices Forecast the Australian Dollar Movements?*
5. Capie F, Mills T, Wood G (2005), *Gold as a Hedge Against the Dollar.*
6. Chen Y, Rogoff K (2003), *Commodity Currencies.*
7. Meese R, Rogoff K (1983), *Empirical Exchange Rate Models of the Seventies.*
8. O'Connor F, Lucey B, Batten J, Baur D (2015), *The Financial Economics of Gold — A Survey.*
