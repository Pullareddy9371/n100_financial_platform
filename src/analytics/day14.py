import os
import pandas as pd

OUTPUT_DIR = "src/output"

files = [
    "profitability_ratios.csv",
    "liquidity_ratios.csv",
    "solvency_ratios.csv",
    "efficiency_ratios.csv",
    "growth_ratios.csv",
    "valuation_ratios.csv"
]

summary = []

print("=" * 60)
print("FINANCIAL ANALYTICS SUMMARY")
print("=" * 60)

for file in files:

    path = os.path.join(OUTPUT_DIR, file)

    if os.path.exists(path):

        df = pd.read_csv(path)

        print(f"\n{file}")
        print("-" * 60)
        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")

        summary.append({
            "Dataset": file,
            "Rows": len(df),
            "Columns": len(df.columns)
        })

    else:

        print(f"{file} not found!")

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    os.path.join(OUTPUT_DIR, "analytics_summary.csv"),
    index=False
)

print("\nAnalytics Summary Created Successfully!")