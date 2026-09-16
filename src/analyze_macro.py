"""Run exploratory macroeconomic analysis and generate decision-oriented outputs."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
CHARTS = ROOT / "outputs" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

SERIES = [
    "fed_funds",
    "cpi",
    "unemployment",
    "gdp",
    "treasury_3m",
    "treasury_2y",
    "treasury_5y",
    "treasury_10y",
    "treasury_30y",
]


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(PROCESSED / f"{name}.csv", parse_dates=["observation_date"])
    return df.set_index("observation_date")


def build_dataset() -> pd.DataFrame:
    frames = [load(name) for name in SERIES]
    # Forward-fill means "latest known observation" after monthly alignment;
    # it does not imply that lower-frequency indicators were measured daily.
    return pd.concat(frames, axis=1).sort_index().ffill()


def zscore(series: pd.Series) -> pd.Series:
    std = series.std()
    return (series - series.mean()) / std if std else pd.Series(0, index=series.index)


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["cpi_yoy_pct"] = out["cpi"].pct_change(12) * 100
    out["gdp_yoy_pct"] = out["gdp"].pct_change(12) * 100
    out["yield_curve_proxy"] = out["treasury_10y"] - out["fed_funds"]
    out["curve_10y_2y"] = out["treasury_10y"] - out["treasury_2y"]
    out["curve_10y_3m"] = out["treasury_10y"] - out["treasury_3m"]
    out["curve_30y_10y"] = out["treasury_30y"] - out["treasury_10y"]
    out["rate_change_3m"] = out["fed_funds"].diff(3)
    out["inflation_z"] = zscore(out["cpi_yoy_pct"])
    out["growth_z"] = zscore(out["gdp_yoy_pct"])
    out["unemployment_z"] = zscore(out["unemployment"])
    out["curve_z"] = zscore(out["yield_curve_proxy"])
    out["curve_10y_2y_z"] = zscore(out["curve_10y_2y"])
    out["curve_10y_3m_z"] = zscore(out["curve_10y_3m"])
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


def lagged_correlation_table(
    df: pd.DataFrame,
    source: str = "cpi_yoy_pct",
    targets: tuple[str, ...] = ("fed_funds", "treasury_10y", "curve_10y_2y"),
    max_lag: int = 12,
) -> pd.DataFrame:
    """Calculate descriptive lead/lag correlations without claiming causality.

    Positive lag means the target is shifted forward, asking whether the source
    is associated with the target observed that many months later.
    """
    rows = []
    for target in targets:
        for lag in range(0, max_lag + 1):
            aligned = pd.concat(
                [df[source], df[target].shift(-lag)], axis=1
            ).dropna()
            rows.append(
                {
                    "source": source,
                    "target": target,
                    "target_lead_months": lag,
                    "correlation": aligned.iloc[:, 0].corr(aligned.iloc[:, 1])
                    if len(aligned) >= 3
                    else np.nan,
                    "observations": len(aligned),
                }
            )
    return pd.DataFrame(rows)


def save_charts(df: pd.DataFrame) -> None:
    charts = [
        (
            df[["fed_funds", "treasury_10y"]],
            "U.S. Interest Rates Over Time",
            "Rate (%)",
            "interest_rates.svg",
        ),
        (
            df[["cpi_yoy_pct", "unemployment"]],
            "Inflation and Unemployment",
            "Percent",
            "inflation_unemployment.svg",
        ),
        (
            df[["treasury_3m", "treasury_2y", "treasury_5y", "treasury_10y", "treasury_30y"]],
            "U.S. Treasury Curve",
            "Yield (%)",
            "treasury_curve.svg",
        ),
    ]
    for frame, title, ylabel, filename in charts:
        ax = frame.plot(figsize=(11, 5), title=title)
        ax.set_ylabel(ylabel)
        ax.figure.tight_layout()
        ax.figure.savefig(CHARTS / filename, format="svg", bbox_inches="tight")
        plt.close(ax.figure)

    corr = df[["fed_funds", "cpi_yoy_pct", "unemployment", "gdp_yoy_pct", "treasury_10y"]].corr()
    ax = corr.plot(kind="bar", figsize=(11, 5), title="Macro Indicator Correlations")
    ax.set_ylabel("Correlation")
    ax.figure.tight_layout()
    ax.figure.savefig(CHARTS / "correlations.svg", format="svg", bbox_inches="tight")
    plt.close(ax.figure)

    regime_counts = df["macro_regime"].value_counts().sort_values()
    ax = regime_counts.plot(kind="barh", figsize=(10, 5), title="Heuristic Macro Regime Observations")
    ax.set_xlabel("Observations")
    ax.figure.tight_layout()
    ax.figure.savefig(CHARTS / "macro_regimes.svg", format="svg", bbox_inches="tight")
    plt.close(ax.figure)


if __name__ == "__main__":
    data = analyze(build_dataset())
    data.to_csv(PROCESSED / "macro_master.csv")
    data["macro_regime"].value_counts().rename("observations").to_csv(PROCESSED / "macro_regime_summary.csv")
    lagged_correlation_table(data).to_csv(PROCESSED / "lagged_correlations.csv", index=False)
    save_charts(data)
    print(data.tail())
