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
    TableStyle
)

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "reports/sector"

styles = getSampleStyleSheet()
class SectorReport:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

        os.makedirs(
            OUTPUT_DIR,
            exist_ok=True
        )

    def load_sector(self, sector):
        query = f"""
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,
            r.return_on_equity_pct,
            r.net_profit_margin_pct,
            r.operating_profit_margin_pct,
            r.debt_to_equity,
            r.interest_coverage,
            r.asset_turnover,
            r.free_cash_flow_cr
        FROM companies c
        INNER JOIN sectors s
            ON c.id = s.company_id
        LEFT JOIN financial_ratios r
            ON c.id = r.company_id
        WHERE s.broad_sector = '{sector}'
        """

        return pd.read_sql(query, self.conn)

    def generate_sector_pdf(self, sector):

        df = self.load_sector(sector)

        if df.empty:
            print(f"{sector} : No Data")
            return

        output = os.path.join(
            OUTPUT_DIR,
            f"{sector}_report.pdf"
        )

        story = []

        # Title
        story.append(
            Paragraph(
                f"<b><font size=18>{sector} Sector Report</font></b>",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 15))

        # Summary
        story.append(
            Paragraph(
                "<b>Sector Median KPIs</b>",
                styles["Heading2"]
            )
        )

        summary = [
            [
                "Metric",
                "Median"
            ],
            [
                "ROE",
                round(df["return_on_equity_pct"].median(), 2)
            ],
            [
                "Net Profit Margin",
                round(df["net_profit_margin_pct"].median(), 2)
            ],
            [
                "Operating Margin",
                round(df["operating_profit_margin_pct"].median(), 2)
            ],
            [
                "Debt / Equity",
                round(df["debt_to_equity"].median(), 2)
            ],
            [
                "Interest Coverage",
                round(df["interest_coverage"].median(), 2)
            ],
            [
                "Asset Turnover",
                round(df["asset_turnover"].median(), 2)
            ]
        ]

        table = Table(summary)

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
                    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                    ("GRID", (0,0), (-1,-1), 1, colors.black),
                    ("BACKGROUND", (0,1), (-1,-1), colors.beige),
                    ("ALIGN", (0,0), (-1,-1), "CENTER"),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 6)
                ]
            )
        )

        story.append(table)

        story.append(Spacer(1, 20))
                # Company Details
        story.append(
            Paragraph(
                "<b>Companies in this Sector</b>",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 10))

        company_table = [[
            "Company",
            "ROE",
            "NPM",
            "OPM",
            "D/E",
            "ICR",
            "ATO",
            "FCF"
        ]]

        for _, row in df.iterrows():

            company_table.append([
                str(row["company_name"]),

                round(row["return_on_equity_pct"], 2)
                if pd.notna(row["return_on_equity_pct"]) else "-",

                round(row["net_profit_margin_pct"], 2)
                if pd.notna(row["net_profit_margin_pct"]) else "-",

                round(row["operating_profit_margin_pct"], 2)
                if pd.notna(row["operating_profit_margin_pct"]) else "-",

                round(row["debt_to_equity"], 2)
                if pd.notna(row["debt_to_equity"]) else "-",

                round(row["interest_coverage"], 2)
                if pd.notna(row["interest_coverage"]) else "-",

                round(row["asset_turnover"], 2)
                if pd.notna(row["asset_turnover"]) else "-",

                round(row["free_cash_flow_cr"], 2)
                if pd.notna(row["free_cash_flow_cr"]) else "-"
            ])

        table = Table(
            company_table,
            repeatRows=1
        )

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
                ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
                ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE", (0,0), (-1,-1), 8),
                ("ALIGN", (1,1), (-1,-1), "CENTER"),
                ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                ("WORDWRAP", (0,0), (-1,-1), True)
            ])
        )

        story.append(table)

        pdf = SimpleDocTemplate(
            output,
            pagesize=A4
        )

        pdf.build(story)

        print(f"{sector} Report Generated")

    def run(self):

        sectors = pd.read_sql(
    """
    SELECT DISTINCT broad_sector
    FROM sectors
    WHERE broad_sector IS NOT NULL
    ORDER BY broad_sector
    """,
    self.conn
)
        generated = 0

        for sector in sectors["broad_sector"]:

            try:

                self.generate_sector_pdf(sector)

                generated += 1

            except Exception as e:

                print(f"{sector} Failed : {e}")

        print("\nSector Report Generation Completed")

        print("Total Sector Reports :", generated)


if __name__ == "__main__":
    SectorReport().run()