import os
import sqlite3
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "reports/portfolio"

styles = getSampleStyleSheet()
class PortfolioSummary:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

        os.makedirs(
            OUTPUT_DIR,
            exist_ok=True
        )

    def load_data(self):
        query = """
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,
            r.year,
            r.return_on_equity_pct,
            r.net_profit_margin_pct,
            r.operating_profit_margin_pct,
            r.debt_to_equity,
            r.interest_coverage,
            r.asset_turnover,
            r.free_cash_flow_cr
        FROM companies c

        LEFT JOIN sectors s
            ON c.id = s.company_id

        LEFT JOIN financial_ratios r
            ON c.id = r.company_id

        ORDER BY
            c.id,
            r.year
        """

        return pd.read_sql(
            query,
            self.conn
        )
    def trend_arrow(
        self,
        current,
        previous
    ):

        if pd.isna(current) or pd.isna(previous):
            return "→"

        if previous == 0:
            return "→"

        change = ((current - previous) / abs(previous)) * 100

        if change > 2:
            return "↑"

        elif change < -2:
            return "↓"

        else:
            return "→"
    def build_company_page(
        self,
        story,
        company_df
    ):

        latest = company_df.iloc[-1]

        previous = (
            company_df.iloc[-2]
            if len(company_df) > 1
            else latest
        )

        story.append(

            Paragraph(

                f"<b><font size=18>{latest['company_name']}</font></b>",

                styles["Title"]

            )

        )

        story.append(Spacer(1, 8))

        story.append(

            Paragraph(

                f"<b>Sector:</b> {latest['broad_sector']}",

                styles["BodyText"]

            )

        )

        story.append(Spacer(1, 10))

        table_data = [

            ["Metric", "Value", "Trend"],

            [
                "ROE",
                latest["return_on_equity_pct"],
                self.trend_arrow(
                    latest["return_on_equity_pct"],
                    previous["return_on_equity_pct"]
                )
            ],

            [
                "Net Profit Margin",
                latest["net_profit_margin_pct"],
                self.trend_arrow(
                    latest["net_profit_margin_pct"],
                    previous["net_profit_margin_pct"]
                )
            ],

            [
                "Operating Margin",
                latest["operating_profit_margin_pct"],
                self.trend_arrow(
                    latest["operating_profit_margin_pct"],
                    previous["operating_profit_margin_pct"]
                )
            ],

            [
                "Debt / Equity",
                latest["debt_to_equity"],
                self.trend_arrow(
                    latest["debt_to_equity"],
                    previous["debt_to_equity"]
                )
            ],

            [
                "Interest Coverage",
                latest["interest_coverage"],
                self.trend_arrow(
                    latest["interest_coverage"],
                    previous["interest_coverage"]
                )
            ],

            [
                "Free Cash Flow",
                latest["free_cash_flow_cr"],
                self.trend_arrow(
                    latest["free_cash_flow_cr"],
                    previous["free_cash_flow_cr"]
                )
            ]
        ]

        table = Table(table_data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

                ("TEXTCOLOR", (0,0), (-1,0), colors.white),

                ("GRID", (0,0), (-1,-1), 1, colors.black),

                ("BACKGROUND", (0,1), (-1,-1), colors.beige),

                ("ALIGN", (0,0), (-1,-1), "CENTER"),

                ("WORDWRAP", (0,0), (-1,-1), True)

            ])

        )

        story.append(table)

        story.append(PageBreak())
    def generate_pdf(self):

        df = self.load_data()

        output = os.path.join(
            OUTPUT_DIR,
            "portfolio_summary.pdf"
        )

        story = []

        companies = sorted(
            df["id"].dropna().unique()
        )

        for company in companies:

            company_df = (
                df[df["id"] == company]
                .sort_values("year")
            )

            if company_df.empty:
                continue

            self.build_company_page(
                story,
                company_df
            )

        pdf = SimpleDocTemplate(
            output,
            pagesize=A4
        )

        pdf.build(story)

        print("\nPortfolio Summary Generated Successfully!")
        print("PDF :", output)
    def run(self):

        self.generate_pdf()

        print("\nDay 35 Completed Successfully!")
if __name__ == "__main__":
    PortfolioSummary().run()