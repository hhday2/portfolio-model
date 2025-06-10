# scripts/screener.py

def screen_etfs(min_aum: float = 1e10,
                min_avg_vol: float = 5e5,
                must_include: list[str] = None) -> list[str]:
    """
    STUB: returns only the must_include list (uppercased),
    until you wire in a real ETF data client.
    """
    return sorted({t.upper() for t in (must_include or [])})