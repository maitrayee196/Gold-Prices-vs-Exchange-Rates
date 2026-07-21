# GOLD MONEY
### Global FX & Commodities Research
 
**Do gold prices really move currencies? Evidence from 21 years of daily data**
 
| | |
|---|---|
| **Research by** | Maitrayee Anand Vishnu |
| **Date** | July 2026 |
| **Asset classes** | Gold (XAU), G10 & EM FX |
| **Coverage** | AUD, ZAR, CAD, CHF vs. gold (JPY numeraire) |
| **Sample** | Daily, 4 Jan 2005 to 25 Feb 2026 (5,146 obs.) |
 
---
 
## Key takeaways
 
- The Australian dollar is the only genuine gold currency in this sample, and only since 2020. Gold now explains 63% of AUD's movement. The relationship holds even after stripping out the US dollar and global volatility, which points to a real terms-of-trade link rather than a statistical accident.
- The South African rand's gold-currency reputation does not survive scrutiny. Once prices are measured against a neutral currency and the broad dollar is controlled for, the rand's gold link disappears. ZAR trades on dollar strength and global risk appetite, not on gold.
- Much of the published commentary on gold currencies is distorted by the dollar effect. Gold is priced in US dollars, so charts drawn in dollar terms overstate the gold-FX relationship or even reverse its sign. The picture changes completely when everything is re-measured in yen.
- No long-run anchor ties any of these currencies to gold. Cointegration tests reject a stable equilibrium in every case. When gold and a currency drift apart, they can stay apart for years.
- The direction of causality reveals what a currency really is. Gold moves first for the producer currencies (AUD, CAD), while the risk currencies (ZAR, CHF) move first for gold. This makes a simple, repeatable classification test for any candidate currency.
- The relationship is only marginally tradable. An 11-year systematic backtest earns 4.5% on AUD and loses money on the other three currencies. The gold link is real, but it switches regimes too often for fixed trading rules.
---
 
## Summary assessment
 
| Currency | Gold link (full sample) | Gold link (2020-26) | Survives USD + VIX controls? | Classification |
|---|---|---|---|---|
| **AUD** | Weak (R² 0.11) | **Strong (R² 0.63)** | **Yes** (β 0.16, t 12.2) | Genuine gold currency, regime-dependent |
| **ZAR** | Wrong sign (β −0.37) | Positive but dollar-driven | **No** (β −0.15) | Dollar-beta / risk currency |
| **CAD** | Weak (R² 0.09) | Strong (R² 0.60) | Yes (β 0.11, t 5.2) | Minor gold currency |
| **CHF** | Strongest (R² 0.78) | Strongest (R² 0.86) | Yes (β 0.31, t 24.1) | Safe-haven twin, zero mining exposure |
 
*The CHF row is the cautionary tale here. The highest gold correlation in the sample belongs to a country with no gold mines. Correlation is not geology.*
 
---
 
## 1. Investment thesis
 
Market commentary routinely treats the Australian dollar and the South African rand as levered plays on the gold price, on the logic that gold makes up a large share of what these countries export. That claim gets repeated far more often than it gets tested. This project tests it.
 
Gold is an awkward fit for the standard commodity-currency framework because it is not only a commodity. It is also a quasi-monetary asset whose price responds to US real interest rates, broad dollar strength and safe-haven demand, the same global forces that drive commodity currencies in the first place. A naive correlation between gold and AUD therefore mixes up three very different channels:
 
1. **The income channel.** Higher gold prices improve an exporter's terms of trade. This is the channel the market narrative assumes.
2. **The denomination channel.** A weaker US dollar mechanically lifts the dollar price of gold and most dollar crosses at the same time.
3. **The common-factor channel.** Risk aversion and real rates push gold and currencies around together without any causal link between them.
The identification strategy here deals with both problems at once. Every price is re-denominated in Japanese yen, and the broad USD index and VIX enter the regressions as controls.
 
### Why these four currencies
 
The four currencies were not picked at random. Each one plays a specific role in the test design:
 
| Currency | Role | Rationale |
|---|---|---|
| **AUD** | Primary candidate | Australia is a top-three gold producer and gold sits among its largest export earners, with a freely floating currency. If any currency should follow gold, it is this one. |
| **ZAR** | Historic candidate | South Africa was the world's largest producer for most of a century, and the phrase "gold currency" was practically invented for the rand. Its mines have been declining for two decades, so it tests whether the label survives when the industry fades. |
| **CAD** | Control case | Canada mines plenty of gold but is a large, diversified exporter (oil, autos, metals). If CAD shows the same gold link as AUD despite gold being a small slice of its exports, the link is probably coming from something global rather than from mines. |
| **CHF** | Trap detector | Switzerland mines no gold at all, but the franc and gold are both safe havens that rise in anxious markets. If CHF shows a strong gold correlation anyway (it shows the strongest of the four), that proves a big correlation can exist with zero gold exports. |
 
Other large producers fail basic requirements for this kind of test. China consumes its own production and manages its currency. Russia is sanctioned. Uzbekistan and the West African producers run managed or pegged exchange rates, and a peg cannot transmit a gold signal. Peru and Ghana are workable and are flagged as the natural next extensions.
 
### Why yen as the measuring stick, not the dollar
 
Gold is priced in US dollars everywhere in the world. Test "does gold move the Aussie?" using AUD/USD and gold-in-USD and both series have the dollar inside them: when the dollar weakens, gold rises and AUD/USD rises at the same time, mechanically, even if Australia's gold exports did nothing. The test would find a gold link that is really a dollar link. Section 2 shows exactly this happening to the rand.
 
A clean test needs a neutral numeraire, meaning a currency that (a) is not the dollar, (b) floats freely with deep, liquid markets, and (c) belongs to an economy with no meaningful gold production and hence no gold story of its own. The yen satisfies all three, which is why every price in this report, including gold, is measured in yen, and why the backtest trades yen crosses like AUD/JPY. Results are cross-checked in dollar terms precisely to show how much the choice of measuring stick changes the answer. A natural robustness extension is re-running the pipeline with the euro as numeraire.
 
---
 
## 2. The dollar effect
 
Exhibit 1 is the single most important chart in this report. In dollar terms the rand appears strongly related to gold, though with a negative sign (β −0.57, R² 0.53). Re-priced in yen, the relationship largely dissolves into two unrelated trends: a rising gold price and a depreciating rand.
 
![Exhibit 1](preview/dollar_effect_zar.png)
*Exhibit 1: ZAR vs. gold, both priced in USD (left) and JPY (right). Normalized log levels.*
 
Any gold-FX analysis run purely in dollar terms inherits this distortion. It is probably the most common methodological error in published gold-currency commentary.
 
![Exhibit 2](preview/gold_vs_usd.png)
*Exhibit 2: Gold (USD/oz) vs. the broad USD index, 2006-2026. This inverse relationship sits underneath every dollar-denominated gold chart.*
 
---
 
## 3. Australian dollar: the genuine article, but only recently
 
The full-sample regression is unremarkable (β 0.07, R² 0.11). Splitting the sample changes the story entirely:
 
| Period | Gold β | Newey-West t | R² |
|---|---|---|---|
| 2005-2012 | −0.02 | −1.3 | 0.00 |
| 2013-2019 | −0.51 | −3.2 | 0.11 |
| **2020-2026** | **+0.23** | **11.0** | **0.63** |
 
AUD acquired its gold-currency status in the 2020s, the era of the bull market that took gold from $1,500 to above $5,000 and of record central-bank buying. The link also survives controls, which is the critical test: with broad USD and VIX included, gold retains β = 0.16 (t = 12.2). For AUD, gold is not just the dollar in disguise.
 
One caveat belongs next to the 63% figure. These are levels regressions on trending series, and Section 6 shows there is no cointegration between them, so the R² should be read as a description of how tightly the two prices moved in that era, not as evidence of a stable equilibrium. The Newey-West t-statistics and the fact that the result repeats across specifications are what carry the inference, not the R² itself.
 
![Exhibit 3](preview/subsample_beta.png)
*Exhibit 3: Gold elasticity by sub-period. Note the sign flips across eras for every currency.*
 
![Exhibit 4](preview/comovement.png)
*Exhibit 4: Each currency vs. gold in JPY terms, normalized log levels, 2005-2026.*
 
---
 
## 4. South African rand: title retired
 
The full sample in yen terms produces β of −0.37 (R² 0.50), which is the wrong sign for a gold currency. With controls, gold stays negative (−0.15) while the broad dollar absorbs the entire relationship (β −1.22). The rand trades as a dollar-beta and global-risk currency. The structural reason is well known: South African gold output has been declining for two decades, from world number one to outside the top five, while platinum-group metals, coal and above all global risk appetite now dominate the currency. The positive 2020-26 sub-sample (β 0.20) reflects the global regime rather than the mining sector, and the controls model makes that explicit.
 
---
 
## 5. Canadian dollar and Swiss franc: control and cautionary tale
 
**CAD (control).** Gold effects are small in the full sample (R² 0.09). With controls, however, the coefficient is positive and significant (β 0.11, t = 5.2), and the 2020-26 R² reaches 0.60. The loonie has actually been a better gold currency than the rand this decade, which was not the expected result.
 
**CHF (cautionary tale).** The franc posts the highest gold fit of all four currencies (full-sample R² 0.78, t = 24 with controls) despite having no domestic mining at all. This is the portfolio channel in its purest form: gold and the franc are the two classic safe-haven assets and trend together against everything else. Any exporter-based analysis that fails to control for this channel will misattribute safe-haven co-movement to trade fundamentals.
 
---
 
## 6. Econometrics: long run, causality, predictability
 
**Unit roots.** All log levels are I(1) and all returns are I(0) under ADF tests.
 
**Cointegration.** There is no long-run equilibrium anywhere in the sample. Engle-Granger rejects for all four currencies (AUD comes closest at p = 0.07; ZAR is nowhere at p = 0.88), and the Johansen trace test selects rank 0 in every {FX, gold, USD} system. Where error-correction terms can be estimated at all, half-lives run from 190 to 350 trading days, well outside any practical horizon.
 
**Granger causality (daily returns, 5 lags).** The results split cleanly in two:
 
| Direction | AUD | ZAR | CAD | CHF |
|---|---|---|---|---|
| Gold → currency | **p = 0.001** | 0.39 | **p = 0.011** | 0.39 |
| Currency → gold | 0.06 | **p = 0.004** | 0.27 | **p = 0.007** |
 
Gold leads the producer currencies. The risk currencies lead gold.
 
**Out-of-sample.** Using realized same-day gold returns, the gold model cuts forecast errors 9 to 12% below a random walk at daily frequency for all four currencies. This is contemporaneous explanatory power rather than an ex-ante trading signal, and the distinction matters.
 
![Exhibit 5](preview/rolling_r2.png)
*Exhibit 5: Rolling 250-day R² vs. gold. The relationship comes in episodes, sitting above the 70% threshold only 7 to 16% of the time, clustered in 2008-09, 2011-13 and 2022-26.*
 
---
 
## 7. Strategy backtest
 
The rule tested: a rolling 50-day regression of FX on gold (both in yen), trading only when the rolling R² is at least 50%, entering on a 2-sigma break in the direction of the break, and exiting after 10 days or at a 2% stop. The backtest runs from August 2014 (after a 50-day warm-up on data starting June 2014) through February 2026, before costs:
 
| Currency | Trades | Total return | Win rate | Assessment |
|---|---|---|---|---|
| **AUD** | 43 | **+4.5%** | 53% | Marginally positive. Peaks at +9.2% under tuned parameters, but the grid is sign-unstable |
| ZAR | 45 | −29.0% | 36% | Uninvestable |
| CAD | 40 | −5.0% | 53% | Negative |
| CHF | 45 | −8.9% | 44% | Negative |
 
![Exhibit 6](preview/aud_fit.png)
*Exhibit 6: AUD/JPY vs. the rolling gold-model fit with 2-sigma bands, 2022-2026.*
 
![Exhibit 7](preview/strategy_aud.png)
*Exhibit 7: AUD strategy equity curve. 43 trades, +4.5% cumulative.*
 
![Exhibit 8](preview/heatmap_aud.png)
*Exhibit 8: AUD total return across the holding-period and stop-level grid. Adjacent cells flip sign, which is the signature of a fragile edge.*
 
Three qualifications keep this result honest. First, the +9.2% peak comes from in-sample optimization: it is the best cell of a 16-parameter grid searched over the full backtest period, not an out-of-sample result. Second, returns are reported gross of costs, and at roughly 10bp of average profit per trade on AUD, realistic spread and slippage in AUD/JPY would consume much or all of the edge. Third, the figures are sums of per-trade log returns on unit positions rather than a compounded portfolio return, and no Sharpe ratio or drawdown statistics are claimed.
 
The strategy view that follows from this: the gold-FX relationship flips regimes too frequently for fixed-parameter systematic rules. Any real implementation would need a regime filter that only trades inside the high rolling-R² clusters, and even then return expectations should stay modest.
 
---
 
## 8. Risk factors and limitations
 
- No daily real-rate (TIPS) control was available in the free data used here, so real rates are addressed qualitatively.
- The broad USD index covers 2006 to December 2025. The daily gold fix in the mirror used ends February 2026.
- Smaller gold exporters (Peru, Ghana and others) are not yet covered and are natural extensions.
- Backtest results are gross of transaction costs, slippage and funding.
- Recent results are dominated by the 2020-26 regime, which may not persist. Regime identification is inherently backward-looking.
---
 
## Appendix A: Data
 
| Series | Source (mirror) | Range used |
|---|---|---|
| Gold PM fix, USD (daily) | LBMA via `forex-centuries` | 2005 to 2026-02 |
| Fed H.10 daily FX (local-per-USD) | `datasets/exchange-rates` | 2005 to 2026-02 |
| Broad USD index (DTWEXBGS) | FRED via `forex-centuries` | 2006 to 2025-12 |
| VIX daily close | CBOE via `datasets/finance-vix` | 2005 to 2026-02 |
| Gold monthly average | LBMA via `datasets/gold-prices` | context only |
 
Crosses are constructed as yen per unit of currency (AUDJPY = (JPY/USD)/(AUD/USD)), and gold in yen is the dollar fix times JPY/USD. All models use natural logs.
 
## Appendix B: Reproduce
 
```bash
pip install -r requirements.txt
python scripts/01_download_data.py   # shallow-clones public dataset mirrors
python scripts/02_build_panel.py     # builds data/processed/panel_daily.csv
python scripts/03_models.py          # writes results/model_results.json
python scripts/04_figures.py         # writes preview/*.png
python scripts/05_backtest.py        # writes results/backtest.json + figures
```
 
## Appendix C: Selected references
 
Sjaastad & Scacciavillani (1996); Baur & Lucey (2010); Pukthuanthong & Roll (2011); Apergis (2014); Capie, Mills & Wood (2005); Chen & Rogoff (2003); Meese & Rogoff (1983); O'Connor, Lucey, Batten & Baur (2015).
 
---
 
## About the author
 
**Written by Maitrayee Anand Vishnu**
 
MS Finance candidate, Stevens Institute of Technology · Ex-FP&A Associate, JPMorgan Chase (CIB)
 
[LinkedIn](https://www.linkedin.com/in/maitrayee-vishnu) · [Portfolio](https://maitrayee196.github.io/Maitrayee_Portfolio/) · [GitHub](https://github.com/maitrayee196)
 
Questions, feedback, or ideas for extending the model? Open an issue or reach out.
 
---
 
*This repository is an independent research project produced for educational purposes. It is not investment research, an offer, or a recommendation to buy or sell any security or currency. Past backtested performance is not indicative of future results.*
