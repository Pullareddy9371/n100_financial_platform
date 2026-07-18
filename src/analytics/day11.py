import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import CashFlowKPIs

conn = sqlite3.connect("db/nifty100.db")

cashflow = pd.read_sql("SELECT * FROM cashflow", conn)
pnl = pd.read_sql("SELECT * FROM profitandloss", conn)

df = cashflow.merge(
    pnl,
    on=["company_id", "year"],
    how="inner"
)

# Free Cash Flow
df["Free Cash Flow"] = df.apply(
    lambda x: CashFlowKPIs.free_cash_flow(
        x["operating_activity"],
        x["investing_activity"]
    ),
    axis=1
)

# CFO Quality Score
df["CFO Quality"] = df.apply(
    lambda x: CashFlowKPIs.cfo_quality_score(
        x["operating_activity"],
        x["net_profit"]
    ),
    axis=1
)

# CapEx Intensity
df["CapEx Intensity"] = df.apply(
    lambda x: CashFlowKPIs.capex_intensity(
        x["investing_activity"],
        x["sales"]
    ),
    axis=1
)

# FCF Conversion Rate
df["FCF Conversion Rate"] = df.apply(
    lambda x: CashFlowKPIs.fcf_conversion_rate(
        x["Free Cash Flow"],
        x["operating_profit"]
    ),
    axis=1
)

# Cash Flow Pattern
df["Pattern"] = df.apply(
    lambda x: CashFlowKPIs.cashflow_pattern(
        x["operating_activity"],
        x["investing_activity"],
        x["financing_activity"]
    ),
    axis=1
)

print(
    df[
        [
            "company_id",
            "year",
            "Free Cash Flow",
            "CFO Quality",
            "CapEx Intensity",
            "FCF Conversion Rate",
            "Pattern"
        ]
    ].head()
)

df[
    [
        "company_id",
        "year",
        "Free Cash Flow",
        "CFO Quality",
        "CapEx Intensity",
        "FCF Conversion Rate",
        "Pattern"
    ]
].to_csv(
    "src/output/capital_allocation.csv",
    index=False
)

print("\ncapital_allocation.csv created successfully!")

conn.close()