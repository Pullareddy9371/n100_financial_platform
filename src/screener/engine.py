import sqlite3
import pandas as pd
import yaml
from src.screener.presets import PresetScreeners
from src.screener.export_excel import ScreenerExporter

DB_PATH = "db/nifty100.db"


class ScreenerEngine:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

        with open("config/screener_config.yaml", "r") as file:
            self.config = yaml.safe_load(file)

    def load_data(self):

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        companies = pd.read_sql(
            "SELECT * FROM companies",
            self.conn
        )

        sectors = pd.read_sql(
            "SELECT * FROM sectors",
            self.conn
        )

        market = pd.read_sql(
            "SELECT * FROM market_cap",
            self.conn
        )

        print("financial_ratios :", len(ratios))
        print("companies        :", len(companies))
        print("sectors          :", len(sectors))
        print("market_cap       :", len(market))

        df = ratios.copy()

        print("\nStart:", len(df))

        df = df.merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left"
        )

        print("After companies merge:", len(df))

        df = df.merge(
            sectors,
            on="company_id",
            how="left"
        )

        print("After sectors merge:", len(df))

        market = (
            market.sort_values("year")
                  .drop_duplicates(subset="company_id", keep="last")
        )

        df = df.merge(
            market,
            on="company_id",
            how="left",
            suffixes=("", "_market")
        )

        print("After market merge:", len(df))

        return df

    def apply_filters(self, df):

     cfg = self.config

     print("\nBefore Filters :", len(df))

    # ROE
     if "return_on_equity_pct" in df.columns:
        df = df[df["return_on_equity_pct"] >= cfg["roe_min"]]
        print("After ROE :", len(df))

    # Debt to Equity
     if "debt_to_equity" in df.columns:
        df = df[df["debt_to_equity"] <= cfg["de_max"]]
        print("After Debt to Equity :", len(df))

    # Free Cash Flow
     if "free_cash_flow_cr" in df.columns:
        df = df[df["free_cash_flow_cr"] >= cfg["fcf_min"]]
        print("After Free Cash Flow :", len(df))

    # Interest Coverage
     if "interest_coverage" in df.columns:
        df = df[df["interest_coverage"] >= cfg["icr_min"]]
        print("After Interest Coverage :", len(df))

    # Asset Turnover
     if "asset_turnover" in df.columns:
        df = df[df["asset_turnover"] >= cfg["asset_turnover_min"]]
        print("After Asset Turnover :", len(df))

    # Market Cap
     if "market_cap_crore" in df.columns:
        df = df[df["market_cap_crore"] >= cfg["market_cap_min"]]
        print("After Market Cap :", len(df))

    # PE Ratio
     if "pe_ratio" in df.columns:
        df = df[df["pe_ratio"] <= cfg["pe_max"]]
        print("After PE Ratio :", len(df))

    # PB Ratio
     if "pb_ratio" in df.columns:
        df = df[df["pb_ratio"] <= cfg["pb_max"]]
        print("After PB Ratio :", len(df))

    # Dividend Yield
     if "dividend_yield_pct" in df.columns:
        df = df[df["dividend_yield_pct"] >= cfg["dividend_yield_min"]]
        print("After Dividend Yield :", len(df))

     return df

    def add_score(self, df):

     df["composite_quality_score"] = (
        (df["return_on_equity_pct"].fillna(0) * 0.4) +
        (df["net_profit_margin_pct"].fillna(0) * 0.3) +
        (df["operating_profit_margin_pct"].fillna(0) * 0.3)
    )

    # Scale score to 0–100
     max_score = df["composite_quality_score"].max()

     if max_score > 0:
        df["composite_quality_score"] = (
            df["composite_quality_score"] / max_score
        ) * 100

     return df.sort_values(
        "composite_quality_score",
        ascending=False
    )
    def run_presets(self, df):

        presets = {

            "Quality Compounder":
                PresetScreeners.quality_compounder(df),

            "Value Pick":
                PresetScreeners.value_pick(df),

            "Growth Accelerator":
                PresetScreeners.growth_accelerator(df),

            "Dividend Champion":
                PresetScreeners.dividend_champion(df),

            "Debt Free Bluechip":
                PresetScreeners.debt_free_bluechip(df),

            "Turnaround Watch":
                PresetScreeners.turnaround_watch(df)

        }

        print("\nPreset Screener Results")
        print("=" * 45)

        for name, data in presets.items():
            print(f"{name} : {len(data)} Companies")

        return presets

    def run(self):

        df = self.load_data()

        print("\nTotal Companies:", len(df))

        df = self.apply_filters(df)

        print("After Filters:", len(df))

        df = self.add_score(df)
        presets = self.run_presets(df)
        ScreenerExporter.export(presets)

        print(
            df[
                [
                    "company_id",
                    "company_name",
                    "year",
                    "return_on_equity_pct",
                    "debt_to_equity",
                    "free_cash_flow_cr",
                    "composite_quality_score"
                ]
            ].head(20)
        )

        return df


if __name__ == "__main__":

    engine = ScreenerEngine()

    engine.run()