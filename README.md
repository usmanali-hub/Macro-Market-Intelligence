# Macro Market Intelligence

## Economic data → macro signals → decision context

A recruiter-ready **Data & Financial Analytics** project that turns public U.S. economic indicators into structured, decision-oriented analysis using Python, SQL, time-series analysis, feature engineering, statistics, and visualization.

> **Recruiter takeaway:** this project demonstrates the full chain from raw economic data to validated signals, analytical context, visual evidence, and clearly communicated research questions.

## Interactive Dashboard

Run the project as an interactive local dashboard:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard lets users select a historical window and explore policy rates, the Treasury curve, CPI, unemployment, GDP, and curve spreads. It automatically downloads and prepares the public economic data if the processed dataset is not present.

For a hosted version, deploy `app.py` on any Streamlit-compatible hosting service.

## The Business Problem

Economic indicators arrive at different frequencies and can tell different parts of the story. This project creates a repeatable framework for combining **interest rates, inflation, unemployment, GDP growth, and Treasury yields** into one analytical view.

### Questions the analysis answers

- How are policy and short-, medium-, and long-term rates evolving?
- Is inflation accelerating or cooling?
- Is growth strengthening or weakening?
- Is unemployment improving or deteriorating?
- What does the Treasury curve look like across maturities?
- How are 10Y–2Y, 10Y–3M, and 30Y–10Y spreads changing?
- Which indicators are accelerating or decelerating?
- Do macro indicators show descriptive lead/lag relationships worth investigating?
- What broad historical macro regime does the combined evidence describe?

## Executive View

| Area | Output | Business use |
|---|---|---|
| **Rates** | Policy rate + Treasury yields | Monetary-policy context |
| **Inflation** | YoY inflation + momentum | Price-pressure direction |
| **Growth** | YoY growth + momentum | Economic-cycle context |
| **Labor** | Unemployment trend | Labor-market context |
| **Yield curve** | 3M/2Y/5Y/10Y/30Y + spreads | Curve-shape and rate-environment context |
| **Relationships** | Correlations + lagged correlations | Further-investigation questions |
| **Regimes** | Heuristic classification | Consistent historical segmentation |

## Visual Analysis

The charts below are committed as SVG so a recruiter can see the analytical output directly on GitHub. GitHub Actions regenerates and validates the charts on every push/PR and stores the generated versions as workflow artifacts; CI does not commit back to `main`.

![U.S. Interest Rates Over Time](outputs/charts/interest_rates.svg)

![Inflation and Unemployment](outputs/charts/inflation_unemployment.svg)

![U.S. Treasury Curve](outputs/charts/treasury_curve.svg)

![Macro Indicator Correlations](outputs/charts/correlations.svg)

![Heuristic Macro Regime Observations](outputs/charts/macro_regimes.svg)

**[Open the Executive Dashboard](reports/executive_dashboard.md)** for the interpretation layer and methodological guardrails.

## Analytical Workflow

```text
Public Economic Data
        ↓
Validation & Frequency Alignment
        ↓
Derived Metrics & Feature Engineering
        ↓
Momentum / Z-Scores / Treasury Curve Spreads
        ↓
Correlation & Lead/Lag Analysis
        ↓
Heuristic Regime Segmentation
        ↓
SQL + Visual Reporting
        ↓
Decision Framework
```

## What This Demonstrates

**Data preparation** — validation, frequency alignment, missing-value handling, documented transformations.

**Feature engineering** — YoY changes, three-month momentum, Treasury curve spreads, standardized scores, derived indicators.

**Statistical reasoning** — historical correlation and descriptive lead/lag analysis without confusing association with causation.

**Segmentation** — transparent, descriptive macro-regime classification.

**Business communication** — `Observation → evidence → relationship → uncertainty → next analytical question`.

## Tech Stack

**Python · pandas · NumPy · SQL · Matplotlib · Git/GitHub · GitHub Actions · Streamlit**

## Reproduce It

```bash
pip install -r requirements.txt
python src/download_data.py
python src/clean_data.py
python src/analyze_macro.py
```

The pipeline also writes `data/processed/lagged_correlations.csv`, a reusable descriptive lead/lag analysis table.

## Repository Map

| Folder | Purpose |
|---|---|
| `app.py` | Interactive Streamlit dashboard |
| `reports/` | Executive interpretation |
| `docs/` | Methodology, data dictionary, decision framework |
| `sql/` | Reusable analytical queries |
| `src/` | Reproducible pipeline |
| `tests/` | Automated analytical checks |
| `outputs/charts/` | Recruiter-visible analytical charts |
| `.github/workflows/` | Automated validation and chart artifact generation |

## Guardrails

- Public economic data only.
- Derived metrics are distinguished from official releases.
- Treasury curve values are monthly averages of daily FRED yields.
- Lower-frequency indicators are aligned to a monthly index using the latest known observation; this does not mean they were measured each day.
- Lead/lag correlations are descriptive and do not establish causation.
- Macro regimes are heuristic and descriptive, not predictive.
- This version does not claim real-time release-vintage reconstruction; historical revisions may therefore differ from information available at the original release date.
- This is an analytical portfolio project, not investment advice.

## Portfolio

Part of a three-project analytics portfolio:

- **Macro Market Intelligence** — economic and market context
- **Trading Risk & Performance Analytics** — financial risk and performance
- **Customer Support Analytics** — business and operations analytics
