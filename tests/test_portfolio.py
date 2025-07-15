import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.portfolio import load_prices, score_tickers
from pathlib import Path


def test_load_prices(tmp_path):
    csv_path = tmp_path / "test.csv"
    csv_path.write_text("Date,Close,ticker\n2021-01-01,100,A\n2021-01-02,101,A\n")
    data = load_prices(csv_path)
    assert data == {"A": [100.0, 101.0]}


def test_score_tickers():
    hist = {"A": [100 + i for i in range(300)]}
    scores = score_tickers(hist)
    assert "A" in scores
