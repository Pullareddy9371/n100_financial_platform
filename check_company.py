import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT id, company_name
FROM companies
WHERE company_name LIKE '%State%'
   OR id LIKE '%SBI%'
""", conn)

print(df)