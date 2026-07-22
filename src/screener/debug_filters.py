import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("SELECT * FROM financial_ratios", conn)

print(df[[
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "interest_coverage",
    "asset_turnover"
]].describe())

conn.close()