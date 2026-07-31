import sqlite3
import pandas as pd
import os

DB_PATH = "db/nifty100.db"


class ValuationEngine:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def load_data(self):

        # -----------------------------
        # Load Financial Ratios
        # -----------------------------
        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        # -----------------------------
        # Load Companies
        # -----------------------------
        companies = pd.read_sql(
            """
            SELECT
                id,
                company_name,
                roe_percentage,
                roce_percentage
            FROM companies
            """,
            self.conn
        )

        # -----------------------------
        # Load Sectors
        # -----------------------------
        sectors = pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector
            FROM sectors
            """,
            self.conn
        )

        # -----------------------------
        # Load Market Cap
        # -----------------------------
        market = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                market_cap_crore,
                enterprise_value_crore,
                pe_ratio,
                pb_ratio,
                ev_ebitda,
                dividend_yield_pct
            FROM market_cap
            """,
            self.conn
        )

        # -----------------------------
        # Prepare Year Columns
        # -----------------------------
        ratios["year"] = ratios["year"].astype(str)

        # Example:
        # Mar 2023 -> 2023
        ratios["year_num"] = ratios["year"].str.extract(r"(\d{4})")

        market["year_num"] = market["year"].astype(str)

        print("\nFINANCIAL RATIOS")
        print(ratios[["company_id", "year", "year_num"]].head())

        print("\nMARKET CAP")
        print(market[["company_id", "year", "year_num"]].head())

        # -----------------------------
        # Merge Companies
        # -----------------------------
        df = ratios.merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left"
        )

        df.drop(
            columns=["id", "id_x", "id_y"],
            errors="ignore",
            inplace=True
        )

        # -----------------------------
        # Merge Sector
        # -----------------------------
        df = df.merge(
            sectors,
            on="company_id",
            how="left"
        )

        # -----------------------------
        # Merge Market Data
        # -----------------------------
        df = df.merge(
            market.drop(columns=["year"]),
            on=["company_id", "year_num"],
            how="left"
        )

        print("\nTotal Records :", len(df))

        return df 
    
    def calculate(self, df):

        # -----------------------------
        # Free Cash Flow Yield
        # -----------------------------
        df["fcf_yield"] = (
            df["free_cash_flow_cr"] 
            / df["market_cap_crore"]
         ) * 100
        

        # Replace infinite values
        df["fcf_yield"] = (
            df["fcf_yield"]
            .replace([float("inf"), float("-inf")], pd.NA)
        )

        # -----------------------------
        # Sector Median PE
        # -----------------------------
        sector_pe = (
            df.groupby("broad_sector")["pe_ratio"]
            .median()
            .reset_index()
            .rename(
                columns={
                    "pe_ratio": "sector_median_pe"
                }
            )
        )

        df = df.merge(
            sector_pe,
            on="broad_sector",
            how="left"
        )

        # -----------------------------
        # Sector Median PB
        # -----------------------------
        sector_pb = (
            df.groupby("broad_sector")["pb_ratio"]
            .median()
            .reset_index()
            .rename(
                columns={
                    "pb_ratio": "sector_median_pb"
                }
            )
        )

        df = df.merge(
            sector_pb,
            on="broad_sector",
            how="left"
        )

        # -----------------------------
        # Valuation Classification
        # -----------------------------
        def valuation(row):

            if pd.isna(row["pe_ratio"]):
                return "Unknown"

            if row["pe_ratio"] < row["sector_median_pe"] * 0.90:
                return "Discount"

            elif row["pe_ratio"] > row["sector_median_pe"] * 1.10:
                return "Caution"

            return "Fair"

        df["valuation_flag"] = df.apply(
            valuation,
            axis=1
        )

        # -----------------------------
        # Additional Flags
        # -----------------------------
        df["pb_flag"] = df.apply(
            lambda x:
            "Undervalued"
            if (
                pd.notna(x["pb_ratio"])
                and pd.notna(x["sector_median_pb"])
                and x["pb_ratio"] < x["sector_median_pb"]
            )
            else "Normal",
            axis=1
        )

        df["high_dividend"] = df["dividend_yield_pct"] >= 2

        return df
    def save(self, df):

        # Create output folder
        os.makedirs(
            "src/output",
            exist_ok=True
        )

        summary = df[
            [
                "company_id",
                "company_name",
                "year",
                "broad_sector",
                "market_cap_crore",
                "enterprise_value_crore",
                "pe_ratio",
                "pb_ratio",
                "ev_ebitda",
                "dividend_yield_pct",
                "free_cash_flow_cr",
                "fcf_yield",
                "sector_median_pe",
                "sector_median_pb",
                "valuation_flag",
                "pb_flag",
                "high_dividend"
            ]
        ].copy()

        summary.to_csv(
            "src/output/valuation_flags.csv",
            index=False
        )

        summary.to_excel(
            "src/output/valuation_summary.xlsx",
            index=False
        )

        print("\nValuation reports generated successfully!")
        print("CSV  : src/output/valuation_flags.csv")
        print("Excel: src/output/valuation_summary.xlsx")

    def run(self):

        # Load
        df = self.load_data()

        # Calculate
        df = self.calculate(df)

        # Save
        self.save(df)

        print("\nTop 20 Companies\n")

        print(
            df[
                [
                    "company_id",
                    "company_name",
                    "year",
                    "broad_sector",
                    "market_cap_crore",
                    "pe_ratio",
                    "pb_ratio",
                    "fcf_yield",
                    "valuation_flag"
                ]
            ].head(20)
        )

        print("\nSummary")

        print("Total Records :", len(df))
        print("Discount :", (df["valuation_flag"] == "Discount").sum())
        print("Fair      :", (df["valuation_flag"] == "Fair").sum())
        print("Caution   :", (df["valuation_flag"] == "Caution").sum())
        print("Unknown   :", (df["valuation_flag"] == "Unknown").sum())


if __name__ == "__main__":

    ValuationEngine().run()