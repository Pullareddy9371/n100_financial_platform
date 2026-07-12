import pandas as pd


def check_null_values(df):
    """
    Check for null values.
    """
    return df.isnull().sum()


def check_duplicate_rows(df):
    """
    Count duplicate rows.
    """
    return df.duplicated().sum()


def check_duplicate_ids(df):
    """
    Check duplicate values in the id column.
    """
    if "id" not in df.columns:
        return 0

    return df["id"].duplicated().sum()


def check_negative_numbers(df):
    """
    Check negative values in numeric columns.
    """
    numeric_columns = df.select_dtypes(include="number").columns

    negatives = {}

    for column in numeric_columns:
        negatives[column] = (df[column] < 0).sum()

    return negatives


def validate_dataset(name, df):

    print(f"\n{name}")
    print("-" * 60)

    print("Duplicate Rows :", check_duplicate_rows(df))
    print("Duplicate IDs  :", check_duplicate_ids(df))

    print("\nNull Values")
    print(check_null_values(df))

    print("\nNegative Values")
    print(check_negative_numbers(df))