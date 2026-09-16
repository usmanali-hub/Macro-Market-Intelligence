# Executive Dashboard — Macro Market Intelligence

> **Economic signals → structured market context**

This is the entry point for the analytical output. Charts are generated reproducibly by `src/analyze_macro.py`.

## Executive View

| Area | Analytical question | Output |
|---|---|---|
| Rates | How have policy and long-term rates moved? | Interest-rate trend |
| Inflation | Is price pressure accelerating or cooling? | YoY inflation + 3-month change |
| Growth | Is economic growth strengthening or weakening? | YoY growth + momentum |
| Labor | Is unemployment improving or deteriorating? | Unemployment trend |
| Curve | How does the 10Y yield compare with policy rates? | Yield-curve proxy |
| Regime | What broad conditions appear historically? | Heuristic regime classification |
| Relationships | Which indicators move together? | Correlation analysis |

## Generated Visuals

Running the pipeline creates these charts under `outputs/charts/`:

- `interest_rates.svg` — policy rate vs 10-year Treasury yield
- `inflation_unemployment.svg` — inflation and unemployment context
- `correlations.svg` — historical indicator relationships
- `macro_regimes.svg` — frequency of heuristic macro regimes

These SVG files are committed so the analytical output is visible directly on GitHub without opening source code.

## Decision Lens

1. **What changed?** Identify direction and magnitude.
2. **Is the change broad or isolated?** Compare rates, inflation, growth, labor, and the curve.
3. **What deserves investigation?** Focus on regime transitions and unusual momentum.
4. **What should not be assumed?** Historical correlation does not establish causation or predict future outcomes.

## Methodological Guardrails

- Public economic data only.
- Derived metrics are separated from official releases.
- Macro regimes are heuristic and descriptive, not predictive.
- Frequency alignment and forward-filling are documented in `docs/methodology.md`.
- This project is analytical demonstration, not investment advice.

## Reproduce

```bash
pip install -r requirements.txt
python src/download_data.py
python src/clean_data.py
python src/analyze_macro.py
```

**Interview framing:** `Observation → evidence → relationship → uncertainty → next analytical question.`
