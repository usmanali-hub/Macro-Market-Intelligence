"""Run exploratory macroeconomic analysis and generate decision-oriented outputs."""
from pathlib import Path
import numpy as np
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


def zscore(series: pd.Series) -> pd.Series:
    std = series.std()
    return (series - series.mean()) / std if std else pd.Series(0, index=series.index)


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["cpi_yoy_pct"] = out["cpi"].pct_change(12) * 100
    out["gdp_yoy_pct"] = out["gdp"].pct_change(12) * 100
    out["yield_curve_proxy"] = out["treasury_10y"] - out["fed_funds"]
    out["rate_change_3m"] = out["fed_funds"].diff(3)
    out["inflation_z"] = zscore(out["cpi_yoy_pct"])
    out["growth_z"] = zscore(out["gdp_yoy_pct"])
    out["unemployment_z"] = zscore(out["unemployment"])
    out["curve_z"] = zscore(out["yield_curve_proxy"])
    out["inflation_3m_change"] = out["cpi_yoy_pct"].diff(3)
    out["growth_3m_change"] = out["gdp_yoy_pct"].diff(3)

    def classify(row):
        if pd.isna(row[["inflation_z", "growth_z", "unemployment_z", "curve_z"]]).any():
            return "Insufficient history"
        if row["inflation_z"] > 0.5 and row["growth_z"] < 0:
            return "Inflationary slowdown"
        if row["growth_z"] > 0.5 and row["unemployment_z"] < 0:
            return "Expansion"
        if row["growth_z"] < -0.5 and row["unemployment_z"] > 0.5:
            return "Weak growth"
        if row["curve_z"] > 0.5 and row["growth_z"] > 0:
            return "Improving conditions"
        return "Mixed conditions"

    out["macro_regime"] = out.apply(classify, axis=1)
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

    regime_counts = df["macro_regime"].value_counts().sort_values()
    ax = regime_counts.plot(kind="barh", figsize=(10, 5), title="Heuristic Macro Regime Observations")
    ax.set_xlabel("Observations")
    ax.figure.tight_layout()
    ax.figure.savefig(CHARTS / "macro_regimes.png", dpi=150)
    plt.close(ax.figure)


if __name__ == "__main__":
    data = analyze(build_dataset())
    data.to_csv(PROCESSED / "macro_master.csv")
    data["macro_regime"].value_counts().rename("observations").to_csv(PROCESSED / "macro_regime_summary.csv")
    save_charts(data)
    print(data.tail())
