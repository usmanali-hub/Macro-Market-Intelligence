"""Download selected U.S. macroeconomic series from FRED public CSV endpoints."""
from pathlib import Path
import pandas as pd

BASE_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
SERIES = {
    "FEDFUNDS": "effective_federal_funds_rate",
    "CPIAUCSL": "consumer_price_index",
    "UNRATE": "unemployment_rate",
    "GDP": "gross_domestic_product",
    "DGS10": "treasury_10y_yield",
}

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def download_series(series_id: str, name: str) -> pd.DataFrame:
    url = BASE_URL.format(series_id)
    df = pd.read_csv(url)
    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    value_cols = [c for c in df.columns if c != "observation_date"]
    df[value_cols[0]] = pd.to_numeric(df[value_cols[0]], errors="coerce")
    df = df.dropna(subset=["observation_date"])
    output = RAW / f"{name}.csv"
    df.to_csv(output, index=False)
    print(f"Saved {series_id} -> {output}")
    return df


if __name__ == "__main__":
    for series_id, name in SERIES.items():
        try:
            download_series(series_id, name)
        except Exception as exc:
            print(f"Could not download {series_id}: {exc}")
