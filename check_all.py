import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios"
]

for table in tables:
    df = pd.read_sql(
        f"SELECT COUNT(*) AS count FROM {table} WHERE company_id='SBIN'",
        conn
    )

    print(table, ":", df.iloc[0]["count"])