# scripts/utils.py

import pandas as pd
from pathlib import Path
import yaml

# BASE → the root of your “Portfolio Model” project
BASE = Path(__file__).parent.parent

def data_paths() -> dict:
    """
    Returns the key directories for raw/processed data.
    """
    return {
        "raw":  BASE / "data" / "raw",
        "proc": BASE / "data" / "processed",
    }

def load_etf_list() -> list[str]:
    """
    Returns your ETF universe by running the screener stub.
    """
    from .screener import screen_etfs
    return screen_etfs(
        min_aum=15e9,
        min_avg_vol=1e6,
        must_include=["VOO"]
    )

def load_sector_map() -> dict:
    """
    Reads config/sector_map.csv into a { ticker: detailed_sector } dict.
    """
    path = BASE / "config" / "sector_map.csv"
    df   = pd.read_csv(path, index_col="ticker")
    return df["detailed_sector"].to_dict()

def load_yaml_config(name: str) -> dict:
    """
    Helper to read any YAML under config/, e.g. etf_list.yml.
    """
    path = BASE / "config" / name
    return yaml.safe_load(path.read_text())