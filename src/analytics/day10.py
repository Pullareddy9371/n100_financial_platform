import sqlite3
import pandas as pd

from src.analytics.ratios import RatioEngine

conn = sqlite3.connect("db/nifty100.db")

bs = pd.read_sql("SELECT * FROM balancesheet", conn)
pnl = pd.read_sql("SELECT * FROM profitandloss", conn)

df = bs.merge(
    pnl,
    on=["company_id", "year"],
    how="inner"
)

# Calculate Shareholders' Equity
df["shareholders_equity"] = (
    df["equity_capital"] +
    df["reserves"]
)

# Debt to Equity
df["Debt to Equity"] = df.apply(
    lambda x: RatioEngine.debt_to_equity(
        x["borrowings"],
        x["shareholders_equity"]
    ),
    axis=1
)

# Interest Coverage
df["Interest Coverage"] = df.apply(
    lambda x: RatioEngine.interest_coverage(
        x["operating_profit"],
        x["interest"]
    ),
    axis=1
)

# Debt Ratio
df["Debt Ratio"] = df.apply(
    lambda x: RatioEngine.debt_ratio(
        x["total_liabilities"],
        x["total_assets"]
    ),
    axis=1
)

print(df[
    [
        "company_id",
        "year",
        "Debt to Equity",
        "Interest Coverage",
        "Debt Ratio"
    ]
].head())

df[
    [
        "company_id",
        "year",
        "Debt to Equity",
        "Interest Coverage",
        "Debt Ratio"
    ]
].to_csv(
    "src/output/solvency_ratios.csv",
    index=False
)

print("\nSolvency ratios saved successfully!")

conn.close()