import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

tables = [
    "analysis",
    "balancesheet",
    "cashflow",
    "companies",
    "documents",
    "profitandloss",
    "prosandcons",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "sectors",
    "stock_prices"
]

conn = sqlite3.connect(DB_PATH)

audit_data = []

for table in tables:
    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]

    audit_data.append({
        "table_name": table,
        "rows_loaded": count,
        "status": "SUCCESS"
    })

conn.close()

audit_df = pd.DataFrame(audit_data)

audit_file = OUTPUT_DIR / "load_audit.csv"
audit_df.to_csv(audit_file, index=False)

print("Load Audit Report")
print(audit_df)
print(f"\nAudit report saved to: {audit_file}")