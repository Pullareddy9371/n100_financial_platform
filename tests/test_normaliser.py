import pandas as pd
from src.etl.normaliser import clean_column_names


def test_clean_column_names():

    df = pd.DataFrame(
        columns=[
            "Company Name",
            "Market Cap",
            "P/E Ratio"
        ]
    )

    cleaned = clean_column_names(df)

    assert list(cleaned.columns) == [
        "company_name",
        "market_cap",
        "p/e_ratio"
    ]