import sys
from pathlib import Path

import streamlit as st
import plotly.express as px

# Fix import path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.db import (
    get_companies,
    get_ratios,
    get_sectors
)

st.set_page_config(
    page_title="Home",
    layout="wide"
)

st.title("📊 N100 Financial Intelligence Dashboard")

# -------------------------------------------------
# Load Data
# -------------------------------------------------

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

years = sorted(ratios["year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

ratios = ratios[
    ratios["year"] == selected_year
]

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------

st.subheader("📈 Dashboard Overview")
# -----------------------------
# KPI Cards
# -----------------------------

st.markdown("""
<style>
.kpi-card{
background:#E8F4FF;
padding:18px;
border-radius:12px;
text-align:center;
border:1px solid #D0E7FF;
box-shadow:2px 2px 8px rgba(0,0,0,0.08);
margin-bottom:15px;
}

.kpi-title{
font-size:16px;
font-weight:bold;
color:#1F4E79;
}

.kpi-value{
font-size:34px;
font-weight:bold;
color:#0A3D62;
}
</style>
""", unsafe_allow_html=True)

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>🏢 Total Companies</div>
    <div class='kpi-value'>{len(companies)}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>📈 Average ROE</div>
    <div class='kpi-value'>{ratios['return_on_equity_pct'].mean():.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>💰 Average Debt / Equity</div>
    <div class='kpi-value'>{ratios['debt_to_equity'].mean():.2f}</div>
    </div>
    """, unsafe_allow_html=True)

c4,c5,c6 = st.columns(3)

with c4:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>📊 Average Net Margin</div>
    <div class='kpi-value'>{ratios['net_profit_margin_pct'].mean():.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>⚙️ Asset Turnover</div>
    <div class='kpi-value'>{ratios['asset_turnover'].mean():.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>🗄 Database Tables</div>
    <div class='kpi-value'>13</div>
    </div>
    """, unsafe_allow_html=True)


st.divider()

st.markdown("### 📈 Platform Summary")

col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("""
    <div style="
    background:#E8F5E9;
    padding:20px;
    border-radius:12px;
    text-align:center;
    border:1px solid #81C784;">
        <h4>🗂 Database Tables</h4>
        <h1>13</h1>
    </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown("""
    <div style="
    background:#FFF3E0;
    padding:20px;
    border-radius:12px;
    text-align:center;
    border:1px solid #FFB74D;">
        <h4>📄 Dashboard Pages</h4>
        <h1>9</h1>
    </div>
    """, unsafe_allow_html=True)

with col9:
    st.markdown("""
    <div style="
    background:#F3E5F5;
    padding:20px;
    border-radius:12px;
    text-align:center;
    border:1px solid #BA68C8;">
        <h4>📊 Financial Metrics</h4>
        <h1>20+</h1>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Project Statistics
# -------------------------------------------------

st.divider()

st.subheader("📊 Project Statistics")

stats_col1, stats_col2, stats_col3 = st.columns(3)

with stats_col1:
    st.info("🏢 Companies : 92")

with stats_col2:
    st.info("📑 Financial Records : 1184")

with stats_col3:
    st.info("👥 Peer Groups : 11")

stats_col4, stats_col5, stats_col6 = st.columns(3)

with stats_col4:
    st.info("📄 Dashboard Pages : 9")

with stats_col5:
    st.info("🗄 Database Tables : 13")

with stats_col6:
    st.info("📈 Metrics Analysed : 20+")

# -------------------------------------------------
# Top Companies
# -------------------------------------------------

st.divider()

st.subheader("🏆 Top 5 Companies by ROE")

top5 = (
    ratios
    .sort_values(
        by="return_on_equity_pct",
        ascending=False
    )
    [
        [
            "company_id",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity"
        ]
    ]
    .head(5)
)

st.dataframe(
    top5,
    use_container_width=True
)

# -------------------------------------------------
# Sector Distribution
# -------------------------------------------------

st.divider()

st.subheader("📊 Sector Distribution")

sector_count = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="Companies",
    hole=0.45,
    title="Companies by Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Sector-wise Company Count
# -------------------------------------------------

st.divider()

st.subheader("📈 Companies in Each Sector")

bar = px.bar(
    sector_count,
    x="broad_sector",
    y="Companies",
    color="Companies",
    title="Sector-wise Company Count"
)

st.plotly_chart(
    bar,
    use_container_width=True
)

# -------------------------------------------------
# Workflow
# -------------------------------------------------

st.divider()

st.subheader("🔄 Project Workflow")

st.markdown("""
""")

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

st.caption(
    "© 2026 N100 Financial Intelligence Platform | Bluestock Fintech Internship | Developed by Pulla Reddy Onteddu"
)