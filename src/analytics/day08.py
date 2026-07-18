import sqlite3
import pandas as pd

from src.analytics.ratios import RatioEngine

conn = sqlite3.connect("db/nifty100.db")

pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)

df = pnl.merge(
    bs,
    on=["company_id", "year"],
    how="inner"
)

df["Net Profit Margin"] = df.apply(
    lambda x:
    RatioEngine.net_profit_margin(
        x["net_profit"],
        x["sales"]
    ),
    axis=1
)

df["Operating Profit Margin"] = df.apply(
    lambda x:
    RatioEngine.operating_profit_margin(
        x["operating_profit"],
        x["sales"]
    ),
    axis=1
)

df["ROE"] = df.apply(
    lambda x:
    RatioEngine.return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

df["ROCE"] = df.apply(
    lambda x:
    RatioEngine.return_on_capital_employed(
        x["operating_profit"],
        x["equity_capital"],
        x["reserves"],
        x["borrowings"]
    ),
    axis=1
)

df["ROA"] = df.apply(
    lambda x:
    RatioEngine.return_on_assets(
        x["net_profit"],
        x["total_assets"]
    ),
    axis=1
)

print(df[
[
"company_id",
"year",
"Net Profit Margin",
"Operating Profit Margin",
"ROE",
"ROCE",
"ROA"
]
].head())
df["Difference"] = (
    df["Operating Profit Margin"] -
    df["opm_percentage"]
).abs()

warnings = df[df["Difference"] > 1]

print()

print("OPM mismatches (>1%)")

print(warnings[
[
"company_id",
"year",
"Operating Profit Margin",
"opm_percentage",
"Difference"
]
])
# Save OPM mismatch report
warnings.to_csv(
    "src/output/opm_mismatch.csv",
    index=False
)

# Save all profitability ratios
ratio_columns = [
    "company_id",
    "year",
    "Net Profit Margin",
    "Operating Profit Margin",
    "ROE",
    "ROCE",
    "ROA"
]

df[ratio_columns].to_csv(
    "src/output/profitability_ratios.csv",
    index=False
)

print("\nFiles saved successfully!")
print("1. src/output/opm_mismatch.csv")
print("2. src/output/profitability_ratios.csv")
conn.close()


