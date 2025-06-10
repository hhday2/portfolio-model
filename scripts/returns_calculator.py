# File: scripts/returns_calculator.py

import pandas as pd
import numpy as np

def calculate_daily_returns(price_df):
    """
    Calculate daily returns from price data.

    Parameters:
    price_df (pd.DataFrame): DataFrame of prices.

    Returns:
    pd.DataFrame: DataFrame of daily returns.
    """
    returns = price_df.pct_change().dropna()
    return returns

def compute_portfolio_return(weights, returns_df):
    """
    Calculate daily portfolio return based on asset weights.

    Parameters:
    weights (dict): Dictionary of weights. Example: {'AAPL': 0.5, 'MSFT': 0.5}
    returns_df (pd.DataFrame): Daily returns with tickers as columns.

    Returns:
    pd.Series: Daily portfolio returns as a single column Series.
    """
    aligned_weights = [weights.get(ticker, 0) for ticker in returns_df.columns]
    weight_array = np.array(aligned_weights)
    portfolio_returns = returns_df.dot(weight_array)
    return portfolio_returns