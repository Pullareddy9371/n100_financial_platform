import sqlite3
import pandas as pd

from src.analytics.ratios import RatioEngine

conn = sqlite3.connect("db/nifty100.db")

market = pd.read_sql("SELECT * FROM market_cap", conn)

profit = pd.read_sql(
    """
    SELECT company_id,
           year,
           eps
    FROM profitandloss
    """,
    conn
)
# Convert merge columns to the same data type
market["year"] = market["year"].astype(str)
profit["year"] = profit["year"].astype(str)

market["company_id"] = market["company_id"].astype(str)
profit["company_id"] = profit["company_id"].astype(str)


companies = pd.read_sql(
    """
    SELECT company_name,
           id,
           book_value
    FROM companies
    """,
    conn
)
companies["id"] = companies["id"].astype(str)

# Merge datasets
df = market.merge(
    profit,
    on=["company_id", "year"],
    how="left"
)

df = df.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# Approximate Market Price
df["market_price"] = (
    df["market_cap_crore"] / 1000
)

# PE Ratio
df["PE Ratio"] = df.apply(
    lambda x: RatioEngine.pe_ratio(
        x["market_price"],
        x["eps"]
    ),
    axis=1
)

# PB Ratio
df["PB Ratio"] = df.apply(
    lambda x: RatioEngine.pb_ratio(
        x["market_price"],
        x["book_value"]
    ),
    axis=1
)

# Earnings Yield
df["Earnings Yield"] = df.apply(
    lambda x: RatioEngine.earnings_yield(
        x["eps"],
        x["market_price"]
    ),
    axis=1
)

print(df[
    [
        "company_id",
        "year",
        "PE Ratio",
        "PB Ratio",
        "Earnings Yield"
    ]
].head())

df[
    [
        "company_id",
        "year",
        "PE Ratio",
        "PB Ratio",
        "Earnings Yield"
    ]
].to_csv(
    "src/output/valuation_ratios.csv",
    index=False
)

print("\nValuation ratios saved successfully!")

conn.close()