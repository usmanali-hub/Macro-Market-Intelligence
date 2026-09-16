# Methodology

## Data

The project retrieves public observations from the Federal Reserve Bank of St. Louis FRED. Series are downloaded through FRED's public CSV endpoint.

The current Treasury inputs cover 3-month, 2-year, 5-year, 10-year, and 30-year constant-maturity Treasury yields, alongside the effective federal funds rate, CPI, unemployment, and nominal GDP.

## Cleaning

- Parse observation dates explicitly.
- Convert values to numeric types.
- Remove invalid dates and missing values where appropriate.
- Resample daily/frequency-dependent observations to monthly averages for cross-series analysis.
- Forward-fill remaining gaps only after frequency alignment, so the analytical table has a consistent monthly index.

A forward-filled lower-frequency value represents the **latest known observation carried into the aligned analytical index**; it does not mean the underlying economic series was measured at that frequency.

## Derived Metrics

**CPI year-over-year change**

Measures the percentage change in the Consumer Price Index versus 12 months earlier.

**GDP year-over-year change**

Measures the percentage change in nominal GDP versus 12 months earlier. GDP interpretation should account for the fact that this series is nominal.

**Treasury curve**

The project analyzes 3M, 2Y, 5Y, 10Y, and 30Y Treasury yields. Daily Treasury observations are converted to monthly averages before cross-series analysis.

**Curve spreads**

- 10Y–2Y: intermediate curve slope
- 10Y–3M: longer-term yield relative to the short end
- 30Y–10Y: long-end slope

The original 10Y minus federal-funds-rate measure is retained as a separate **policy-rate spread proxy** because it answers a different question from a conventional Treasury-to-Treasury curve slope.

**Three-month rate change**

The change in the effective federal funds rate over three months, used to highlight periods of rapid policy adjustment.

**Lagged correlations**

The pipeline calculates descriptive correlations between CPI year-over-year inflation and selected rate/curve measures at 0–12 month target leads. A positive target lead asks whether the source measure is associated with the target observed later. These results are exploratory and are not causal estimates.

## Information Availability and Vintage Limitations

The current FRED CSV workflow is based on observation data and does not reconstruct historical release vintages or consensus expectations. As a result, the project should not be interpreted as a point-in-time backtest of what an analyst knew on each historical date. Economic series can be revised after initial release.

A future event-intelligence layer can add release dates, actual/consensus/previous values, surprise measures, and vintage-aware datasets when suitable sources are available.

## Interpretation Rules

Correlation and lead/lag correlation are treated as descriptive rather than causal. The project does not claim that one macroeconomic variable causes another without additional econometric testing.

The regime classifier is heuristic and descriptive. Thresholds are transparent rules for historical segmentation, not a validated forecasting model.

All conclusions should be tied to the observed sample, definitions, and data frequency.

## Reproducibility

Run `src/download_data.py`, then `src/clean_data.py`, then `src/analyze_macro.py` from the project root. Automated tests validate the curve calculations and lead/lag analysis, while GitHub Actions validates compilation and the complete data-analysis pipeline.
