# scripts/pipeline.py

from .utils      import load_etf_list, data_paths
from .ingestion  import fetch_etf_data, build_price_df
from .cleaning   import filter_min_history, fill_missing, flag_illiquid
from .tagging    import assign_broad_category, assign_detailed_sector

def run_etf_pipeline(months=12, vol_thresh=1e5):
    # 1) Universe
    etfs = load_etf_list()

    # 2) Ingest
    raw      = fetch_etf_data(etfs)
    price_df = build_price_df(raw)

    # 3) Clean & flag
    clean = filter_min_history(price_df, months=months)
    clean = fill_missing(clean)
    clean = flag_illiquid(clean, vol_thresh=vol_thresh)

    # 4) Tag
    clean['broad_cat']      = clean['category_raw'].apply(assign_broad_category)
    clean['detailed_sector']= clean['ticker'].apply(assign_detailed_sector)

    # 5) Export
    out_path = data_paths()['proc'] / 'etf_master.csv'
    clean.to_csv(out_path, index=False)
    print(f"Pipeline complete: ETF master written to {out_path}")

    return clean