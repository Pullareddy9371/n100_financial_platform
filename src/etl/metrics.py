import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_metrics():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        c.company_name,
        m.year,
        m.market_cap_crore,
        m.pe_ratio,
        m.pb_ratio,
        m.dividend_yield_pct
    FROM market_cap m
    JOIN companies c
    ON m.company_id = c.id
    ORDER BY m.market_cap_crore DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print("\nTop 10 Companies by Market Cap\n")
    print(df.head(10))

    df.to_csv(
        OUTPUT_DIR / "financial_metrics.csv",
        index=False
    )

    print("\nfinancial_metrics.csv created successfully!")


if __name__ == "__main__":
    generate_metrics()