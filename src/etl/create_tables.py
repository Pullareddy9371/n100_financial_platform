import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")
SCHEMA_PATH = Path("db/schema.sql")


def create_tables():

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r") as file:
        conn.executescript(file.read())

    conn.commit()

    print("Tables created successfully!")

    conn.close()


if __name__ == "__main__":
    create_tables()