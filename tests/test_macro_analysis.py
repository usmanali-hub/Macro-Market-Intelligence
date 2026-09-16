import numpy as np
import pandas as pd

from src.analyze_macro import analyze, lagged_correlation_table


def sample_frame(periods=36):
    dates = pd.date_range("2020-01-01", periods=periods, freq="MS")
    return pd.DataFrame(
        {
            "fed_funds": np.linspace(1.0, 4.0, periods),
            "cpi": np.linspace(100.0, 112.0, periods),
            "unemployment": np.linspace(6.0, 4.0, periods),
            "gdp": np.linspace(20_000.0, 22_000.0, periods),
            "treasury_3m": np.linspace(0.8, 3.8, periods),
            "treasury_2y": np.linspace(1.0, 3.9, periods),
            "treasury_5y": np.linspace(1.4, 4.0, periods),
            "treasury_10y": np.linspace(1.8, 4.2, periods),
            "treasury_30y": np.linspace(2.2, 4.5, periods),
        },
        index=dates,
    )


def test_analyze_creates_full_curve_features():
    result = analyze(sample_frame())
    for column in [
        "curve_10y_2y",
        "curve_10y_3m",
        "curve_30y_10y",
        "curve_10y_2y_z",
        "curve_10y_3m_z",
        "macro_regime",
    ]:
        assert column in result.columns

    assert np.isclose(result["curve_10y_2y"].iloc[-1], 0.3)
    assert np.isclose(result["curve_10y_3m"].iloc[-1], 0.4)
    assert np.isclose(result["curve_30y_10y"].iloc[-1], 0.3)


def test_lagged_correlation_table_has_expected_horizons():
    result = lagged_correlation_table(sample_frame(), max_lag=6)
    assert len(result) == 3 * 7
    assert set(result["target"]) == {"fed_funds", "treasury_10y", "curve_10y_2y"}
    assert result["target_lead_months"].min() == 0
    assert result["target_lead_months"].max() == 6
    assert (result["observations"] >= 3).all()


def test_lagged_correlation_uses_future_target_values():
    frame = sample_frame()
    result = lagged_correlation_table(frame, targets=("fed_funds",), max_lag=1)
    zero_lag = result.loc[result["target_lead_months"] == 0, "correlation"].iloc[0]
    one_lag = result.loc[result["target_lead_months"] == 1, "correlation"].iloc[0]
    assert np.isfinite(zero_lag)
    assert np.isfinite(one_lag)
