"""Scoring utilities for ETFs and stocks.

These functions avoid heavy dependencies so that tests
run in minimal environments.
"""
import math
import statistics as st
from typing import List

def compute_sharpe(returns: List[float], risk_free: float = 0.0) -> float:
    """Compute annualized Sharpe ratio given daily returns."""
    if not returns:
        return 0.0
    excess = [r - risk_free/252 for r in returns]
    avg = st.mean(excess)
    std = st.stdev(excess) if len(excess) > 1 else 0
    if std == 0:
        return 0.0
    return math.sqrt(252) * avg / std

def lagged_momentum(prices: List[float], months: int = 6, lag: int = 1, period: int = 21) -> float:
    """Return percentage change over ``months`` ending ``lag`` months ago."""
    needed = (months + lag) * period
    if len(prices) < needed:
        raise ValueError("Not enough price history for momentum calculation")
    end_idx = len(prices) - lag * period - 1
    start_idx = len(prices) - (months + lag) * period - 1
    start = prices[start_idx]
    end = prices[end_idx]
    if start == 0:
        return 0.0
    return end / start - 1

def compute_volatility(returns: List[float]) -> float:
    """Annualized standard deviation of daily returns."""
    if not returns:
        return 0.0
    std = st.stdev(returns) if len(returns) > 1 else 0
    return math.sqrt(252) * std

