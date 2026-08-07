import sqlite3
import pandas as pd
import os

DB_PATH = "db/nifty100.db"
class CapitalAllocationReport:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def load_data(self):
        capital = pd.read_csv("src/output/capital_allocation.csv")

        cashflow = pd.read_excel(
            "src/output/cashflow_intelligence.xlsx"
        )

        companies = pd.read_sql(
            """
            SELECT
                id,
                company_name
            FROM companies
            """,
            self.conn
        )

        capital = capital.merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left"
        )

        capital.drop(
            columns=["id"],
            inplace=True,
            errors="ignore"
        )

        print("\nCapital Allocation Records :", len(capital))
        print("Cashflow Intelligence Records :", len(cashflow))

        return capital, cashflow
    def verify_data(self, capital):
        print("\nVerification")

        companies = capital["company_id"].nunique()

        years = capital["year"].nunique()

        print("Companies :", companies)
        print("Years :", years)
        print("Total Records :", len(capital))

        if companies == 92:
            print("✓ All companies available")
        else:
            print("✗ Missing companies")

    def distribution_summary(self, capital):
        latest_year = capital["year"].max()

        latest = capital[
            capital["year"] == latest_year
        ]

        summary = (
            latest.groupby("Pattern")
            .size()
            .reset_index(name="company_count")
        )

        print("\nLatest Year :", latest_year)

        print(summary)

        os.makedirs(
            "src/output",
            exist_ok=True
        )

        summary.to_csv(
            "src/output/capital_distribution_summary.csv",
            index=False
        )

        return summary
    def update_cashflow_report(self, capital, cashflow):
        latest = capital.sort_values("year")

        latest = latest.groupby(
            "company_id"
        ).tail(1)

        latest = latest[
            [
                "company_id",
                "Pattern"
            ]
        ]

        report = cashflow.merge(
            latest.rename(
                columns={
                    "Pattern": "capital_allocation"
                }
            ),
            on="company_id",
            how="left"
        )

        report.to_excel(
            "src/output/cashflow_intelligence.xlsx",
            index=False
        )

        print("\nCashflow report updated.")

        return report
    def pattern_changes(self, capital):
        capital = capital.sort_values(
            ["company_id", "year"]
        )

        changes = []

        for company, group in capital.groupby("company_id"):
            group = group.reset_index(drop=True)

            for i in range(1, len(group)):
                old = group.loc[i-1, "Pattern"]
                new = group.loc[i, "Pattern"]

                if old != new:
                    changes.append({
                        "company_id": company,
                        "company_name": group.loc[i, "company_name"],
                        "year": group.loc[i, "year"],
                        "previous_pattern": old,
                        "current_pattern": new
                    })

        changes = pd.DataFrame(changes)

        changes.to_csv(
            "src/output/pattern_changes.csv",
            index=False
        )

        print("\nPattern Changes :", len(changes))

        return changes
    def run(self):

        capital, cashflow = self.load_data()

        self.verify_data(capital)

        self.distribution_summary(capital)

        self.update_cashflow_report(
            capital,
            cashflow
        )

        self.pattern_changes(capital)

        print("\nDay 32 Completed Successfully!")


if __name__ == "__main__":
    CapitalAllocationReport().run()