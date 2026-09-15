# Macro Market Intelligence

## Economic signals → structured market context

A ready, reproducible macroeconomic analytics project that transforms public economic indicators into **decision-oriented analytical signals** using Python, SQL, time-series analysis, feature engineering, and visualization.

> **Portfolio focus:** turning raw economic data into evidence, context, and the next analytical question—not simply producing charts.

### Analyst Snapshot

| Capability | Demonstrated here |
|---|---|
| Data preparation | Validation, frequency alignment, missing-value handling |
| Time-series analysis | YoY growth, 3-month momentum, trend comparison |
| Feature engineering | Yield-curve proxy, z-scores, derived indicators |
| Statistical reasoning | Correlation analysis and standardized signals |
| Segmentation | Heuristic macro-regime classification |
| SQL | Reusable analytical queries |
| Communication | Executive dashboard and decision framework |
| Reproducibility | Scripted pipeline + GitHub Actions |

## Business Questions

- How are U.S. interest rates evolving over time?
- How are inflation, unemployment, and growth changing relative to monetary-policy conditions?
- What does the 10-year Treasury minus federal funds spread indicate about the rate environment?
- Which indicators are accelerating or decelerating over three months?
- Which historical relationships deserve further investigation?
- How can multiple indicators be combined into a consistent macro regime framework?

## Executive Dashboard

See the recruiter-facing interpretation layer: **[Executive Dashboard](reports/executive_dashboard.md)**.

The dashboard is designed around:

**Observation → evidence → relationship → uncertainty → next analytical question**

## Analytical Workflow

```text
Public Economic Data → Validation → Frequency Alignment
        ↓
Derived Metrics → Momentum / Z-Scores → Heuristic Regimes
        ↓
SQL Analysis → Visual Reporting → Decision Framework
```

## Advanced Analytics

- Year-over-year inflation and GDP growth
- Three-month policy-rate and macro-momentum changes
- Yield-curve proxy
- Standardized indicator scores
- Heuristic macro-regime classification
- Regime-frequency summary
- Correlation analysis
- Decision-oriented interpretation rules

The regime model is explicitly **heuristic and descriptive**, not a predictive model.

## Tech Stack

**Python · pandas · NumPy · SQL · Matplotlib · Public economic data · Git/GitHub · GitHub Actions**

## Repository Structure

```text
├── data/                 # Generated raw/processed data
├── docs/                 # Methodology, dictionary, decision framework
├── sql/                  # Analytical queries
├── src/                  # Download, cleaning and analysis pipeline
├── outputs/              # Generated charts
├── .github/workflows/    # Automated quality checks
├── README.md
└── requirements.txt
```

## Reproducibility

```bash
pip install -r requirements.txt
python src/download_data.py
python src/clean_data.py
python src/analyze_macro.py
```

Every analytical output can be regenerated from the documented pipeline. GitHub Actions also runs Python compilation checks on pushes and pull requests.

## Analyst Decision Framework

**What happened?** Measure direction, magnitude, and persistence.

**Why might it matter?** Compare momentum and relationships across indicators.

**What should be investigated next?** Prioritize regime transitions, unusually large changes, and relationships that remain stable across periods.

**What should not be assumed?** Correlation does not establish causation, and heuristic regimes are not investment signals.

## What This Project Demonstrates

Economic data analysis, time-series alignment, feature engineering, statistical reasoning, SQL, visualization, reproducible pipelines, and evidence-based communication.

## Data Integrity

The project uses public economic data for analytical demonstration and research. Derived features are clearly distinguished from official economic releases. The project is not investment advice.

## Portfolio

Part of a three-project Data Analyst portfolio:

- **Macro Market Intelligence** — economic and market context
- **Trading Risk & Performance Analytics** — financial risk and performance
- **Customer Support Analytics** — business and operations analytics
