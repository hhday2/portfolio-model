# Portfolio Model Build Plan

## Enhanced 4-Week Portfolio Model Build Plan

### Week 1: Environment & Data Pipeline (6–7 hrs)
**Goals:** Get your dev environment wired up, ingest & clean Top 100 tickers (not 550), validate data quality.

1. **Setup & Boilerplate**
   - Create virtualenv/conda env; install yfinance, pandas, numpy, matplotlib
   - Scaffold project repo with README.md, folder structure, requirements.txt
   - Initialize Git repo with .gitignore for Python/data files

2. **Data Ingestion Module**
   - Fetch price & fundamentals for Top 100 US stocks + 20 ETFs
   - Implement CSV cache + update-tracking
   - Basic dividend/split adjustment check (yfinance handles this automatically)

3. **Quality Controls**
   - Outlier detection & missing-data flags (use `quality_score` stub)
   - Write simple unit tests (e.g. assert no >10% nulls, price jumps flagged)

### Week 2: Core Scoring Engine (6–7 hrs)
**Goals:** Build composite score for Sharpe Ratio & Momentum only; get percentile ranking solid.

1. **Sharpe Ratio Factor**
   - Compute 1-year Sharpe for each ticker; winsorize outliers
   - Percentile-rank into 0–100 scale

2. **Momentum Factor**
   - Compute 6-month return; winsorize & percentile-rank

3. **Factor Analysis**
   - Simple correlation check between Sharpe and Momentum factors
   - Cross-correlation matrix for selected assets
   - Document correlation findings in comments

4. **Composite Score**
   - Hard-code weights: 60% Sharpe, 40% Momentum
   - Verify lag handling (1-month look-ahead bias control)

5. **Smoke Tests**
   - Quick sanity checks (top/bottom tickers) & basic backtest stub

### Week 3: Portfolio Construction & Backtest (6 hrs)
**Goals:** Nail down selection logic in pandas; automate one quarter of backtest.

1. **Selection Logic**
   - Pick top 15 by score, enforce ≤3/ticker-sector & ≥2 ETFs
   - Equal-weight calculation & turnover control (hold ≥1 quarter)
   - Simple portfolio volatility target: reject if projected vol > 25% annualized

2. **Backtest Loop**
   - Simulate 4 quarters: generate portfolio each rebalance, track returns
   - Track transaction costs even if simplified (assume 0.1% per trade)
   - Compute basic metrics: cumulative return, sharpe, max drawdown

3. **Basic Risk Check**
   - Validate portfolio volatility < target threshold

### Week 4: Analytics, Visualization & Polish (6 hrs)
**Goals:** Deliver 3–4 polished charts, write README + short write-up, prep for demo.

1. **Static Charts (matplotlib)**
   - Allocation pie chart on initial portfolio
   - Cumulative returns vs. SPY
   - Drawdown plot
   - Factor attribution table (print to console or CSV)
   - Simple performance attribution: which assets contributed most to returns

2. **Interactive Element (Optional)**
   - Consider one interactive element if time permits – simple parameter slider for Sharpe/Momentum weights using matplotlib widgets

3. **Documentation & Write-up**
   - Flesh out README.md: setup, usage, key design choices, "next steps"
   - Draft 1-page summary (MD or slide): project overview, high-level results, lessons learned
   - Add scaling notes: how to extend to larger universes, international assets

4. **Buffer & Review**
   - Code cleanup, add docstrings, final QC

### Why This Enhanced Plan Works
- **Data Engineering:** systematic data quality framework with automated outlier detection and unit tests.
- **Quantitative Finance:** factor correlations and bias controls to prevent look-ahead issues.
- **Business Acumen:** incorporate realistic transaction costs and turnover constraints.
- **Technical Leadership:** interactive tool for parameter sensitivity analysis.

### Success Metrics
- **Functional:** Automated quarterly portfolio generation
- **Performance:** Clear benchmark comparison with SPY
- **Technical:** Sub-2 second execution, > 95% data quality
- **Professional:** Interview-ready documentation and presentation
