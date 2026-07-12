import sqlite3

from src.etl.loader import load_all_excels

DB_PATH = "db/nifty100.db"


def load_data():

    conn = sqlite3.connect(DB_PATH)

    datasets = load_all_excels()

    for table_name, df in datasets.items():

        print(f"Loading {table_name}...")

        # Convert column names to lowercase
        df.columns = [col.lower() for col in df.columns]

        # Replace spaces with underscores
        df.columns = [col.replace(" ", "_") for col in df.columns]

        # Write to SQLite
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"✓ {len(df)} rows inserted into {table_name}")

    conn.close()

    print("\nAll datasets loaded successfully!")


# 👇 These lines must be at the left margin (no indentation)
if __name__ == "__main__":
    load_data()