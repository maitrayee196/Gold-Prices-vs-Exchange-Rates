# GOLD MONEY
### Global FX & Commodities Research

**When do gold prices matter for exchange rates? Evidence from 21 years of daily data**

| | |
|---|---|
| **Research by** | Maitrayee Anand Vishnu |
| **Date** | July 2026 |
| **Asset classes** | Gold (XAU), G10 & EM FX |
| **Coverage** | AUD, ZAR, CAD, CHF vs. gold (JPY, EUR, CHF and basket numeraires) |
| **Sample** | Daily, 4 Jan 2005 to 25 Feb 2026 (5,146 obs.) |

**Full research report:** [paper/Gold-Prices-vs-Exchange-Rate_Maitrayee_Anand_Vishnu.pdf](paper/Gold-Prices-vs-Exchange-Rate_Maitrayee_Anand_Vishnu.pdf)

---

## Key takeaways

- The most robust finding in this project: since 2020, daily gold returns and Australian dollar returns move together positively and significantly in every measuring currency tested (yen, euro, franc, and a four-currency basket), and gold keeps its explanatory power after dollar and volatility controls in three of the four. No other currency here passes that test.
- The often-quoted headline that gold accounts for 63% of the variation in AUD is the fragile way to state it. That number comes from price levels measured in yen, and part of it reflects the yen's own weakness in 2022-24 rather than gold. In euro or basket terms the levels relationship fades or flips sign, while the returns relationship survives everywhere. Levels flatter the story; returns carry it.
- The South African rand fails in every numeraire. With dollar and volatility controls, the rand's gold coefficient is negative in all four measuring currencies. Its gold-currency reputation does not survive any specification tested here.
- Formal structural-break tests do not choose 2020. A Quandt-Andrews search over all candidate dates puts the dominant break for AUD in September 2008 (levels) and May 2011 (returns). The "2020s gold decade" split used in the tables is descriptive, not statistically identified, and is labeled as such.
- Nothing ties any currency to gold in the long run. Cointegration tests reject a stable equilibrium in every case; divergences can persist for years.
- The relationship is not investable as a fixed rule. The AUD strategy earns 4.5% before costs over 11.5 years, a Sharpe ratio of 0.10 with a 9.9% maximum drawdown, and realistic costs would consume most of the remainder.

---

## Summary assessment

| Currency | Levels link, 2020-26 (JPY) | Returns link, 2020-26 (all numeraires) | Survives controls? | Classification |
|---|---|---|---|---|
| **AUD** | Strong (R² 0.63) | **Positive, significant in all four** | **Yes, in 3 of 4 numeraires** | Gold-linked producer currency, regime-dependent |
| **ZAR** | Strong (R² 0.56) | Positive (common global factor) | **No, negative in all four** | Dollar-beta / risk currency |
| **CAD** | Strong (R² 0.60) | Positive | Yes (JPY: β 0.11, t 5.2) | Minor gold-linked producer |
| **CHF** | Strongest (R² 0.86) | Positive | Yes (JPY terms) | Safe-haven co-mover, zero mining exposure |

*The CHF row remains the cautionary tale: the strongest raw correlation belongs to a country with no gold mines. Correlation is not geology.*

---

## Positioning in the literature

The building blocks here are well established: Chen and Rogoff (2003) established the commodity-currency framework; Sjaastad and Scacciavillani (1996) connected gold to exchange rates; Apergis (2014) examined gold and the Australian dollar specifically; Erb and Harvey (2013) documented gold's broader and often misunderstood investment roles. What this project adds relative to that work: it prices gold and currencies in several non-dollar numeraires to strip out the mechanical USD denomination effect and show how much of the published relationship depends on that choice; it applies rolling-regime and formal structural-break analysis rather than assuming a stable relationship; and it closes the loop with a trading evaluation, so statistical significance is tested against economic significance.

---

## 1. Research design

Market commentary routinely treats the Australian dollar and the South African rand as levered plays on the gold price, on the logic that gold makes up a large share of what these countries export. That claim gets repeated far more often than it gets tested. This project tests it.

Gold is an awkward fit for the standard commodity-currency framework because it is not only a commodity. It is also a quasi-monetary asset whose price responds to US real interest rates, broad dollar strength and safe-haven demand, the same global forces that drive commodity currencies in the first place. A naive correlation between gold and AUD therefore mixes up three very different channels:

1. **The income channel.** Higher gold prices improve an exporter's terms of trade. This is the channel the market narrative assumes.
2. **The denomination channel.** A weaker US dollar mechanically lifts the dollar price of gold and most dollar crosses at the same time.
3. **The common-factor channel.** Risk aversion and real rates push gold and currencies around together without any causal link between them.

### Why these four currencies

| Currency | Role | Rationale |
|---|---|---|
| **AUD** | Primary candidate | Australia is a top-three gold producer, gold is among its biggest exports, and the currency floats freely. If any currency should follow gold, it is this one. |
| **ZAR** | Historic candidate | South Africa was the world's largest producer for most of a century, but its mines have been shrinking for twenty years. It tests whether the label survives when the industry fades. |
| **CAD** | Control case | Canada mines plenty of gold but is a big, diversified exporter (oil, autos, metals). If CAD shows the same gold link as AUD, the link is probably global, not mining-related. |
| **CHF** | Look-alike detector | Switzerland mines no gold, but the franc and gold both attract safe-haven flows. A strong gold correlation here shows how large the look-alike effect can be. |

Other large producers fail basic requirements: China consumes its own production and manages its currency; Russia is sanctioned; Uzbekistan and the large West African producers run managed or pegged rates, and a peg cannot transmit a gold signal. Peru and Ghana are workable candidates flagged as extensions.

### The numeraire problem, stated honestly

Gold is priced in US dollars, so testing AUD/USD against gold-in-USD embeds the dollar in both series and manufactures correlation. The main text therefore measures everything in Japanese yen: Japan mines almost no gold, and the yen is deep and free-floating. But the yen is not perfectly neutral either. It has its own drivers, including Bank of Japan policy, carry trades and safe-haven flows, and it was one of the weakest major currencies in 2022-24. Pricing in yen substantially reduces the embedded USD mechanical correlation; it does not eliminate numeraire effects. For that reason, every key result is re-estimated with the euro, the Swiss franc, and an equal-weight USD/EUR/JPY/GBP basket as alternative measuring sticks (Section 4), and conclusions are drawn only from what survives across them.

---

## 2. The dollar effect

In USD terms the rand looks strongly (negatively) related to gold; re-priced in yen, most of that relationship is revealed as two long trends passing each other. In USD terms, the full-sample log-log regression gives β −0.57 with R² 0.53, the opposite sign of the gold-currency story.

![alt text](preview/dollar_effect_zar.png)

![alt text](preview/gold_vs_usd.png)

---

## 3. Headline results by era (descriptive)

The sub-period table below uses hand-chosen splits and price levels, so treat it as description, not inference. It shows how completely the apparent relationship changes across eras. (The formal break analysis is in Section 4.)

| Period | AUD gold β | t | R² |
|---|---|---|---|
| 2005-2012 | −0.02 | −1.3 | 0.00 |
| 2013-2019 | −0.51 | −3.2 | 0.11 |
| 2020-2026 | +0.23 | 11.0 | 0.63 |

Gold accounts for 63% of the variation in AUD (in yen terms) during 2020-26. But these are levels regressions on trending, non-stationary series with no cointegration behind them, so the R² describes co-trending in that era rather than an equilibrium. The inference rests on the robust t-statistics, the returns-based results, and the multi-numeraire checks below.

With the broad dollar index and VIX as controls (2006-2025, yen terms), the gold coefficient is: AUD +0.16 (t 12.2), CAD +0.11 (t 5.2), CHF +0.31 (t 24.1), ZAR −0.15 (t −3.3). The rand's gold link is absorbed entirely by the dollar (dollar β −1.22).

![alt text](preview/subsample_beta.png)

![alt text](preview/comovement.png)

---

## 4. Robustness: numeraires and formal break tests

**Numeraire robustness.** The key AUD and ZAR results re-estimated in four measuring currencies:

| AUD vs gold | JPY | EUR | CHF | Basket |
|---|---|---|---|---|
| Levels β, 2020-26 | +0.23 (t 11.0) | −0.11 (t −7.2) | −0.32 (t −11.4) | −0.08 (t −2.7) |
| **Returns β, 2020-26** | **+0.25 (t 7.9)** | **+0.10 (t 6.0)** | **+0.12 (t 5.2)** | **+0.43 (t 13.8)** |
| Controls β (full sample) | +0.16 (t 12.2) | +0.14 (t 7.7) | −0.17 (t −9.8) | +0.13 (t 8.9) |

Read the first row and the second row together and the lesson is clear. The levels relationship is numeraire-dependent: it is strongly positive only in yen, partly because the weak yen of 2022-24 trended both AUD/JPY and gold/JPY upward together. The **returns** relationship is positive and statistically significant in every numeraire, and the controls result holds in three of four (the CHF-numeraire exception is expected, since measuring against the franc subtracts the safe-haven factor that gold shares). The defensible claim is therefore about returns: day to day, gold and AUD genuinely move together in this era, whatever you measure them in.

| ZAR vs gold, controls β | JPY | EUR | CHF | Basket |
|---|---|---|---|---|
| Gold coefficient | −0.15 | −0.22 | −0.59 | −0.24 |

ZAR's verdict needs no nuance: negative in every numeraire. The rand is not a gold currency in any specification tested.

**Formal break tests.** A Quandt-Andrews sup-F search over all candidate break dates (15% trimming) does not select 2020. For AUD the dominant single break is September 2008 in levels and May 2011 in returns; ZAR breaks in late 2015 (levels), CHF in April 2013. Two honest conclusions follow: the relationship is unstable everywhere (the sup-F statistics are enormous), and the 2020 split used in Section 3 is a readable description of the recent era, not a statistically identified regime date. A multi-break Bai-Perron analysis is the natural next step.

---

## 5. Information flow and the long run

**No long-run anchor.** Engle-Granger rejects cointegration for all four currencies (AUD closest, p = 0.07; ZAR p = 0.88); Johansen selects rank 0 in every {FX, gold, broad USD} system. Where error-correction terms can be estimated at all, half-lives run 190-350 trading days.

**Predictive information (Granger tests).** These tests ask whether yesterday's gold returns contain statistically useful information for forecasting today's currency returns, and the reverse. They establish predictive content, not economic causation. P-values shown are the smallest across the five lags tested, which slightly flatters borderline results.

| Direction | AUD | ZAR | CAD | CHF |
|---|---|---|---|---|
| Gold → currency | **0.001** | 0.39 | **0.011** | 0.39 |
| Currency → gold | 0.06 | **0.004** | 0.27 | **0.007** |

Gold carries forecasting information for the producer currencies (AUD, CAD); the risk-sensitive currencies (ZAR, CHF) carry forecasting information for gold. The direction of predictive content itself classifies the currency type.

**Out-of-sample fit.** Using realized same-day gold returns, a gold model reduces forecast error (mean squared error) by 9-12% versus a random walk at daily frequency for all four currencies. This is contemporaneous explanatory power, not an ex-ante trading signal.

![alt text](preview/rolling_r2.png)

The rolling chart is the honest summary: the link is episodic, above the 70% line only 7-16% of the time, in clusters (2008-09, 2011-13, 2022-26).

---

## 6. Trading strategy

Momentum-on-model-break rule: rolling 50-day regression of FX on gold (both in JPY); trade only when rolling R² ≥ 50%; enter on a ±2σ break; exit after 10 days or a 2% stop. Backtest August 2014 (after a 50-day warm-up on data starting June 2014) to February 2026, before costs:

| Currency | Trades | Total return | Win rate |
|---|---|---|---|
| AUD | 43 | **+4.5%** | 53% |
| ZAR | 45 | −29.0% | 36% |
| CAD | 40 | −5.0% | 53% |
| CHF | 45 | −8.9% | 44% |

Institutional risk metrics for the AUD strategy, computed from the daily P&L series: annualized return 0.4%, annualized volatility 3.9%, **Sharpe ratio 0.10**, maximum drawdown −9.9% over 11.5 years. Stated plainly: not investable as a fixed rule.

![alt text](preview/aud_fit.png)
![alt text](preview/strategy_aud.png)
![alt text](preview/heatmap_aud.png)

Three qualifications: the tuned +9.2% grid peak is in-sample optimization; returns are gross of costs, and at roughly 10bp average profit per trade, spreads and slippage in AUD/JPY would consume much of the edge; figures are sums of per-trade log returns, not compounded portfolio returns. Any real implementation would need a regime filter (trade only inside the high rolling-R² clusters) and walk-forward validation, which is future work.

---

## 7. Discussion

1. **The robust claim is about returns, not levels.** Gold and AUD returns co-move positively in every numeraire since 2020; the dramatic levels statistics are partly a yen artifact. State the modest version and it survives review; state the flashy version and it does not.
2. **"Gold currency" is a regime, not an identity.** And formal tests date the big instabilities to 2008-2013, not to a clean 2020 switch.
3. **The dollar effect is the great illusion-maker,** and the numeraire table quantifies exactly how much.
4. **The direction of predictive content classifies currencies:** gold informs producer currencies; risk currencies inform gold.
5. **CHF's high correlation reflects shared safe-haven demand, SNB policy and European financial conditions,** not gold exposure — the standing warning against reading correlation as geology.

## Limitations

- Controls are limited to the broad dollar and VIX. Interest-rate differentials, terms of trade, oil (especially for CAD), inflation surprises and current-account dynamics are omitted; some of the estimated gold effect may proxy for these.
- No daily real-rate (TIPS) series was available in the free data used.
- Break analysis is single-break (Quandt-Andrews); multi-break Bai-Perron is future work, as are Peru and Ghana, walk-forward strategy validation, and an SDR numeraire.
- Broad dollar index covers 2006 to Dec 2025; the daily gold fix mirror ends Feb 2026.
- Data mirrors update daily: to reproduce the exact numbers here, use the frozen files in `data/raw` rather than re-running the downloader.

---

## Reproduce

```bash
pip install -r requirements.txt
# To reproduce the exact numbers in this README, skip 01 and use the frozen data/raw files.
python scripts/01_download_data.py   # optional: pulls latest data (numbers will drift)
python scripts/02_build_panel.py     # builds data/processed/panel_daily.csv
python scripts/03_models.py          # writes results/model_results.json
python scripts/04_figures.py         # writes preview/*.png
python scripts/05_backtest.py        # writes results/backtest.json + figures
python scripts/07_robustness.py      # numeraire robustness, break tests, risk metrics
```

## Further reading

1. Chen Y, Rogoff K (2003), *Commodity Currencies.*
2. Sjaastad L, Scacciavillani F (1996), *The Price of Gold and the Exchange Rate.*
3. Apergis N (2014), *Can Gold Prices Forecast the Australian Dollar Movements?*
4. Erb C, Harvey C (2013), *The Golden Dilemma.*
5. Baur D, Lucey B (2010), *Is Gold a Hedge or a Safe Haven?*
6. Pukthuanthong K, Roll R (2011), *Gold and the Dollar (and the Euro, Pound, and Yen).*
7. Capie F, Mills T, Wood G (2005), *Gold as a Hedge Against the Dollar.*
8. Meese R, Rogoff K (1983), *Empirical Exchange Rate Models of the Seventies.*
9. O'Connor F, Lucey B, Batten J, Baur D (2015), *The Financial Economics of Gold — A Survey.*

---

## About the author

**Written by Maitrayee Anand Vishnu**

MS Finance candidate, Stevens Institute of Technology · Ex-FP&A Associate, JPMorgan Chase (CIB)

[LinkedIn](https://www.linkedin.com/in/maitrayee-vishnu) · [Portfolio](https://maitrayee196.github.io/Maitrayee_Portfolio/) · [GitHub](https://github.com/maitrayee196)

Questions, feedback, or ideas for extending the model? Open an issue or reach out.

---

*This repository is an independent research project produced for educational purposes. It is not investment research, an offer, or a recommendation to buy or sell any security or currency. Past backtested performance is not indicative of future results.*
