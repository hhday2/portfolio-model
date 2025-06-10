# File: scripts/data_fetcher.py

import yfinance as yf
import pandas as pd

def fetch_data(tickers, start_date, end_date):
    """
    Fetch adjusted close prices for a list of tickers using yfinance.

    Parameters:
    tickers (list): List of stock ticker symbols.
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
    pd.DataFrame: DataFrame with tickers as columns and date as index.
    """
    data = yf.download(tickers, start=start_date, end=end_date)

    try:
        adj_close = data['Adj Close']
    except KeyError:
        print("Note: 'Adj Close' not found, using 'Close' instead.")
        adj_close = data['Close']

    adj_close.index = pd.to_datetime(adj_close.index)
    return adj_close
