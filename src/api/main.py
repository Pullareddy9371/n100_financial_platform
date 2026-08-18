import os
from fastapi import FastAPI
import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

app = FastAPI(
    title="N100 Financial Intelligence API",
    description="REST API for N100 Financial Intelligence Platform",
    version="1.0.0"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


@app.get("/")
def home():
    return {
        "message": "N100 Financial Intelligence API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/companies")
def get_companies():
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            id,
            company_name,
            website,
            roe_percentage,
            roce_percentage
        FROM companies
        ORDER BY id
        """,
        conn
    )

    conn.close()

    return df.fillna("").to_dict(orient="records")

@app.get("/companies/{company_id}")
def get_company(company_id: str):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            id,
            company_name,
            website,
            about_company,
            roe_percentage,
            roce_percentage,
            book_value
        FROM companies
        WHERE id = ?
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    if df.empty:
        return {
            "error": "Company not found",
            "company_id": company_id
        }

    return df.fillna("").to_dict(orient="records")[0]


@app.get("/companies/{company_id}/ratios")
def get_company_ratios(company_id: str):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df.fillna("").to_dict(orient="records")


@app.get("/companies/{company_id}/profit-loss")
def get_profit_loss(company_id: str):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df.fillna("").to_dict(orient="records")


@app.get("/companies/{company_id}/balance-sheet")
def get_balance_sheet(company_id: str):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df.fillna("").to_dict(orient="records")


@app.get("/companies/{company_id}/cash-flow")
def get_cash_flow(company_id: str):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df.fillna("").to_dict(orient="records")
@app.get("/sectors")
def get_sectors():
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            broad_sector,
            COUNT(DISTINCT company_id) AS company_count
        FROM sectors
        WHERE broad_sector IS NOT NULL
        GROUP BY broad_sector
        ORDER BY broad_sector
        """,
        conn
    )

    conn.close()

    return df.fillna("").to_dict(orient="records")


@app.get("/companies/{company_id}/sector")
def get_company_sector(company_id: str):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            company_id,
            broad_sector,
            sub_sector,
            index_weight_pct,
            market_cap_category
        FROM sectors
        WHERE company_id = ?
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df.fillna("").to_dict(orient="records")
@app.get("/companies/{company_id}/valuation")
def get_valuation(company_id: str):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    if df.empty:
        return {
            "error": "Valuation data not found",
            "company_id": company_id
        }

    row = df.iloc[0]

    return {
        "company_id": company_id,
        "year": row["year"],
        "free_cash_flow_cr": row["free_cash_flow_cr"],
        "debt_to_equity": row["debt_to_equity"],
        "return_on_equity_pct": row["return_on_equity_pct"]
    }
@app.get("/companies/{company_id}/capital-allocation")
def get_capital_allocation(company_id: str):
    try:
        df = pd.read_csv(
            "src/output/capital_allocation.csv"
        )

        df = df[
            df["company_id"].astype(str).str.upper()
            == company_id.upper()
        ]

        return df.fillna("").to_dict(orient="records")

    except FileNotFoundError:
        return {
            "error": "Capital allocation file not found"
        }
@app.get("/companies/{company_id}/cluster")
def get_cluster(company_id: str):
    try:
        df = pd.read_csv(
            "src/output/cluster_labels.csv"
        )

        df = df[
            df["company_id"].astype(str).str.upper()
            == company_id.upper()
        ]

        if df.empty:
            return {
                "error": "Cluster data not found",
                "company_id": company_id
            }

        return df.fillna("").to_dict(orient="records")[0]

    except FileNotFoundError:
        return {
            "error": "Cluster labels file not found"
        }
@app.get("/companies/{company_id}/cashflow-intelligence")
def get_cashflow_intelligence(company_id: str):
    try:
        df = pd.read_excel(
            "src/output/cashflow_intelligence.xlsx"
        )

        df = df[
            df["company_id"].astype(str).str.upper()
            == company_id.upper()
        ]

        if df.empty:
            return {
                "error": "Cash flow intelligence data not found",
                "company_id": company_id
            }

        return df.fillna("").to_dict(orient="records")

    except FileNotFoundError:
        return {
            "error": "Cash flow intelligence file not found"
        }
@app.get("/companies/{company_id}/pros-cons")
def get_pros_cons(company_id: str):
    try:
        df = pd.read_csv(
            "src/output/pros_cons_generated.csv"
        )

        df = df[
            df["company_id"].astype(str).str.upper()
            == company_id.upper()
        ]

        if df.empty:
            return {
                "error": "Pros and cons data not found",
                "company_id": company_id
            }

        return df.fillna("").to_dict(orient="records")

    except FileNotFoundError:
        return {
            "error": "Pros and cons file not found"
        }
@app.get("/companies/{company_id}/report")
def get_report(company_id: str):
    report_path = (
        f"reports/tearsheets/"
        f"{company_id}_tearsheet.pdf"
    )

    if os.path.exists(report_path):
        return {
            "company_id": company_id,
            "report": report_path,
            "status": "available"
        }

    return {
        "company_id": company_id,
        "status": "not_available"
    }