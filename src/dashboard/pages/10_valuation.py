import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

sys.path.append(str(Path(__file__).resolve().parents[2]))

st.set_page_config(
    page_title="Valuation",
    layout="wide"
)

st.title("💰 Company Valuation Dashboard")

FILE = "src/output/valuation_flags.csv"

try:
    df = pd.read_csv(FILE)
except FileNotFoundError:
    st.error("Run valuation.py first to generate valuation_flags.csv")
    st.stop()

# -----------------------
# KPI Cards
# -----------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Discount",
    (df["valuation_flag"] == "Discount").sum()
)

c2.metric(
    "Fair",
    (df["valuation_flag"] == "Fair").sum()
)

c3.metric(
    "Caution",
    (df["valuation_flag"] == "Caution").sum()
)

c4.metric(
    "Unknown",
    (df["valuation_flag"] == "Unknown").sum()
)

st.divider()

# -----------------------
# Filter
# -----------------------

sector = st.selectbox(
    "Select Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique().tolist())
)

if sector != "All":
    df = df[df["broad_sector"] == sector]

st.divider()

# -----------------------
# Pie Chart
# -----------------------

fig = px.pie(
    df,
    names="valuation_flag",
    title="Valuation Distribution",
    hole=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------
# Bar Chart
# -----------------------

bar = (
    df.groupby("valuation_flag")
      .size()
      .reset_index(name="Companies")
)

fig2 = px.bar(
    bar,
    x="valuation_flag",
    y="Companies",
    title="Companies by Valuation"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------
# Data Table
# -----------------------

st.subheader("Valuation Table")

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------
# Download
# -----------------------

csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "valuation.csv",
    "text/csv"
)