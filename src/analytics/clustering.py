import os
import sqlite3

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


DB_PATH = "db/nifty100.db"
OUTPUT_PATH = "src/output/cluster_labels.csv"


def load_data():
    """Load exactly one latest financial record for each company."""

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        company_id,
        company_name,
        return_on_equity_pct,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        debt_to_equity,
        interest_coverage,
        asset_turnover,
        free_cash_flow_cr
    FROM (
        SELECT
            c.id AS company_id,
            c.company_name,
            r.return_on_equity_pct,
            r.net_profit_margin_pct,
            r.operating_profit_margin_pct,
            r.debt_to_equity,
            r.interest_coverage,
            r.asset_turnover,
            r.free_cash_flow_cr,

            ROW_NUMBER() OVER (
                PARTITION BY UPPER(TRIM(c.id))
                ORDER BY r.year DESC, r.id DESC
            ) AS row_num

        FROM companies c

        INNER JOIN financial_ratios r
            ON UPPER(TRIM(c.id)) =
               UPPER(TRIM(r.company_id))
    )
    WHERE row_num = 1
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

def prepare_data(df):
    """Clean and prepare financial features."""

    features = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
    ]

    # Normalize company ID
    df["company_id"] = (
        df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Convert financial columns to numeric
    for column in features:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Replace missing values with median
    for column in features:
        median_value = df[column].median()

        df[column] = df[column].fillna(
            median_value
        )

    return df, features


def create_clusters(df, features):
    """Create financial clusters using KMeans."""

    scaler = StandardScaler()

    X = scaler.fit_transform(
        df[features]
    )

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    df["cluster"] = model.fit_predict(X)

    return df


def create_cluster_labels(df):
    """Convert numeric clusters into readable labels."""

    cluster_scores = (
        df.groupby("cluster")[
            "return_on_equity_pct"
        ]
        .mean()
        .sort_values()
    )

    labels = [
        "Low Profitability",
        "Moderate",
        "Balanced",
        "Strong",
        "High Profitability",
    ]

    label_map = {}

    for cluster_id, label in zip(
        cluster_scores.index,
        labels
    ):
        label_map[cluster_id] = label

    df["cluster_label"] = (
        df["cluster"].map(label_map)
    )

    return df


def save_output(df):
    """Save clustering results."""

    os.makedirs(
        "src/output",
        exist_ok=True
    )

    output = df[
        [
            "company_id",
            "company_name",
            "cluster",
            "cluster_label",
        ]
    ].copy()

    output = output.sort_values(
        "company_id"
    )

    output.to_csv(
        OUTPUT_PATH,
        index=False
    )

    return output


def main():

    print("Starting N100 clustering...")

    # Step 1: Load data
    df = load_data()

    if df.empty:
        raise ValueError(
            "No financial data found in database."
        )

    print(
        "Companies loaded:",
        df["company_id"].nunique()
    )

    # Step 2: Prepare data
    df, features = prepare_data(df)

    # Step 3: Create clusters
    df = create_clusters(
        df,
        features
    )

    # Step 4: Create readable labels
    df = create_cluster_labels(df)

    # Step 5: Save output
    output = save_output(df)

    print(
        "Cluster analysis completed successfully."
    )

    print(
        "Output file:",
        OUTPUT_PATH
    )

    print(
        "Rows generated:",
        len(output)
    )

    print("\nCluster distribution:")

    print(
        output["cluster_label"]
        .value_counts()
    )


if __name__ == "__main__":
    main()