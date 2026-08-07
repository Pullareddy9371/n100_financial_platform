import sqlite3
import pandas as pd
import os

from src.analytics.cashflow_kpis import CashFlowKPIs

DB_PATH = "db/nifty100.db"
class CashFlowIntelligence:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
    
    def load_data(self):
        # Financial Ratios
        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        # Cash Flow
        cashflow = pd.read_sql(
            "SELECT * FROM cashflow",
            self.conn
        )

        # Profit & Loss
        pnl = pd.read_sql(
            "SELECT * FROM profitandloss",
            self.conn
        )

        # Companies
        companies = pd.read_sql(
            """
            SELECT
                id,
                company_name
            FROM companies
            """,
            self.conn
        )

        # Sectors
        sectors = pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector
            FROM sectors
            """,
            self.conn
        )

        # Convert year columns
        ratios["year"] = ratios["year"].astype(str)
        cashflow["year"] = cashflow["year"].astype(str)
        pnl["year"] = pnl["year"].astype(str)

        ratios["year_num"] = ratios["year"].str.extract(r"(\d{4})")
        cashflow["year_num"] = cashflow["year"].str.extract(r"(\d{4})")
        pnl["year_num"] = pnl["year"].str.extract(r"(\d{4})")

        print("\nFinancial Ratios :", len(ratios))
        print("Cash Flow Records :", len(cashflow))
        print("Profit & Loss Records :", len(pnl))

        # Merge Companies
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

        # Merge Sectors
        df = df.merge(
            sectors,
            on="company_id",
            how="left"
        )

        # Merge Cash Flow
        df = df.merge(
            cashflow.drop(columns=["year"], errors="ignore"),
            on=["company_id", "year_num"],
            how="left",
            suffixes=("", "_cash")
        )

        # Merge Profit & Loss
        df = df.merge(
            pnl.drop(columns=["year"], errors="ignore"),
            on=["company_id", "year_num"],
            how="left",
            suffixes=("", "_pnl")
        )

        print("\nMerged Records :", len(df))

        return df
    
    def calculate(self, df):
        # -----------------------------
        # Free Cash Flow
        # -----------------------------
        df["free_cash_flow"] = df.apply(
            lambda x: CashFlowKPIs.free_cash_flow(
                x.get("cash_from_operations_cr"),
                x.get("capex_cr")
            ),
            axis=1
        )

        # -----------------------------
        # CFO Quality Score
        # -----------------------------
        df["cfo_quality_score"] = df.apply(
            lambda x: CashFlowKPIs.cfo_quality_score(
                x.get("cash_from_operations_cr"),
                x.get("net_profit_margin_pct")
            ),
            axis=1
        )

        # -----------------------------
        # CFO Quality Label
        # -----------------------------
        def quality(score):

            if pd.isna(score):
                return "Unknown"

            if score >= 1:
                return "High Quality"

            elif score >= 0.5:
                return "Moderate"

            return "Accrual Risk"

        df["cfo_quality_label"] = df["cfo_quality_score"].apply(quality)

        # -----------------------------
        # CapEx Intensity
        # -----------------------------
        df["capex_intensity_pct"] = df.apply(
            lambda x: CashFlowKPIs.capex_intensity(
                x.get("capex_cr"),
                x.get("free_cash_flow_cr")
            ),
            axis=1
        )

        # -----------------------------
        # CapEx Label
        # -----------------------------
        def capex_label(value):

            if pd.isna(value):
                return "Unknown"

            if value < 3:
                return "Asset Light"

            elif value <= 8:
                return "Moderate"

            return "Capital Intensive"

        df["capex_label"] = df["capex_intensity_pct"].apply(capex_label)

        # -----------------------------
        # FCF Conversion
        # -----------------------------
        df["fcf_conversion_pct"] = df.apply(
            lambda x: CashFlowKPIs.fcf_conversion_rate(
                x.get("free_cash_flow"),
                x.get("operating_profit_margin_pct")
            ),
            axis=1
        )

        # -----------------------------
        # Distress Flag
        # -----------------------------
        df["distress_flag"] = (
            (df["cash_from_operations_cr"] < 0)
        ).map({
            True: "Yes",
            False: "No"
        })

        # -----------------------------
        # Deleveraging Flag
        # -----------------------------
        df["deleveraging_flag"] = (
            df["total_debt_cr"] < df["total_debt_cr"].median()
        ).map({
            True: "Yes",
            False: "No"
        })

        # -----------------------------
        # Capital Allocation
        # -----------------------------
        def allocation(row):

            if row["distress_flag"] == "Yes":
                return "Distress"

            if row["deleveraging_flag"] == "Yes":
                return "Debt Reduction"

            if row["capex_label"] == "Capital Intensive":
                return "Growth Investment"

            return "Balanced"

        df["capital_allocation_label"] = df.apply(
            allocation,
            axis=1
        )

        return df

    def save(self, df):
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
                "cash_from_operations_cr",
                "capex_cr",
                "free_cash_flow",
                "cfo_quality_score",
                "cfo_quality_label",
                "capex_intensity_pct",
                "capex_label",
                "fcf_conversion_pct",
                "distress_flag",
                "deleveraging_flag",
                "capital_allocation_label"
            ]
        ].copy()

        summary.to_excel(
            "src/output/cashflow_intelligence.xlsx",
            index=False
        )

        summary[
            summary["distress_flag"] == "Yes"
        ].to_csv(
            "src/output/distress_alerts.csv",
            index=False
        )

        print("\nCash Flow Intelligence Reports Generated Successfully!")
        print("Excel : src/output/cashflow_intelligence.xlsx")
        print("CSV   : src/output/distress_alerts.csv")


    def run(self):
        df = self.load_data()

        df = self.calculate(df)

        self.save(df)

        print("\nTop 20 Companies\n")

        print(
            df[
                [
                    "company_id",
                    "company_name",
                    "year",
                    "free_cash_flow",
                    "cfo_quality_score",
                    "cfo_quality_label",
                    "capex_label",
                    "distress_flag",
                    "capital_allocation_label",
                ]
            ].head(20)
        )

        print("\nSummary")

        print("Total Records :", len(df))
        print("High Quality :", (df["cfo_quality_label"] == "High Quality").sum())
        print("Moderate :", (df["cfo_quality_label"] == "Moderate").sum())
        print("Accrual Risk :", (df["cfo_quality_label"] == "Accrual Risk").sum())
        print("Distress Companies :", (df["distress_flag"] == "Yes").sum())


if __name__ == "__main__":
    CashFlowIntelligence().run()