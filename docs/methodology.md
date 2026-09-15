# Methodology

## Data

The project retrieves public observations from the Federal Reserve Bank of St. Louis FRED. Series are downloaded through FRED's public CSV endpoint.

## Cleaning

- Parse observation dates explicitly.
- Convert values to numeric types.
- Remove invalid dates and missing values where appropriate.
- Resample daily/frequency-dependent observations to monthly averages for cross-series analysis.
- Forward-fill remaining gaps only after frequency alignment, so the analytical table has a consistent monthly index.

## Derived Metrics

**CPI year-over-year change**

Measures the percentage change in the Consumer Price Index versus 12 months earlier.

**GDP year-over-year change**

Measures the percentage change in nominal GDP versus 12 months earlier. GDP interpretation should account for the fact that this series is nominal.

**Yield-curve proxy**

10-year Treasury yield minus the effective federal funds rate. Negative values indicate the short policy rate was above the 10-year yield.

**Three-month rate change**

The change in the effective federal funds rate over three months, used to highlight periods of rapid policy adjustment.

## Interpretation Rules

Correlation is treated as descriptive rather than causal. The project does not claim that one macroeconomic variable causes another without additional econometric testing.

All conclusions should be tied to the observed sample, definitions, and data frequency.

## Reproducibility

Run `src/download_data.py`, then `src/clean_data.py`, then `src/analyze_macro.py` from the project root. Generated raw/processed data and charts are excluded from version control by `.gitignore` because they can be regenerated from the documented public source.
