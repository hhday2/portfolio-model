import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.scoring import compute_sharpe, lagged_momentum

def test_compute_sharpe_nonzero():
    returns = [0.01, 0.02] * 126
    sr = compute_sharpe(returns)
    assert sr > 40

def test_lagged_momentum():
    prices = list(range(500))
    m = lagged_momentum(prices, months=6, lag=1)
    assert round(m, 6) == round(0.3579545454545454, 6)
