# scripts/utils.py

try:
    import pandas as pd
except Exception:  # pragma: no cover - optional dependency
    pd = None
from pathlib import Path
try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None

try:
    import yfinance as yf
except Exception:  # pragma: no cover - optional dependency
    yf = None

# BASE → the root of your “Portfolio Model” project
BASE = Path(__file__).parent.parent

_SETTINGS = None

def load_settings() -> dict:
    """Read config/settings.yml once and cache the result."""
    global _SETTINGS
    if _SETTINGS is None:
        path = BASE / "config" / "settings.yml"
        if path.exists() and yaml is not None:
            _SETTINGS = yaml.safe_load(path.read_text()) or {}
        else:
            _SETTINGS = {}
    return _SETTINGS

def data_paths() -> dict:
    """
    Returns the key directories for raw/processed data.
    """
    return {
        "raw":  BASE / "data" / "raw",
        "proc": BASE / "data" / "processed",
    }

def load_etf_list() -> list[str]:
    """Return the ETF universe from etf_list.yml or via the screener stub."""
    cfg = load_settings().get("screener", {})

    path = BASE / "config" / "etf_list.yml"
    tickers = []
    if path.exists() and yaml is not None:
        raw = yaml.safe_load(path.read_text()) or []
        tickers = [str(t).upper() for t in raw if t]

    if not tickers:
        from .screener import screen_etfs
        tickers = screen_etfs(
            min_aum=cfg.get("min_aum", 15e9),
            min_avg_vol=cfg.get("min_avg_vol", 1e6),
            must_include=cfg.get("must_include", ["VOO"]),
        )

    return sorted(set(tickers))

def load_sector_map() -> dict:
    """
    Reads config/sector_map.csv into a { ticker: detailed_sector } dict.
    """
    if pd is None:
        raise ImportError("pandas is required for load_sector_map")
    path = BASE / "config" / "sector_map.csv"
    df   = pd.read_csv(path, index_col="ticker")
    return df["detailed_sector"].to_dict()

def load_yaml_config(name: str) -> dict:
    """
    Helper to read any YAML under config/, e.g. etf_list.yml.
    """
    path = BASE / "config" / name
    if yaml is None:
        raise ImportError("pyyaml is required for load_yaml_config")
    return yaml.safe_load(path.read_text())


def validate_tickers(tickers: list[str]) -> list[str]:
    """Simple validation to drop tickers with no available data."""
    if yf is None:
        return tickers
    valid = []
    for t in tickers:
        try:
            data = yf.Ticker(t).history(period="1d")
            if not data.empty and data.iloc[-1]["Close"] > 0:
                valid.append(t)
        except Exception:
            continue
    return valid
