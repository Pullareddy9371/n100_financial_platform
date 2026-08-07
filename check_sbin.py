import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios WHERE company_id='SBIN'",
    conn
)

print("\nColumns:")
print(df.columns.tolist())

print("\nLast Record:")
print(df.tail(1).T)