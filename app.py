"""Interactive dashboard for Macro Market Intelligence."""
from pathlib import Path
import subprocess
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"

st.set_page_config(page_title="Macro Market Intelligence", layout="wide")
st.title("Macro Market Intelligence")
st.caption("Interactive view of public U.S. economic indicators, Treasury curve structure, and derived macro context.")

FILES = {
    "fed_funds": "Policy Rate",
    "treasury_3m": "3M Treasury Yield",
    "treasury_2y": "2Y Treasury Yield",
    "treasury_5y": "5Y Treasury Yield",
    "treasury_10y": "10Y Treasury Yield",
    "treasury_30y": "30Y Treasury Yield",
    "cpi": "CPI",
    "unemployment": "Unemployment",
    "gdp": "GDP",
}


def prepare_data():
    required = [PROCESSED / f"{name}.csv" for name in FILES]
    if not all(path.exists() for path in required):
        subprocess.run([sys.executable, "src/download_data.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "src/clean_data.py"], cwd=ROOT, check=True)


try:
    prepare_data()
    series = {}
    for name, label in FILES.items():
        frame = pd.read_csv(PROCESSED / f"{name}.csv", parse_dates=["observation_date"])
        value = [c for c in frame.columns if c != "observation_date"][0]
        series[label] = frame.set_index("observation_date")[value].rename(label)
    df = pd.concat(series.values(), axis=1).sort_index().ffill()
except Exception as exc:
    st.error(f"Could not prepare the economic dataset: {exc}")
    st.stop()

start, end = st.slider("Historical window", 1948, int(df.index.year.max()), (2000, int(df.index.year.max())))
view = df[(df.index.year >= start) & (df.index.year <= end)]

c1, c2, c3, c4 = st.columns(4)
latest = view.dropna(how="all").iloc[-1]
c1.metric("Policy Rate", f"{latest['Policy Rate']:.2f}%")
c2.metric("10Y Yield", f"{latest['10Y Treasury Yield']:.2f}%")
c3.metric("Unemployment", f"{latest['Unemployment']:.2f}%")
c4.metric("10Y–2Y Spread", f"{latest['10Y Treasury Yield'] - latest['2Y Treasury Yield']:.2f} pp")

left, right = st.columns(2)
with left:
    st.subheader("Rates")
    st.line_chart(view[["Policy Rate", "10Y Treasury Yield"]])
with right:
    st.subheader("Inflation & Labor")
    st.line_chart(view[["CPI", "Unemployment"]])

st.subheader("Treasury Curve")
curve_cols = [
    "3M Treasury Yield",
    "2Y Treasury Yield",
    "5Y Treasury Yield",
    "10Y Treasury Yield",
    "30Y Treasury Yield",
]
st.line_chart(view[curve_cols])

spread_view = pd.DataFrame(index=view.index)
spread_view["10Y–2Y"] = view["10Y Treasury Yield"] - view["2Y Treasury Yield"]
spread_view["10Y–3M"] = view["10Y Treasury Yield"] - view["3M Treasury Yield"]
spread_view["30Y–10Y"] = view["30Y Treasury Yield"] - view["10Y Treasury Yield"]
st.subheader("Curve Spreads")
st.line_chart(spread_view)

st.subheader("Latest Observations")
st.dataframe(view.tail(12).round(2), use_container_width=True)

st.caption(
    "Frequency note: lower-frequency indicators are aligned to a monthly index using their latest known observation; this does not mean they were measured each day. "
    "The Treasury curve uses monthly averages of daily FRED yields."
)
st.info("Public economic data are used for analytical demonstration. Derived indicators are descriptive; correlation does not establish causation, and this dashboard is not investment advice.")
