import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.db import (
    get_companies,
    get_ratios,
    get_sectors
)

st.set_page_config(
    page_title="Company Profile",
    layout="wide"
)

st.title("🏢 Company Profile")

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

company = st.selectbox(
    "Select Company",
    sorted(companies["company_name"])
)

company_info = companies[
    companies["company_name"] == company
].iloc[0]

company_id = company_info["id"]

ratio = ratios[
    ratios["company_id"] == company_id
].copy()

sector = sectors[
    sectors["company_id"] == company_id
]

# --------------------------------------------------
# Company Information
# --------------------------------------------------

st.subheader("Company Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Company ID:**", company_id)
    st.write("**Company Name:**", company_info["company_name"])

    if "website" in company_info.index:
        st.write("**Website:**", company_info["website"])

with col2:

    if len(sector):

        st.write(
            "**Sector:**",
            sector.iloc[0]["broad_sector"]
        )

        st.write(
            "**Sub Sector:**",
            sector.iloc[0]["sub_sector"]
        )

# --------------------------------------------------
# Latest KPIs
# --------------------------------------------------

latest = ratio.sort_values(
    "year"
).iloc[-1]

st.divider()

st.subheader("Latest Financial KPIs")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "ROE",
    round(latest["return_on_equity_pct"],2)
)

k2.metric(
    "Net Margin",
    round(latest["net_profit_margin_pct"],2)
)

k3.metric(
    "Debt/Equity",
    round(latest["debt_to_equity"],2)
)

k4.metric(
    "Asset Turnover",
    round(latest["asset_turnover"],2)
)

# --------------------------------------------------
# Trend Charts
# --------------------------------------------------

st.divider()

metric = st.selectbox(
    "Choose Metric",
    [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr"
    ]
)

fig = px.line(
    ratio,
    x="year",
    y=metric,
    markers=True,
    title=f"{metric} Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Financial History
# --------------------------------------------------

st.divider()

st.subheader("Financial History")

st.dataframe(
    ratio,
    use_container_width=True
)

# --------------------------------------------------
# Download
# --------------------------------------------------

csv = ratio.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Company Report",
    csv,
    f"{company_id}_financials.csv",
    "text/csv"
)
# ---------------------------------
# Footer
# ---------------------------------

st.divider()

st.caption(
    "© 2026 N100 Financial Intelligence Platform | Bluestock Fintech Internship | Developed by Pulla Reddy Onteddu"
)