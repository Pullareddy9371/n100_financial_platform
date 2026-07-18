import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)

df = pnl.merge(
    bs,
    on=["company_id", "year"],
    how="inner"
)

logs = []

for _, row in df.iterrows():

    if row["sales"] == 0:
        logs.append(
            f"Company {row['company_id']} ({row['year']}): Sales is zero"
        )

    if row["equity_capital"] + row["reserves"] <= 0:
        logs.append(
            f"Company {row['company_id']} ({row['year']}): Equity is zero or negative"
        )

    if row["operating_profit"] < 0:
        logs.append(
            f"Company {row['company_id']} ({row['year']}): Operating Profit is negative"
        )

    if row["net_profit"] < 0:
        logs.append(
            f"Company {row['company_id']} ({row['year']}): Net Profit is negative"
        )

with open("src/output/ratio_edge_cases.log", "w") as file:
    file.write("RATIO EDGE CASE REPORT\n")
    file.write("=" * 50 + "\n\n")

    if logs:
        for item in logs:
            file.write(item + "\n")
    else:
        file.write("No edge cases found.\n")

print("ratio_edge_cases.log created successfully!")

conn.close()