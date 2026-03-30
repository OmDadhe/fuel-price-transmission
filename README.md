# Fuel Price Transmission Effect: India 2019-2025

How Delhi petrol and diesel price shocks propagate through inflation, logistics costs, and consumer spending across 70 months of multi-source government data.

Author: Om Dadhe | BTech CSE |
[LinkedIn](https://linkedin.com/in/contactom) | [GitHub](https://github.com/OmDadhe) | [Portfolio](https://om-dadhe-portfolio.vercel.app)

---

## The Business Question

When petrol prices spike in Delhi, what actually happens to India's inflation, logistics costs, and consumer discretionary spending — and how fast?

This is a live question every FMCG company, logistics startup, and D2C brand in India models internally before making pricing decisions. This project answers it with 70 months of multi-source data across 5 integrated datasets and 6 econometric models.

---

## Key Performance Indicators

| Metric | Value |
|--------|-------|
| Petrol RSP change (FY2019-20 to FY2024-25) | +30.3% |
| Diesel RSP change (FY2019-20 to FY2024-25) | +33.2% |
| Brent vs Petrol RSP correlation | r = 0.694 |
| CPI transmission lag (CCF peak) | 3 months |
| Q1/Q5 regressive burden ratio | 2.8x |
| Rupee depreciation over study period | +24.3% |

---

## Key Findings

**Finding 1 — Administered Pricing Is Real and Quantifiable**
The Brent-to-Delhi-petrol correlation stands at r = 0.694, substantially below what a fully market-linked system would produce. Excise adjustments act as a policy shock absorber — and sometimes amplifier — keeping retail prices in flat bands by policy regime rather than tracking global crude.

**Finding 2 — COVID: The Government Captured the Crude Crash**
In April 2020, Brent hit $26.57 per barrel, its lowest since 2002. Rather than passing the benefit to consumers, the government raised central excise on petrol by Rs.13/litre and diesel by Rs.13/litre in May 2020. The estimated additional fiscal revenue over the 18-month high-excise period exceeds Rs.2.5 lakh crore.

**Finding 3 — The Burden Is Deeply Regressive**
A Rs.10/litre fuel hike erodes 6.7% of a Q1 household's monthly income but only 0.5% of a Q5 household's. The Q1/Q5 regressive burden ratio is 2.8x overall, but a Rs.10 hike represents a 13x larger proportional shock for the bottom quintile compared to the top. Auto drivers — diesel-dependent livelihoods — are hardest hit in absolute income-share terms.

**Finding 4 — Diesel Users Bore More of the Russia-Ukraine Shock**
Between FY2021-22 and FY2022-23, petrol RSP changed by Rs.-0.15 while diesel rose Rs.+3.16. The freight network, not private commuters, absorbed the commodity supply shock, transmitting directly into logistics costs and food inflation.

**Finding 5 — CPI Lags Brent by Approximately 3 Months**
The cross-correlation function between differenced Brent and differenced CPI peaks at lag 3, confirming a roughly 3-month transmission window from global crude to Indian consumer prices. Granger causality is structurally weak because excise policy intervenes in the channel — the regime-switching OLS makes this regime-dependence explicit.

**Finding 6 — Regime-Switching Changes the Pass-Through Estimate**
Estimating crude-to-CPI elasticity separately per policy regime reveals that the COVID-excise period and the Russia-Ukraine war shock produced structurally different pass-through dynamics. A pooled OLS average masks this heterogeneity entirely.

---

## Model Summary

| Model | Method | Key Output | Result |
|-------|--------|------------|--------|
| Model 1 | OLS Price Decomposition | R-squared on RSP | 0.8523 |
| Model 2 | Granger Causality (pure NumPy) | CCF peak lag | 3 months |
| Model 3 | VAR(p) with Impulse Response Functions | AIC-selected lag | p = 1 |
| Model 4a | ARIMA(1,1,0) | FY25-26 petrol forecast | Rs.96.16/L |
| Model 4b | Ridge Regression (lambda = 0.5) | Held-out 6-month RMSE | 1.098 |
| Model 5 | Regime-Switching OLS | Q1/Q5 burden ratio | 2.8x |

---

## What Is New and Why It Matters

Three models were added in the current version, each addressing a specific gap in the original analysis.

**VAR(p) with Impulse Response Functions**
The ARIMA forecast treated petrol RSP as a univariate series. The VAR model jointly estimates Brent, CPI, and RSP as an endogenous system, then simulates the dynamic response of each variable to a one-standard-deviation shock in crude prices over a 14-month horizon. Lag order is selected by AIC. Identification follows a Cholesky decomposition, and confidence bands are bootstrapped at 68%. This is the only model in the project that shows propagation dynamics over time rather than a static elasticity estimate. Implemented entirely in NumPy matrix algebra — no statsmodels dependency.

**Ridge Regression with Head-to-Head Benchmark**
Adding regularization addresses the collinearity problem that arises when lagged Brent, excise policy indicators, and USD/INR are used as simultaneous predictors. The Ridge model (lambda = 0.5) is evaluated against ARIMA on a held-out 6-month window with RMSE, MAE, and MAPE all printed side by side. This makes the forecast comparison explicit and reproducible, rather than relying on in-sample fit alone.

**Regime-Switching OLS**
Estimating a single crude-to-CPI elasticity over the full 2019-2025 period conflates three structurally distinct policy regimes: pre-COVID market-tracking, COVID-era excise maximisation, and the Russia-Ukraine supply shock period. The regime-switching OLS estimates a separate elasticity for each regime using policy event dates as breakpoints. The result confirms that pass-through coefficients differ significantly across regimes — a finding that changes the interpretation of every aggregate correlation in the project.

---

## Analyses and Outputs

| Output | Description |
|--------|-------------|
| model1_ols_decomposition.png | Waterfall decomposition of the 6-year RSP change into Brent, excise, FX, and margin components |
| model2_granger_causality.png | CCF plot + Granger F-statistics across lags 1-6 |
| model3_var_irf.png | Impulse response functions with bootstrapped 68% confidence bands over 14 months |
| model4_forecast_comparison.png | ARIMA vs Ridge head-to-head on held-out window with scenario overlays |
| model5_regime_elasticity.png | Regime-specific pass-through coefficients across three policy periods |
| eda_01_distributions.png | KDE and box plots for all five primary series |
| eda_02_correlation.png | Pairwise scatter matrix with regression overlays |
| eda_03_calendar_heatmaps.png | Fiscal-year calendar heatmaps for Brent, CPI momentum, and excise regime |
| eda_04_boxplots_rolling.png | Rolling volatility and momentum signals by series |
| consumer_impact_simulator.png | Regressive impact curve across five income quintiles under Rs.10/litre shock |
| kpi_summary.csv | Single-row KPI export (project-level metrics) |
| master_dataset.csv | Merged 70-row master dataset (15 columns) |

---

## Data Sources

| Dataset | Source | Frequency |
|---------|--------|-----------|
| Delhi Petrol and Diesel RSP | data.gov.in (Parliament Q&A) | Annual FY |
| All-India CPI (Base 2012 = 100) | MOSPI / RBI Press Release | Monthly |
| Brent Crude Oil Price | EIA via FRED (DCOILBRENTEU) | Monthly |
| USD/INR Exchange Rate | FRED (DEXINUS) | Monthly |
| Central Excise Duty History | data.gov.in (Parliament Q&A) | Event-based |

All sources are publicly available and government-sourced.

---

## Methodology

### Data Pipeline

Raw CSVs and XLSX files are loaded into pandas, merged using merge_asof on excise policy event dates, and consolidated into a 70-row monthly master dataset with 15 columns. Derived metrics include year-on-year and month-on-month changes, Brent price converted to INR per litre, and excise share as a percentage of pump price.

### Analytical Techniques

**OLS Price Decomposition**
Decomposes the observed RSP change from FY2019-20 to FY2024-25 into named cost drivers: Brent price movement (INR-converted), central excise changes, state VAT passthrough, refinery and dealer margins. R-squared of 0.8523 on RSP.

**Granger Causality and Cross-Correlation**
Tests whether lagged Brent changes statistically predict CPI changes using an OLS-based F-test on restricted versus unrestricted VAR models. Built from direct NumPy matrix algebra. Cross-correlation on first-differenced (ADF-confirmed stationary) series identifies the 3-month transmission peak.

**VAR(p) with Impulse Response Functions**
A vector autoregression estimated jointly on Brent, USD/INR, petrol RSP, and CPI. Lag length chosen by AIC (p = 1 selected). Cholesky decomposition identifies the structural shock ordering. Bootstrapped 68% bands show the uncertainty envelope on the 14-month IRF.

**ARIMA(1,1,0) and Ridge Regression Comparison**
ARIMA fits an AR(1) model on the differenced RSP series with 80% confidence intervals from OLS residual standard error. Ridge regression uses lagged Brent, excise indicators, and FX as predictors with L2 regularization (lambda = 0.5). Both are evaluated on a held-out 6-month window. RMSE, MAE, and MAPE are printed for direct comparison.

**Regime-Switching OLS**
Policy regime breakpoints are defined from excise event history. Separate OLS regressions estimate the crude-to-CPI beta for each regime. Coefficient differences across regimes are reported, demonstrating that COVID-era pass-through was structurally different from the war-shock period.

**Regressive Impact Analysis**
Five income quintile personas are constructed from NSSO consumption survey patterns. Fuel burden is computed as (monthly litres times price) divided by monthly income. A Rs.10/litre shock is simulated across all quintiles to produce the regressivity curve.

---

## Project Structure

```
fuel-price-transmission/
|
|-- data/
|   |-- raw_rsp.csv
|   |-- DEXINUS.csv
|   |-- Annexures_for_Press_Release_...xlsx
|   `-- cpi_1109.xlsx
|
|-- outputs/
|   |-- master_dataset.csv
|   |-- kpi_summary.csv
|   |-- consumer_impact_simulator.png
|   |-- report/
|   |   `-- analysis_report.html
|   |-- models/
|   |   |-- model1_ols_decomposition.png
|   |   |-- model2_granger_causality.png
|   |   |-- model3_var_irf.png
|   |   |-- model4_forecast_comparison.png
|   |   `-- model5_regime_elasticity.png
|   `-- eda/
|       |-- eda_01_distributions.png
|       |-- eda_02_correlation.png
|       |-- eda_03_calendar_heatmaps.png
|       `-- eda_04_boxplots_rolling.png
|
|-- fuel_price_transmission_analysis.py
|-- streamlit_app.py
|-- requirements.txt
`-- README.md
```

---

## How to Run

**Clone and install**
```bash
git clone https://github.com/OmDadhe/fuel-price-transmission
cd fuel-price-transmission
pip install -r requirements.txt
```

**Run analysis (generates all outputs and master CSV)**
```bash
python fuel_price_transmission_analysis.py
```

**Launch Streamlit dashboard**
```bash
streamlit run streamlit_app.py
```

---

## Business Applications

This type of analysis is used by FMCG companies modelling freight cost increases into product margin projections, logistics startups hedging and setting contract prices when fuel is volatile, D2C brands running scenario planning for last-mile delivery costs under crude shocks, investment analysts modelling downstream impact of oil price moves on India consumption stories, and policy researchers assessing excise duty incidence across income groups.

---

## License

MIT — use freely with attribution.
