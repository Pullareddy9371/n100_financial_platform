import pandas as pd


def clean_column_names(df):
    """
    Convert column names to lowercase and replace spaces with underscores.
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def normalize_year(df, column="year"):
    """
    Convert year column to integer.
    """
    df[column] = df[column].astype(int)
    return df


def normalize_ticker(df, column="ticker"):
    """
    Convert ticker symbols to uppercase.
    """
    df[column] = df[column].str.upper().str.strip()
    return df


def remove_duplicates(df):
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates()