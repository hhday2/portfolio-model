# scripts/ingestion.py

import yfinance as yf
import pandas as pd
from .utils import load_etf_list

def fetch_etf_data(etfs: list[str] = None) -> dict:
    etfs = etfs or load_etf_list()
    out = {}
    for t in etfs:
        obj = yf.Ticker(t)
        hist = obj.history(period="max")[["Close","Volume"]]
        raw_cat = obj.info.get("category") or obj.info.get("sector")
        out[t] = {"history": hist, "category_raw": raw_cat}
    return out

def build_price_df(raw: dict) -> pd.DataFrame:
    rows = []
    for t, v in raw.items():
        df = v["history"].reset_index()
        df["ticker"]       = t
        df["category_raw"] = v["category_raw"]
        rows.append(df)
    return pd.concat(rows, ignore_index=True)