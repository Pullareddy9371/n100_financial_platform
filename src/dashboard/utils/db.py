import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_table(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


def get_companies():
    return load_table("companies")


def get_ratios():
    return load_table("financial_ratios")


def get_sectors():
    return load_table("sectors")


def get_market_cap():
    return load_table("market_cap")