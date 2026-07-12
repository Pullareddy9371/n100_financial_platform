import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print("=" * 60)
print("N100 DATA QUALITY MANUAL REVIEW")
print("=" * 60)

# Random 5 Companies
print("\nRandom 5 Companies\n")

query = """
SELECT id, company_name
FROM companies
ORDER BY RANDOM()
LIMIT 5;
"""

print(pd.read_sql(query, conn))

# Year Coverage
print("\nYear Coverage\n")

query = """
SELECT MIN(year) AS Min_Year,
       MAX(year) AS Max_Year
FROM balancesheet;
"""

print(pd.read_sql(query, conn))

# Companies with fewer than 5 years of records
print("\nCompanies with Less Than 5 Years of Balance Sheet Data\n")

query = """
SELECT company_id,
       COUNT(*) AS Years
FROM balancesheet
GROUP BY company_id
HAVING COUNT(*) < 5;
"""

print(pd.read_sql(query, conn))

conn.close()