import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "financial_ratios",
    "companies",
    "sectors",
    "market_cap"
]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 5", conn)
    print("\n" + "=" * 60)
    print(table.upper())
    print("=" * 60)
    print(df.columns.tolist())

conn.close()