import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

st.title("📈 Financial Trends Dashboard")

query = """
SELECT
    c.company_name,
    f.company_id,
    f.year,
    f.return_on_equity_pct,
    f.net_profit_margin_pct,
    f.operating_profit_margin_pct,
    f.debt_to_equity,
    f.asset_turnover,
    f.free_cash_flow_cr
FROM financial_ratios f

LEFT JOIN companies c
ON f.company_id = c.id

ORDER BY year
"""

df = pd.read_sql(query, conn)

companies = sorted(df["company_name"].dropna().unique())

selected = st.multiselect(
    "Select Companies",
    companies,
    default=companies[:3]
)

if selected:

    data = df[df["company_name"].isin(selected)]

    metric = st.selectbox(
        "Select Metric",
        [
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "debt_to_equity",
            "asset_turnover",
            "free_cash_flow_cr"
        ]
    )

    fig = px.line(
        data,
        x="year",
        y=metric,
        color="company_name",
        markers=True,
        title=f"{metric} Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Trend Data")

    st.dataframe(
        data[
            [
                "company_name",
                "year",
                metric
            ]
        ],
        use_container_width=True
    )

    csv = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Trend Data",
        csv,
        "financial_trends.csv",
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