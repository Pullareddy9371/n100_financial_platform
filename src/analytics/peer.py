import sqlite3
import pandas as pd
import os

DB_PATH = "db/nifty100.db"


class PeerEngine:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def load_data(self):

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        sectors = pd.read_sql(
            "SELECT * FROM sectors",
            self.conn
        )

        df = ratios.merge(
            sectors,
            on="company_id",
            how="left"
        )

        return df

    def calculate_percentiles(self, df):

        metrics = [
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover"
        ]

        results = []

        for sector in df["broad_sector"].dropna().unique():

            temp = df[df["broad_sector"] == sector].copy()

            for metric in metrics:

                if metric not in temp.columns:
                    continue

                if metric == "debt_to_equity":

                    temp["percentile_rank"] = (
                        1 -
                        temp[metric].rank(pct=True)
                    ) * 100

                else:

                    temp["percentile_rank"] = (
                        temp[metric].rank(pct=True)
                    ) * 100

                x = temp[
                    [
                        "company_id",
                        "year",
                        "broad_sector"
                    ]
                ].copy()

                x["metric"] = metric
                x["value"] = temp[metric]
                x["percentile_rank"] = temp["percentile_rank"]

                results.append(x)

        final = pd.concat(results)

        return final

    def save(self, df):

        os.makedirs("src/output", exist_ok=True)

        df.to_csv(
            "src/output/peer_percentiles.csv",
            index=False
        )

        df.to_sql(
            "peer_percentiles",
            self.conn,
            if_exists="replace",
            index=False
        )

        print("\nPeer percentiles saved successfully.")

    def run(self):

        df = self.load_data()

        result = self.calculate_percentiles(df)
        print(result.dtypes)

        self.save(result)

        print(result.head(20))


if __name__ == "__main__":

    PeerEngine().run()
