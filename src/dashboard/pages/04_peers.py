import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

sys.path.append(str(Path(__file__).resolve().parents[1]))

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

st.set_page_config(
    page_title="Peer Comparison",
    layout="wide"
)

st.title("👥 Peer Comparison Dashboard")

query = """
SELECT
    p.company_id,
    c.company_name,
    p.broad_sector,
    p.metric,
    p.value,
    p.percentile_rank,
    p.year
FROM peer_percentiles p

LEFT JOIN companies c
ON p.company_id=c.id
"""

df = pd.read_sql(query, conn)

companies = sorted(df.company_name.dropna().unique())

company = st.selectbox(
    "Select Company",
    companies
)

company_df = df[
    df.company_name == company
]

sector = company_df.iloc[0]["broad_sector"]

peer_df = df[
    df.broad_sector == sector
]

st.success(f"Peer Group : {sector}")

# ------------------------
# KPI Cards
# ------------------------

col1,col2,col3 = st.columns(3)

col1.metric(
    "Companies",
    peer_df.company_name.nunique()
)

col2.metric(
    "Metrics",
    peer_df.metric.nunique()
)

col3.metric(
    "Records",
    len(peer_df)
)

st.divider()

# ------------------------
# Company Percentiles
# ------------------------

st.subheader("Company Percentile Rankings")

pivot = company_df.pivot_table(
    index="company_name",
    columns="metric",
    values="percentile_rank"
)

st.dataframe(
    pivot,
    use_container_width=True
)

# ------------------------
# Bar Chart
# ------------------------

fig = px.bar(
    company_df,
    x="metric",
    y="percentile_rank",
    color="metric",
    title="Percentile Ranking"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------
# Peer Comparison
# ------------------------

st.divider()

metric = st.selectbox(
    "Compare Metric",
    sorted(df.metric.unique())
)

compare = peer_df[
    peer_df.metric == metric
]

fig2 = px.bar(
    compare,
    x="company_name",
    y="value",
    color="company_name",
    title=f"{metric} Comparison"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ------------------------
# Scatter Plot
# ------------------------

st.divider()

st.subheader("Peer Distribution")

scatter = px.scatter(
    compare,
    x="value",
    y="percentile_rank",
    color="company_name",
    hover_name="company_name",
    size="percentile_rank"
)

st.plotly_chart(
    scatter,
    use_container_width=True
)

# ------------------------
# Complete Peer Table
# ------------------------

st.divider()

st.subheader("Peer Group Data")

st.dataframe(
    peer_df,
    use_container_width=True
)

# ------------------------
# Download
# ------------------------

csv = peer_df.to_csv(index=False).encode()

st.download_button(
    "📥 Download Peer Comparison",
    csv,
    "peer_comparison.csv",
    "text/csv"
)

conn.close()
# ---------------------------------
# Footer
# ---------------------------------

st.divider()

st.caption(
    "© 2026 N100 Financial Intelligence Platform | Bluestock Fintech Internship | Developed by Pulla Reddy Onteddu"
)