import sqlite3
import pandas as pd
import os

DB_PATH = "db/nifty100.db"


class ProsConsGenerator:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def load_data(self):

        # Load Financial Ratios
        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        # Load Market Cap
        market = pd.read_sql(
            "SELECT * FROM market_cap",
            self.conn
        )

        # Load Company Names
        companies = pd.read_sql(
            """
            SELECT
                id,
                company_name
            FROM companies
            """,
            self.conn
        )

        # Merge Company Names
        df = ratios.merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left"
        )

        df.drop(
            columns=["id"],
            inplace=True,
            errors="ignore"
        )

        # Convert year to string
        df["year"] = df["year"].astype(str)
        market["year"] = market["year"].astype(str)

        # Merge Market Data
        df = df.merge(
            market,
            on=["company_id", "year"],
            how="left",
            suffixes=("", "_market")
        )

        print("\nMerged Records :", len(df))

        return df

    def generate_pros_cons(self, df):

        pros = []
        cons = []

        for _, row in df.iterrows():

            p = []
            c = []

            # ---------- Pros ----------

            if pd.notna(row["return_on_equity_pct"]) and row["return_on_equity_pct"] >= 20:
                p.append("High Return on Equity")

            if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] < 0.50:
                p.append("Low Debt")

            if pd.notna(row["interest_coverage"]) and row["interest_coverage"] >= 5:
                p.append("Strong Interest Coverage")

            if pd.notna(row["asset_turnover"]) and row["asset_turnover"] >= 1:
                p.append("Efficient Asset Utilization")

            # ---------- Cons ----------

            if pd.notna(row["return_on_equity_pct"]) and row["return_on_equity_pct"] < 10:
                c.append("Low Return on Equity")

            if pd.notna(row["debt_to_equity"]) and row["debt_to_equity"] > 2:
                c.append("High Debt")

            if pd.notna(row["interest_coverage"]) and row["interest_coverage"] < 2:
                c.append("Weak Interest Coverage")

            if pd.notna(row["asset_turnover"]) and row["asset_turnover"] < 0.50:
                c.append("Poor Asset Utilization")

            pros.append(", ".join(p) if p else "No major strengths")
            cons.append(", ".join(c) if c else "No major weaknesses")

        df["Pros"] = pros
        df["Cons"] = cons

        return df

    def save(self, df):

        os.makedirs("src/output", exist_ok=True)

        output = df[
            [
                "company_id",
                "company_name",
                "year",
                "Pros",
                "Cons"
            ]
        ].copy()

        output = output.sort_values(
            by=["company_id", "year"]
        )

        output.to_csv(
            "src/output/pros_cons.csv",
            index=False
        )

        output.to_excel(
            "src/output/pros_cons.xlsx",
            index=False
        )

        print("\nPros & Cons reports generated successfully!")
        print("CSV   : src/output/pros_cons.csv")
        print("Excel : src/output/pros_cons.xlsx")

    def run(self):

        df = self.load_data()

        df = self.generate_pros_cons(df)

        self.save(df)

        print("\nTop 10 Results\n")

        print(
            df[
                [
                    "company_id",
                    "company_name",
                    "Pros",
                    "Cons"
                ]
            ].head(10)
        )

        print("\nTotal Records :", len(df))

        self.conn.close()


if __name__ == "__main__":
    ProsConsGenerator().run()