import sqlite3


def test_database_exists():

    conn = sqlite3.connect("db/nifty100.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = {
        row[0]
        for row in cursor.fetchall()
    }

    conn.close()

    expected = {
        "companies",
        "analysis",
        "balancesheet",
        "cashflow",
        "documents",
        "profitandloss",
        "prosandcons",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "sectors",
        "stock_prices",
        "peer_percentiles"
    }

    assert expected.issubset(tables)