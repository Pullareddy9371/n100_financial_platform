import sqlite3
import pandas as pd

from src.analytics.ratios import RatioEngine

conn = sqlite3.connect("db/nifty100.db")

pnl = pd.read_sql(
    "SELECT company_id, year, sales, net_profit FROM profitandloss",
    conn
)

bs = pd.read_sql(
    "SELECT company_id, year, total_assets FROM balancesheet",
    conn
)

# Sort data
pnl = pnl.sort_values(["company_id", "year"])
bs = bs.sort_values(["company_id", "year"])

# Previous year values
pnl["previous_sales"] = pnl.groupby("company_id")["sales"].shift(1)
pnl["previous_profit"] = pnl.groupby("company_id")["net_profit"].shift(1)

bs["previous_assets"] = bs.groupby("company_id")["total_assets"].shift(1)

# Sales Growth
pnl["Sales Growth %"] = pnl.apply(
    lambda x: RatioEngine.sales_growth(
        x["sales"],
        x["previous_sales"]
    ) if pd.notna(x["previous_sales"]) else None,
    axis=1
)

# Profit Growth
pnl["Profit Growth %"] = pnl.apply(
    lambda x: RatioEngine.profit_growth(
        x["net_profit"],
        x["previous_profit"]
    ) if pd.notna(x["previous_profit"]) else None,
    axis=1
)

# Asset Growth
bs["Asset Growth %"] = bs.apply(
    lambda x: RatioEngine.asset_growth(
        x["total_assets"],
        x["previous_assets"]
    ) if pd.notna(x["previous_assets"]) else None,
    axis=1
)

growth = pnl.merge(
    bs[["company_id", "year", "Asset Growth %"]],
    on=["company_id", "year"],
    how="left"
)

print(growth[
    [
        "company_id",
        "year",
        "Sales Growth %",
        "Profit Growth %",
        "Asset Growth %"
    ]
].head(10))

growth.to_csv(
    "src/output/growth_ratios.csv",
    index=False
)

print("\nGrowth ratios saved successfully!")

conn.close()