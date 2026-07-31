import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

st.title("💰 Capital Allocation Dashboard")

query = """
SELECT
    c.company_name,
    f.company_id,
    f.year,
    f.free_cash_flow_cr,
    f.capex_cr,
    f.cash_from_operations_cr
FROM financial_ratios f

LEFT JOIN companies c
ON f.company_id = c.id

ORDER BY year
"""

df = pd.read_sql(query, conn)

companies = sorted(df["company_name"].dropna().unique())

company = st.selectbox(
    "Select Company",
    companies
)

company_df = df[df["company_name"] == company]

st.subheader("Capital Allocation Data")

st.dataframe(
    company_df,
    use_container_width=True
)

st.markdown("---")

fig1 = px.line(
    company_df,
    x="year",
    y="free_cash_flow_cr",
    markers=True,
    title="Free Cash Flow Trend"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

fig2 = px.bar(
    company_df,
    x="year",
    y="capex_cr",
    title="Capital Expenditure"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

fig3 = px.line(
    company_df,
    x="year",
    y="cash_from_operations_cr",
    markers=True,
    title="Cash From Operations"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

company_df["FCF / CFO Ratio"] = (
    company_df["free_cash_flow_cr"] /
    company_df["cash_from_operations_cr"]
).round(2)

st.subheader("Capital Allocation Metrics")

st.dataframe(
    company_df[
        [
            "year",
            "free_cash_flow_cr",
            "capex_cr",
            "cash_from_operations_cr",
            "FCF / CFO Ratio"
        ]
    ],
    use_container_width=True
)

csv = company_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Capital Allocation Report",
    csv,
    "capital_allocation.csv",
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