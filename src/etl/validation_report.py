import pandas as pd
from pathlib import Path

from src.etl.loader import load_all_excels

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_validation_report():
    datasets = load_all_excels()

    issues = []

    for table_name, df in datasets.items():

        # Null values
        for column in df.columns:
            null_count = df[column].isnull().sum()

            if null_count > 0:
                issues.append({
                    "table": table_name,
                    "column": column,
                    "issue": "Null Values",
                    "count": int(null_count)
                })

        # Duplicate IDs
        if "id" in df.columns:
            duplicate_ids = df["id"].duplicated().sum()

            if duplicate_ids > 0:
                issues.append({
                    "table": table_name,
                    "column": "id",
                    "issue": "Duplicate IDs",
                    "count": int(duplicate_ids)
                })

        # Duplicate Rows
        duplicate_rows = df.duplicated().sum()

        if duplicate_rows > 0:
            issues.append({
                "table": table_name,
                "column": "-",
                "issue": "Duplicate Rows",
                "count": int(duplicate_rows)
            })

    report = pd.DataFrame(issues)

    report.to_csv(
        OUTPUT_DIR / "validation_failures.csv",
        index=False
    )

    print(report)

    print("\nValidation report generated successfully!")


if __name__ == "__main__":
    generate_validation_report()