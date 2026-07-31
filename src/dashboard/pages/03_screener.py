import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

st.title("📈 Stock Screener")

# ============================
# Load Data
# ============================

query = """
SELECT
    c.company_name,
    f.company_id,
    f.return_on_equity_pct,
    f.net_profit_margin_pct,
    f.operating_profit_margin_pct,
    f.debt_to_equity,
    f.interest_coverage,
    f.asset_turnover,
    f.free_cash_flow_cr,
    m.market_cap_crore,
    m.pe_ratio,
    m.pb_ratio,
    m.dividend_yield_pct,
    s.broad_sector
FROM financial_ratios f

LEFT JOIN companies c
ON f.company_id = c.id

LEFT JOIN sectors s
ON f.company_id = s.company_id

LEFT JOIN market_cap m
ON f.company_id = m.company_id
"""

df = pd.read_sql(query, conn)

# Keep latest company record
df = (
    df.sort_values("market_cap_crore")
      .drop_duplicates(subset="company_id", keep="last")
)

# ============================
# Sidebar Filters
# ============================

st.sidebar.header("Custom Filters")

roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    50,
    15
)

de = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    5.0,
    1.0
)

fcf = st.sidebar.number_input(
    "Minimum Free Cash Flow",
    value=0.0
)

sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique())
)

st.sidebar.markdown("---")

preset = st.sidebar.selectbox(
    "Preset Screener",
    [
        "Custom",
        "Quality Compounder",
        "Value Pick",
        "Growth Accelerator",
        "Dividend Champion",
        "Debt Free Blue Chip",
        "Turnaround Watch"
    ]
)

# ============================
# Apply Presets
# ============================

filtered = df.copy()

if preset == "Quality Compounder":

    filtered = filtered[
        (filtered["return_on_equity_pct"] >= 15) &
        (filtered["debt_to_equity"] <= 1.0) &
        (filtered["free_cash_flow_cr"] > 0)
    ]

elif preset == "Value Pick":

    filtered = filtered[
        (filtered["pe_ratio"] <= 20) &
        (filtered["pb_ratio"] <= 3.0)
    ]

elif preset == "Growth Accelerator":

    filtered = filtered[
        filtered["return_on_equity_pct"] >= 20
    ]

elif preset == "Dividend Champion":

    filtered = filtered[
        filtered["dividend_yield_pct"] >= 2
    ]

elif preset == "Debt Free Blue Chip":

    filtered = filtered[
        filtered["debt_to_equity"] == 0
    ]

elif preset == "Turnaround Watch":

    filtered = filtered[
        filtered["free_cash_flow_cr"] > 0
    ]

else:

    filtered = filtered[
        filtered["return_on_equity_pct"] >= roe
    ]

    filtered = filtered[
        filtered["debt_to_equity"] <= de
    ]

    filtered = filtered[
        filtered["free_cash_flow_cr"] >= fcf
    ]

    if sector != "All":

        filtered = filtered[
            filtered["broad_sector"] == sector
        ]

# ============================
# Composite Quality Score
# ============================

filtered["Composite Score"] = (

    filtered["return_on_equity_pct"].fillna(0) * 0.40 +

    filtered["net_profit_margin_pct"].fillna(0) * 0.30 +

    filtered["operating_profit_margin_pct"].fillna(0) * 0.30

)

filtered = filtered.sort_values(
    "Composite Score",
    ascending=False
)

# ============================
# Results
# ============================

st.subheader("Filtered Companies")

st.success(f"Companies Found : {len(filtered)}")

st.dataframe(

    filtered[
        [
            "company_name",
            "broad_sector",
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct",
            "Composite Score"
        ]
    ],

    use_container_width=True

)

# ============================
# Download CSV
# ============================

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(

    label="📥 Download Screener CSV",

    data=csv,

    file_name="screener_output.csv",

    mime="text/csv"

)

conn.close()
# ---------------------------------
# Footer
# ---------------------------------

st.divider()

st.caption(
    "© 2026 N100 Financial Intelligence Platform | Bluestock Fintech Internship | Developed by Pulla Reddy Onteddu"
)