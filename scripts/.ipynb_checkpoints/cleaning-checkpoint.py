# scripts/cleaning.py

import pandas as pd

def filter_min_history(df: pd.DataFrame, months: int = 12) -> pd.DataFrame:
    """
    Keep only rows with Date within the last `months` months.
    """
    df2 = df.copy()
    df2['Date'] = pd.to_datetime(df2['Date'])
    cutoff = df2['Date'].max() - pd.DateOffset(months=months)
    return df2[df2['Date'] >= cutoff]


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Forward-fill then backward-fill missing values, per ticker,
    while preserving all original columns (including 'ticker').
    """
    df2 = df.copy()
    df2['Date'] = pd.to_datetime(df2['Date'])
    df2 = df2.sort_values(['ticker', 'Date'])
    # For each ticker group, ffill then bfill, but keep the 'ticker' column intact
    df2 = df2.groupby('ticker', group_keys=False).apply(lambda g: g.ffill().bfill())
    return df2


def flag_illiquid(df: pd.DataFrame, vol_thresh: float = 1e5) -> pd.DataFrame:
    """
    Compute a 20-day rolling average of Volume per ticker and
    flag days where that average falls below vol_thresh.
    """
    df2 = df.copy()
    df2['Date'] = pd.to_datetime(df2['Date'])
    df2 = df2.sort_values(['ticker', 'Date'])
    # Rolling 20-day average volume
    df2['rolling_vol20'] = (
        df2
        .groupby('ticker')['Volume']
        .transform(lambda x: x.rolling(20, min_periods=1).mean())
    )
    # Flag illiquid days
    df2['illiquid_flag'] = df2['rolling_vol20'] < vol_thresh
    return df2