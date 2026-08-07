import sqlite3
import pandas as pd
import re
import os

DB_PATH = "db/nifty100.db"

class AnalysisParser:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def load_data(self):

        query = """
        SELECT *
        FROM analysis
        """

        df = pd.read_sql(query, self.conn)

        print("\nAnalysis Records :", len(df))

        return df

    def show_columns(self, df):

        print("\nColumns in Analysis Table:\n")

        for col in df.columns:
            print(col)

    def run(self):

        df = self.load_data()

        self.show_columns(df)
        parsed = self.parse_percentages(df)

        self.save(parsed)

        print("\nTop Records\n")

        print(parsed.head())
    def parse_percentages(self, df):

       percentage_columns = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
      ]

       parsed = df.copy()

       for col in percentage_columns:

        parsed[col] = (
            parsed[col]
            .astype(str)
            .str.extract(r'([-+]?\d+\.?\d*)')
        )

        parsed[col] = pd.to_numeric(
            parsed[col],
            errors="coerce"
        )

       return parsed
    def save(self, parsed):

       os.makedirs("src/output", exist_ok=True)

       parsed.to_csv(
        "src/output/analysis_parsed.csv",
        index=False
    )

    print("\nSaved Successfully")

if __name__ == "__main__":
    AnalysisParser().run()