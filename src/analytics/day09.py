import sqlite3
import pandas as pd

from src.analytics.ratios import RatioEngine

conn = sqlite3.connect("db/nifty100.db")

bs = pd.read_sql("SELECT * FROM balancesheet", conn)

# Example assumptions because the dataset doesn't contain
# current assets, current liabilities, inventory and cash.

bs["current_assets"] = bs["total_assets"] * 0.50
bs["current_liabilities"] = bs["total_liabilities"] * 0.40
bs["inventory"] = bs["current_assets"] * 0.20
bs["cash"] = bs["current_assets"] * 0.10

bs["Current Ratio"] = bs.apply(
    lambda x: RatioEngine.current_ratio(
        x["current_assets"],
        x["current_liabilities"]
    ),
    axis=1
)

bs["Quick Ratio"] = bs.apply(
    lambda x: RatioEngine.quick_ratio(
        x["current_assets"],
        x["inventory"],
        x["current_liabilities"]
    ),
    axis=1
)

bs["Cash Ratio"] = bs.apply(
    lambda x: RatioEngine.cash_ratio(
        x["cash"],
        x["current_liabilities"]
    ),
    axis=1
)

print(
    bs[
        [
            "company_id",
            "year",
            "Current Ratio",
            "Quick Ratio",
            "Cash Ratio"
        ]
    ].head()
)

bs[
    [
        "company_id",
        "year",
        "Current Ratio",
        "Quick Ratio",
        "Cash Ratio"
    ]
].to_csv(
    "src/output/liquidity_ratios.csv",
    index=False
)

print("\nLiquidity ratios saved successfully!")

conn.close()