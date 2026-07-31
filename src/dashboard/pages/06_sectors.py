import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

st.title("🏭 Sector Analysis Dashboard")

query = """
SELECT
    s.broad_sector,
    c.company_name,
    f.return_on_equity_pct,
    f.net_profit_margin_pct,
    f.debt_to_equity,
    f.asset_turnover,
    m.market_cap_crore
FROM financial_ratios f

LEFT JOIN companies c
ON f.company_id = c.id

LEFT JOIN sectors s
ON f.company_id = s.company_id

LEFT JOIN market_cap m
ON f.company_id = m.company_id
"""

df = pd.read_sql(query, conn)

df = df.drop_duplicates(
    subset="company_name",
    keep="last"
)

st.subheader("Sector Summary")

summary = (
    df.groupby("broad_sector")
      .agg(
        Companies=("company_name", "count"),
        Avg_ROE=("return_on_equity_pct", "mean"),
        Avg_NPM=("net_profit_margin_pct", "mean"),
        Avg_DE=("debt_to_equity", "mean"),
        Avg_Asset_Turnover=("asset_turnover", "mean"),
        Total_Market_Cap=("market_cap_crore", "sum")
      )
      .reset_index()
)

st.dataframe(summary, use_container_width=True)

st.markdown("---")

st.subheader("🏆 Sector Market Capitalization")

fig1 = px.bar(
    summary,
    x="broad_sector",
    y="Total_Market_Cap",
    color="broad_sector",
    title="Market Capitalization by Sector"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

st.subheader("📊 Average ROE by Sector")

fig2 = px.bar(
    summary,
    x="broad_sector",
    y="Avg_ROE",
    color="Avg_ROE",
    title="Average ROE"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.subheader("🥧 Companies by Sector")

fig3 = px.pie(
    summary,
    names="broad_sector",
    values="Companies",
    hole=0.45
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

sector = st.selectbox(
    "Select Sector",
    sorted(df["broad_sector"].dropna().unique())
)

sector_df = df[df["broad_sector"] == sector]

st.subheader(f"{sector} Companies")

st.dataframe(
    sector_df[
        [
            "company_name",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "asset_turnover",
            "market_cap_crore"
        ]
    ],
    use_container_width=True
)

csv = sector_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Sector Report",
    csv,
    f"{sector}_report.csv",
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