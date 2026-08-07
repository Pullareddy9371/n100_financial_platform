import sqlite3
import os

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "reports/tearsheets"

styles = getSampleStyleSheet()
class TearSheet:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

        os.makedirs(
            OUTPUT_DIR,
            exist_ok=True
        )
    def load_company(self, company_id):

        company = pd.read_sql(
            f"""
            SELECT *
            FROM companies
            WHERE id='{company_id}'
            """,
            self.conn
        )

        pnl = pd.read_sql(
            f"""
            SELECT *
            FROM profitandloss
            WHERE company_id='{company_id}'
            """,
            self.conn
        )

        balance = pd.read_sql(
            f"""
            SELECT *
            FROM balancesheet
            WHERE company_id='{company_id}'
            """,
            self.conn
        )

        cashflow = pd.read_sql(
            f"""
            SELECT *
            FROM cashflow
            WHERE company_id='{company_id}'
            """,
            self.conn
        )

        ratios = pd.read_sql(
            f"""
            SELECT *
            FROM financial_ratios
            WHERE company_id='{company_id}'
            """,
            self.conn
        )

        capital = pd.read_csv(
            "src/output/capital_allocation.csv"
        )

        capital = capital[
            capital.company_id == company_id
        ]

        return (
            company,
            pnl,
            balance,
            cashflow,
            ratios,
            capital
        )
    def latest(self, df):

        if len(df) == 0:
            return None

        return df.iloc[-1]
    def draw_header(self, story, company):

        title = company.iloc[0].get("company_name", "N/A")

        table = Table(
            [[title]],
            colWidths=[18*cm]
        )

        table.setStyle(
            TableStyle(
                [

                    ("BACKGROUND",(0,0),(-1,-1),
                     colors.darkblue),

                    ("TEXTCOLOR",(0,0),(-1,-1),
                     colors.white),

                    ("FONTSIZE",(0,0),(-1,-1),
                     22),

                    ("BOTTOMPADDING",(0,0),(-1,-1),
                     12),

                    ("ALIGN",(0,0),(-1,-1),
                     "CENTER")
                ]
            )
        )

        story.append(table)
        story.append(Spacer(1,0.5*cm))

    def kpi_tile(
        self,
        title,
        value
    ):

        t = Table(
            [
                [Paragraph(
                    f"<b>{title}</b>",
                    styles["BodyText"]
                )],

                [Paragraph(
                    str(value),
                    styles["Heading2"]
                )]
            ],
            colWidths=[5.2*cm]
        )

        t.setStyle(

            TableStyle(
                [

                    ("GRID",(0,0),(-1,-1),
                     1,
                     colors.grey),

                    ("BACKGROUND",(0,0),(-1,0),
                     colors.lightgrey),

                    ("ALIGN",(0,0),(-1,-1),
                     "CENTER"),

                    ("BOTTOMPADDING",(0,0),(-1,-1),
                     8)
                ]
            )

        )

        return t
    def kpi_section(
        self,
        story,
        ratios,
        capital
    ):

        latest = self.latest(ratios)

        latest_cap = self.latest(capital)

        if latest_cap is None:
            latest_cap = {}

        kpis = [

            self.kpi_tile(
                "ROE",
                latest.get("return_on_equity_pct", "N/A")
            ),

            self.kpi_tile(
                "Operating Margin",
                latest.get("operating_profit_margin_pct", "N/A")
            ),

            self.kpi_tile(
                "Debt/Equity",
                latest.get("debt_to_equity", "N/A")
            ),

            self.kpi_tile(
                "Interest Coverage",
                latest.get("interest_coverage", "N/A")
            ),

            self.kpi_tile(
                "Asset Turnover",
                latest.get("asset_turnover", "N/A")
            ),

            self.kpi_tile(
                "Capital Allocation",
                latest_cap.get("Pattern", "N/A")
            )

        ]

        table = Table(

            [
                kpis[:3],
                kpis[3:]
            ]

        )

        table.setStyle(

            TableStyle(

                [

                    ("BOTTOMPADDING",(0,0),(-1,-1),8),

                    ("TOPPADDING",(0,0),(-1,-1),8)

                ]

            )

        )

        story.append(table)

        story.append(Spacer(1,0.4*cm))

    def revenue_chart(self, pnl):
        if len(pnl) == 0:
            return None

        years = pnl["year"].astype(str).tail(10)
        revenue = pnl["sales"].tail(10)

        plt.figure(figsize=(5,3))
        plt.bar(years, revenue)
        plt.title("10-Year Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()

        path = "reports/temp_revenue.png"
        plt.savefig(path)
        plt.close()

        return path

    def profit_chart(self, pnl):
        if len(pnl) == 0:
            return None

        years = pnl["year"].astype(str).tail(10)
        profit = pnl["net_profit"].tail(10)

        plt.figure(figsize=(5,3))
        plt.bar(years, profit)
        plt.title("10-Year Net Profit")
        plt.xticks(rotation=45)
        plt.tight_layout()

        path = "reports/temp_profit.png"
        plt.savefig(path)
        plt.close()

        return path

    def roe_roce_chart(self, ratios):
        if len(ratios) == 0:
            return None

        years = ratios["year"].astype(str).tail(10)
        roe = ratios["return_on_equity_pct"].tail(10)
        opm = ratios["operating_profit_margin_pct"].tail(10)

        plt.figure(figsize=(8,4))

        plt.plot(
            years,
            roe,
            marker="o",
            linewidth=2,
            label="ROE"
        )

        plt.plot(
            years,
            opm,
            marker="s",
            linewidth=2,
            label="Operating Margin"
        )

        plt.title("ROE vs Operating Margin")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        path = "reports/temp_roe.png"
        plt.savefig(path)
        plt.close()

        return path

    def page_one_charts(self, story, pnl):
        revenue = self.revenue_chart(pnl)
        profit = self.profit_chart(pnl)

        if revenue and profit:
            table = Table(
                [
                    [
                        Image(revenue, width=8*cm, height=5*cm),
                        Image(profit, width=8*cm, height=5*cm)
                    ]
                ]
            )

            story.append(table)
            story.append(Spacer(1,0.5*cm))

    def roe_section(self, story, ratios):
        chart = self.roe_roce_chart(ratios)

        if chart:
            story.append(
                Image(
                    chart,
                    width=16*cm,
                    height=7*cm
                )
            )

            story.append(
                Spacer(1,0.5*cm)
            )

    def build_page_one(
        self,
        story,
        company,
        pnl,
        ratios,
        capital
    ):

        self.draw_header(
            story,
            company
        )

        self.kpi_section(
            story,
            ratios,
            capital
        )

        self.page_one_charts(
            story,
            pnl
        )

        self.roe_section(
            story,
            ratios
        )

    def balance_chart(self, balance):

        if len(balance) == 0:
            return None

        years = balance["year"].astype(str).tail(10)

        equity = balance["equity_capital"].fillna(0).tail(10)

        borrowings = balance["borrowings"].fillna(0).tail(10)

        liabilities = balance["other_liabilities"].fillna(0).tail(10)

        plt.figure(figsize=(8,4))

        plt.bar(years, equity, label="Equity")

        plt.bar(
            years,
            borrowings,
            bottom=equity,
            label="Borrowings"
        )

        plt.bar(
            years,
            liabilities,
            bottom=equity + borrowings,
            label="Other Liabilities"
        )

        plt.title("Balance Sheet Composition")

        plt.xticks(rotation=45)

        plt.legend()

        plt.tight_layout()

        path = "reports/temp_balance.png"

        plt.savefig(path)

        plt.close()

        return path

    def cashflow_chart(self, cashflow):

        if len(cashflow) == 0:
            return None

        latest = cashflow.iloc[-1]

        labels = [
            "CFO",
            "CFI",
            "CFF",
            "Net Cash"
        ]

        values = [
            latest["operating_activity"],
            latest["investing_activity"],
            latest["financing_activity"],
            latest["net_cash_flow"]
        ]

        plt.figure(figsize=(6,4))

        plt.bar(labels, values)

        plt.title("Cash Flow Waterfall")

        plt.tight_layout()

        path = "reports/temp_cashflow.png"

        plt.savefig(path)

        plt.close()

        return path

    def pros_cons_section(
        self,
        story,
        company_id
    ):
        try:
            pros = pd.read_csv(
                "src/output/pros_cons.csv"
            )

            company = pros[
                pros.company_id == company_id
            ]

            if len(company) > 0:
                pros_text = company.iloc[0]["Pros"]
                cons_text = company.iloc[0]["Cons"]
            else:
                pros_text = "No major strengths"
                cons_text = "No major weaknesses"
        except Exception:
            pros_text = "No data"
            cons_text = "No data"

        story.append(
            Paragraph(
                "<font color='green'><b>Pros</b></font>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                pros_text,
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1,0.3*cm)
        )

        story.append(
            Paragraph(
                "<font color='red'><b>Cons</b></font>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                cons_text,
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1,0.4*cm)
        )

    def capital_badge(
        self,
        story,
        capital
    ):

        if capital is None or len(capital) == 0:
            return

        if capital.empty:
            story.append(
                Paragraph(
                    "<b>Capital Allocation:</b> N/A",
                    styles["BodyText"]
                )
            )
            return

        if capital.empty:
            badge = "N/A"
        else:
            badge = capital.iloc[-1]["Pattern"]

        badge = Table(
            [
                [
                    Paragraph(
                        f"<b>{badge}</b>",
                        styles["Heading2"]
                    )
                ]
            ],
            colWidths=[8*cm]
        )

        badge.setStyle(
            TableStyle(
                [
                    ("BACKGROUND",(0,0),(-1,-1), colors.green),
                    ("TEXTCOLOR",(0,0),(-1,-1), colors.white),
                    ("ALIGN",(0,0),(-1,-1), "CENTER"),
                    ("GRID",(0,0),(-1,-1), 1, colors.black),
                    ("BOTTOMPADDING",(0,0),(-1,-1), 8)
                ]
            )
        )

        story.append(badge)

    def build_page_two(
        self,
        story,
        company,
        balance,
        cashflow,
        capital
    ):
        story.append(PageBreak())

        balance_img = self.balance_chart(balance)

        if balance_img:
            story.append(
                Image(
                    balance_img,
                    width=16*cm,
                    height=7*cm
                )
            )

        cash_img = self.cashflow_chart(cashflow)

        if cash_img:
            story.append(
                Image(
                    cash_img,
                    width=14*cm,
                    height=6*cm
                )
            )

        self.pros_cons_section(
            story,
            company.iloc[0]["id"]
        )

        self.capital_badge(
            story,
            capital
        )

    def generate_pdf(
        self,
        company_id
    ):
        (
            company,
            pnl,
            balance,
            cashflow,
            ratios,
            capital
        ) = self.load_company(company_id)

        # Skip companies with missing required data
        if balance.empty or ratios.empty:
            print(f"{company_id} Skipped : Missing balance sheet or financial ratios")
            return False

        if capital.empty:
            print(f"{company_id} Skipped : Missing capital allocation data")
            return False

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{company_id}_tearsheet.pdf"
        )

        story = []

        self.build_page_one(
            story,
            company,
            pnl,
            ratios,
            capital
        )

        self.build_page_two(
            story,
            company,
            balance,
            cashflow,
            capital
        )

        pdf = SimpleDocTemplate(
            output_file,
            pagesize=A4
        )

        pdf.build(story)

        print(company_id, "Completed")
        return True

    def run(self):
        companies = pd.read_sql(
            """
            SELECT DISTINCT id
            FROM companies
            ORDER BY id
            """,
            self.conn
        )

        skipped = []

        generated = 0

        for company in companies["id"]:

            try:

                result = self.generate_pdf(company)

                if result:
                    generated += 1
                else:
                    skipped.append(company)

            except Exception as e:

                print(f"{company} Failed : {e}")

                skipped.append(company)

        os.makedirs("src/output", exist_ok=True)

        pd.DataFrame(
            skipped,
            columns=["company_id"]
        ).to_csv(
            "src/output/skipped_tearsheets.csv",
            index=False
        )

        print("\nBatch Generation Completed")

        print("Generated :", generated)

        print("Skipped :", len(skipped))
    
if __name__ == "__main__":
    TearSheet().run()