import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")


def create_connection():
    """
    Create a SQLite database connection.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    print("Database connected successfully!")

    return conn


if __name__ == "__main__":
    connection = create_connection()
    connection.close()