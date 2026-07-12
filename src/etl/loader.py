from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw")

# Files that contain a title row before the actual header
SPECIAL_FILES = {
    "companies.xlsx",
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx"
}


def load_excel(file_path):
    """
    Load an Excel file with the correct header.
    """

    try:

        if file_path.name in SPECIAL_FILES:
            df = pd.read_excel(file_path, header=1)
        else:
            df = pd.read_excel(file_path)

        return df

    except Exception as e:
        print(f"Error loading {file_path.name}: {e}")
        return None


def load_all_excels():

    datasets = {}

    for excel_file in RAW_DATA_PATH.rglob("*.xlsx"):

        df = load_excel(excel_file)

        if df is not None:
            datasets[excel_file.stem] = df

    return datasets


def display_summary(datasets):

    print("=" * 70)
    print("N100 Financial Intelligence Platform")
    print("=" * 70)

    for name, df in datasets.items():

        print(f"\nDataset : {name}")
        print(f"Rows     : {df.shape[0]}")
        print(f"Columns  : {df.shape[1]}")
        print(f"Column Names : {list(df.columns)}")
        print("-" * 70)


if __name__ == "__main__":

    datasets = load_all_excels()

    display_summary(datasets)

    print(f"\nTotal datasets loaded : {len(datasets)}")