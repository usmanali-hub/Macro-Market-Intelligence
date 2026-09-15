"""Clean and align downloaded macroeconomic series."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

FILES = {
    "effective_federal_funds_rate": "fed_funds",
    "consumer_price_index": "cpi",
    "unemployment_rate": "unemployment",
    "gross_domestic_product": "gdp",
    "treasury_10y_yield": "treasury_10y",
}


def load_monthly(name: str, output_name: str) -> pd.DataFrame:
    path = RAW / f"{name}.csv"
    df = pd.read_csv(path)
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    value_col = [c for c in df.columns if c != "observation_date"][0]
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df.dropna(subset=[value_col]).set_index("observation_date")
    monthly = df.resample("MS")[value_col].mean().rename(output_name).reset_index()
    monthly.to_csv(PROCESSED / f"{output_name}.csv", index=False)
    return monthly


if __name__ == "__main__":
    for source, output in FILES.items():
        try:
            load_monthly(source, output)
            print(f"Processed {output}")
        except FileNotFoundError:
            print(f"Missing raw file: {source}. Run download_data.py first.")
