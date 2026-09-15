# Macro Market Intelligence

## Economic signals → structured market context

A reproducible macroeconomic analytics project that transforms public economic indicators into **decision-oriented analytical signals** using Python, SQL, time-series analysis, feature engineering, and visualization.

### Why this project matters

A recruiter should be able to see the full analyst workflow: raw economic releases are downloaded, validated, aligned, transformed into comparable features, segmented into heuristic regimes, queried with SQL, and converted into an interpretable analytical narrative.

## Business Questions

- How are U.S. interest rates evolving over time?
- How are inflation, unemployment, and growth changing relative to monetary-policy conditions?
- What does the 10-year Treasury minus federal funds spread indicate about the rate environment?
- Which indicators are accelerating or decelerating over three months?
- Which historical relationships deserve further investigation?
- How can multiple indicators be combined into a consistent macro regime framework?

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
