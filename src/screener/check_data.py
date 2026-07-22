import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    "SELECT company_id, year FROM financial_ratios LIMIT 10",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies LIMIT 10",
    conn
)

sectors = pd.read_sql(
    "SELECT company_id, broad_sector FROM sectors LIMIT 10",
    conn
)

market = pd.read_sql(
    "SELECT company_id, year FROM market_cap LIMIT 10",
    conn
)

print("\nFINANCIAL RATIOS")
print(ratios)

print("\nCOMPANIES")
print(companies)

print("\nSECTORS")
print(sectors)

print("\nMARKET CAP")
print(market)

conn.close()