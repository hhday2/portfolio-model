"""Simple portfolio construction using processed ETF data."""
import csv
from pathlib import Path
from typing import Dict, List

from .scoring import compute_sharpe, lagged_momentum
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

def score_tickers(price_hist: Dict[str, List[float]]) -> Dict[str, float]:
    cfg = load_settings().get("score_weights", {"sharpe": 0.6, "momentum": 0.4})
    w_sharpe = cfg.get("sharpe", 0.6)
    w_mom = cfg.get("momentum", 0.4)
    scores = {}
    for ticker, prices in price_hist.items():
        returns = [ (p2/p1) - 1 for p1, p2 in zip(prices[:-1], prices[1:]) ]
        sharpe = compute_sharpe(returns)
        try:
            mom = lagged_momentum(prices)
        except ValueError:
            mom = 0.0
        composite = w_sharpe * sharpe + w_mom * mom
        scores[ticker] = composite
    return scores

def build_portfolio(n: int = 5) -> Dict[str, float]:
    data_path = BASE / "data" / "processed" / "etf_master.csv"
    price_hist = load_prices(data_path)
    scores = score_tickers(price_hist)
    top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:n]
    if not top:
        return {}
    weight = 1 / len(top)
    return {t: weight for t, _ in top}

if __name__ == "__main__":
    pf = build_portfolio()
    for t, w in pf.items():
        print(f"{t}: {w:.2%}")
