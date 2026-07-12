# N100 Financial Intelligence Platform

## Project Overview

The N100 Financial Intelligence Platform is an ETL (Extract, Transform, Load) project developed as part of the Bluestock Fintech Internship. The project processes financial datasets of Nifty 100 companies by extracting Excel files, validating and normalizing the data, and loading it into a SQLite database for further analysis.

---

## Project Objectives

- Extract financial datasets from Excel files.
- Normalize dataset column names.
- Validate data quality.
- Load cleaned data into a SQLite database.
- Generate audit and validation reports.
- Test the ETL pipeline using Pytest.

---

## Technologies Used

- Python 3.11
- Pandas
- SQLite3
- OpenPyXL
- Pytest
- Git & GitHub

---

## Project Structure

```
n100_financial_platform/
│
├── data/
│   ├── raw/
│   └── supporting_datasets/
│
├── db/
│   └── nifty100.db
│
├── output/
│   ├── load_audit.csv
│   └── validation_failures.csv
│
├── src/
│   └── etl/
│       ├── loader.py
│       ├── normaliser.py
│       ├── validator.py
│       ├── database.py
│       ├── create_tables.py
│       ├── data_loader.py
│       ├── verify_data.py
│       ├── load_audit.py
│       └── validation_report.py
│
├── tests/
│   ├── test_database.py
│   ├── test_loader.py
│   └── test_normaliser.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Workflow

1. Load Excel datasets.
2. Normalize column names.
3. Validate data quality.
4. Create SQLite database.
5. Create database tables.
6. Load datasets into SQLite.
7. Verify database records.
8. Generate audit reports.
9. Run unit tests.

---

## Datasets

- Companies
- Analysis
- Balance Sheet
- Cash Flow
- Profit & Loss
- Documents
- Pros & Cons
- Financial Ratios
- Market Cap
- Peer Groups
- Sectors
- Stock Prices

Total Datasets: **12**

---

## Validation Performed

- Duplicate row detection
- Duplicate ID detection
- Null value detection
- Negative value detection
- Row count verification

---

## Testing

Unit tests were written using Pytest.

```
3 tests passed successfully.
```

---

## Output Files

- load_audit.csv
- validation_failures.csv

---

## Author

**Pulla Reddy Onteddu**

Bluestock Fintech Internship Project