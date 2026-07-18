import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    company_id,
    year,
    return_on_equity_pct,
    net_profit_margin_pct,
    operating_profit_margin_pct
FROM financial_ratios
LIMIT 10
"""

df = pd.read_sql(query, conn)

print("\nManual Spot Check")
print("=" * 50)
print(df)

conn.close()