import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 10",
    conn
)

os.makedirs(
    "reports/radar_charts",
    exist_ok=True
)

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "asset_turnover"
]

for _, row in df.iterrows():

    values = [
        row[m] if pd.notna(row[m]) else 0
        for m in metrics
    ]

    values += values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(metrics),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig = plt.figure(figsize=(6, 6))

    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values)

    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(metrics)

    plt.title(row["company_id"])

    plt.savefig(
        f"reports/radar_charts/{row['company_id']}.png"
    )

    plt.close()

print("Radar charts created successfully.")