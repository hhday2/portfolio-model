# Optimized Portfolio Model Design (Version 1 – Robust & High-ROI)

This document extends the project with a more detailed design for a robust investment pipeline. The goal is to screen U.S. equities and ETFs, score them using multiple factors and macro context, and output a diversified quarterly portfolio.

## 1. Universe Definition
- **Assets** – U.S.-listed stocks and ETFs only.
- **Minimum history** – Prefer 36 months daily price data (12 months required). Assets with less data are flagged.
- **ETF categories** – Equity, Bond, Commodity, and Real Estate ETFs.
- **Data quality controls** – Flag assets with more than 2% missing data or abnormal price jumps (>20% daily move). Exclude assets that fail quality checks.

## 2. Filters (Pre-Screening)
- **Market cap** – greater than $2B.
- **Liquidity** – Average daily volume above $1M (last 30 days).
- **Profitability / Earnings** –
  - Stocks must have positive trailing EPS or pass at least one of: ROE > 5% or free cash flow positive.
  - Exception: if a stock ranks in the top 10% by momentum and valuation it can remain, flagged for review.
- **Debt control** (optional) – Exclude if Net Debt/EBITDA > 4× when available.

## 3. Multi‑Factor Scoring System
Each factor is percentile ranked (winsorized at the 1st/99th percentiles) and combined with the following weights:

| Metric | Weight | Notes |
| --- | --- | --- |
| Sharpe Ratio (1‑yr, lagged 1 month) | 35% | Use a one‑month lag to avoid look‑ahead bias. |
| Volatility (3‑yr SD, winsorized) | 20% | Lower volatility is better; invert the rank. |
| Momentum (6‑month, lagged 1 month) | 20% | Uses a one‑month lag for backtest integrity. |
| Valuation (stocks: P/E or EV/EBITDA; ETFs: category mean) | 15% | ETFs default to the mean score of their category. |
| Macro Exposure Alignment | 10% | Default 50; raise to 75 for macro‑hedges, lower to 25 if misaligned. |

Missing data for any factor receives a neutral score of 50.

## 4. Selection Logic
- Select the top 20 assets by composite score.
- **Diversification constraints**
  - Max 3 stocks per sector.
  - ETFs must include at least one per category unless none score above 60; then include the next best above 50 and flag.
  - Equity exposure is capped at 50% of the portfolio.
- For each rebalance, log which constraints were hit, relaxed, or triggered exceptions.

## 5. Historical Lookback
- Volatility and macro trend calculations prefer a 3‑year lookback; use all available data otherwise.
- Sharpe and momentum use 6–12 months with a one‑month lag.
- In regimes where realized volatility exceeds 30% annualized, shorten the lookback to 18 months for these metrics.

## 6. Rebalancing & Turnover Management
- Rebalance quarterly with trigger overrides for weight drift (>20%), asset rank drop (below top 50), or composite score decline (>35%).
- Minimum holding period is one quarter unless the score drops more than 50% from entry.
- Transaction costs: $0.01/share plus 0.05% slippage on trades greater than 0.25% of portfolio weight.
- If a category has no qualifying assets, allow the next best score above 50 and flag.

## 7. Output Format
- Primary output is a CSV containing assets, weights, scores, flags, and a summary of constraints.
- Visuals include:
  - Sharpe vs. Volatility scatter plot.
  - Portfolio allocation pie chart.
  - Return and drawdown plots.
  - An attribution table of top and bottom contributors.
- Produce a configuration and constraint report listing all flags and exceptions each rebalance.

## 8. Additional Data Streams
- Macro indicators from FRED (10‑year yield, Fed Funds, CPI, VIX) define regimes such as rising rates or high inflation.
- Optional news sentiment using VADER or FinBERT headlines with a 7‑day average; if the sentiment is beyond ±0.5, adjust the macro score accordingly.
- Backtesting should use walk‑forward, out‑of‑sample windows with all factor signals lagged to avoid look‑ahead bias.

## Why This Version Is Robust & High‑ROI
- Data quality checks and liquidity screens prevent unreliable assets.
- Scoring logic is modular, transparent, and avoids over‑fitting.
- Macro and sentiment factors are rules‑based and reproducible.
- Turnover costs and constraint logging enable realistic performance evaluation.

Future improvements can include international stocks, dynamic sector caps, advanced optimization techniques, and integration with live trading APIs.
