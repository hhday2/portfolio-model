"""Simple portfolio construction using processed ETF data."""
import csv
from pathlib import Path
from typing import Dict, List, Tuple

from .scoring import compute_sharpe, lagged_momentum, compute_volatility
from .utils import load_settings

BASE = Path(__file__).parent.parent

def load_prices(path: Path) -> Dict[str, List[float]]:
    """Load close prices from processed CSV grouped by ticker."""
    data: Dict[str, List[float]] = {}
    with path.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            t = row["ticker"].upper()
            data.setdefault(t, []).append(float(row["Close"]))
    return data

def load_prices_and_meta(path: Path) -> Tuple[Dict[str, List[float]], Dict[str, str]]:
    """Return price history and broad category for each ticker."""
    prices: Dict[str, List[float]] = {}
    cats: Dict[str, str] = {}
    with path.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            t = row["ticker"].upper()
            prices.setdefault(t, []).append(float(row["Close"]))
            cats[t] = row.get("broad_cat", "Unknown")
    return prices, cats

def score_tickers(price_hist: Dict[str, List[float]]) -> Dict[str, float]:
    """Compute composite scores using Sharpe, Momentum and Volatility."""
    cfg = load_settings().get(
        "score_weights",
        {"sharpe": 0.5, "momentum": 0.3, "volatility": 0.2},
    )
    w_sharpe = cfg.get("sharpe", 0.5)
    w_mom = cfg.get("momentum", 0.3)
    w_vol = cfg.get("volatility", 0.2)

    scores = {}
    for ticker, prices in price_hist.items():
        returns = [(p2 / p1) - 1 for p1, p2 in zip(prices[:-1], prices[1:])]
        sharpe = compute_sharpe(returns)
        vol = compute_volatility(returns)
        try:
            mom = lagged_momentum(prices)
        except ValueError:
            mom = 0.0
        # lower volatility is better so invert the ranking sign
        composite = w_sharpe * sharpe + w_mom * mom - w_vol * vol
        scores[ticker] = composite
    return scores

def build_portfolio(n: int = 5) -> Dict[str, float]:
    """Select top ``n`` tickers ensuring category diversification."""
    data_path = BASE / "data" / "processed" / "etf_master.csv"
    price_hist, cats = load_prices_and_meta(data_path)

    scores = score_tickers(price_hist)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

    required_cats = {"Equity", "Fixed Income", "Commodity", "Real Estate"}
    selected: Dict[str, str] = {}

    # First pass: ensure one per category if available
    for ticker, _ in ranked:
        cat = cats.get(ticker, "Other")
        if cat in required_cats and cat not in selected:
            selected[ticker] = cat
        if len(selected) == len(required_cats) or len(selected) == n:
            break

    # Fill remaining slots with best remaining tickers
    for ticker, _ in ranked:
        if len(selected) >= n:
            break
        if ticker not in selected:
            selected[ticker] = cats.get(ticker, "Other")

    if not selected:
        return {}
    weight = 1 / len(selected)
    return {t: weight for t in selected}

if __name__ == "__main__":
    pf = build_portfolio()
    for t, w in pf.items():
        print(f"{t}: {w:.2%}")
