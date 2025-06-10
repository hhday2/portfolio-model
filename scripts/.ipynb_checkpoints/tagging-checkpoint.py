# scripts/tagging.py

from .utils import load_sector_map

# 1) Broad‐category keyword map
BROAD = {
    "Equity":       ["equity", "stock", "large cap", "blend", "growth", "value"],
    "Fixed Income": ["bond", "fixed income", "treasury", "igs"],
    "Commodity":    ["commodity", "gold", "oil", "metal"],
    "Real Estate":  ["reit", "real estate"]
}

# load your detailed-sector CSV into a dict ticker → detailed_sector
_DETAIL_MAP = load_sector_map()


def assign_broad_category(raw_str: str) -> str:
    """
    Map a raw category/sector string to one of the BROAD keys,
    or return "Other" if no match.
    """
    txt = (raw_str or "").lower()
    for bucket, keywords in BROAD.items():
        if any(kw in txt for kw in keywords):
            return bucket
    return "Other"


def assign_detailed_sector(ticker: str) -> str:
    """
    Look up the ticker in your sector_map.csv; default to "Unclassified".
    """
    return _DETAIL_MAP.get(ticker.upper(), "Unclassified")