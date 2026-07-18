import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

print("Current financial_ratios table:")
print(financial_ratios.head())

# Save back into SQLite
financial_ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("\nfinancial_ratios table updated successfully!")

# Verify row count
count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM financial_ratios",
    conn
)

print("\nVerification:")
print(count)

conn.close()