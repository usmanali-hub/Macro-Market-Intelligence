"""Run exploratory macroeconomic analysis and generate recruiter-friendly charts."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
CHARTS = ROOT / "outputs" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(PROCESSED / f"{name}.csv", parse_dates=["observation_date"])
    return df.set_index("observation_date")


def build_dataset() -> pd.DataFrame:
    frames = [load(name) for name in ["fed_funds", "cpi", "unemployment", "gdp", "treasury_10y"]]
    return pd.concat(frames, axis=1).sort_index().ffill()


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["cpi_yoy_pct"] = out["cpi"].pct_change(12) * 100
    out["gdp_yoy_pct"] = out["gdp"].pct_change(12) * 100
    out["yield_curve_proxy"] = out["treasury_10y"] - out["fed_funds"]
    out["rate_change_3m"] = out["fed_funds"].diff(3)
    return out


def save_charts(df: pd.DataFrame) -> None:
    ax = df[["fed_funds", "treasury_10y"]].plot(figsize=(11, 5), title="U.S. Interest Rates Over Time")
    ax.set_ylabel("Rate (%)")
    ax.figure.tight_layout()
    ax.figure.savefig(CHARTS / "interest_rates.png", dpi=150)
    plt.close(ax.figure)

    ax = df[["cpi_yoy_pct", "unemployment"]].plot(figsize=(11, 5), title="Inflation and Unemployment")
    ax.set_ylabel("Percent")
    ax.figure.tight_layout()
    ax.figure.savefig(CHARTS / "inflation_unemployment.png", dpi=150)
    plt.close(ax.figure)

    corr = df[["fed_funds", "cpi_yoy_pct", "unemployment", "gdp_yoy_pct", "treasury_10y"]].corr()
    ax = corr.plot(kind="bar", figsize=(11, 5), title="Macro Indicator Correlations")
    ax.set_ylabel("Correlation")
    ax.figure.tight_layout()
    ax.figure.savefig(CHARTS / "correlations.png", dpi=150)
    plt.close(ax.figure)


if __name__ == "__main__":
    data = analyze(build_dataset())
    data.to_csv(PROCESSED / "macro_master.csv")
    save_charts(data)
    print(data.tail())
