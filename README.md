# 📊 N100 Financial Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)
![Pytest](https://img.shields.io/badge/Testing-Pytest-red)
![GitHub](https://img.shields.io/badge/Version%20Control-GitHub-black)

---

# Project Overview

The **N100 Financial Intelligence Platform** is an end-to-end Financial Data Engineering project developed during the **Bluestock Fintech Internship**.

The platform automates the extraction, validation, transformation, storage, and analysis of financial datasets for Nifty 100 companies. It combines ETL processes with financial analytics to generate meaningful Key Performance Indicators (KPIs) and business insights.

---

# Project Objectives

- Extract financial datasets from Excel files
- Clean and normalize financial data
- Validate data quality
- Store processed data in SQLite
- Calculate financial ratios and KPIs
- Generate analytical reports
- Export business insights
- Perform automated testing
- Maintain version control using Git and GitHub

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| Data Processing | Pandas |
| Database | SQLite3 |
| Excel Processing | OpenPyXL |
| Testing | Pytest |
| IDE | Visual Studio Code |
| Version Control | Git & GitHub |

---

# Project Architecture

```
Excel Files
      │
      ▼
ETL Pipeline
      │
      ▼
Data Validation
      │
      ▼
Data Normalization
      │
      ▼
SQLite Database
      │
      ▼
Financial Analytics
      │
      ▼
CSV Reports & KPI Outputs
```

---

# Project Structure

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
├── src/
│   ├── analytics/
│   │   ├── ratios.py
│   │   ├── cagr.py
│   │   ├── cashflow_kpis.py
│   │   ├── day08.py
│   │   ├── day09.py
│   │   ├── day10.py
│   │   ├── day11.py
│   │   ├── day12.py
│   │   ├── day13.py
│   │   ├── day14.py
│   │   ├── day15.py
│   │   ├── day16.py
│   │   └── day17.py
│   │
│   ├── etl/
│   │   ├── loader.py
│   │   ├── normaliser.py
│   │   ├── validator.py
│   │   ├── database.py
│   │   ├── data_loader.py
│   │   ├── verify_database.py
│   │   └── manual_review.py
│   │
│   └── output/
│       ├── capital_allocation.csv
│       ├── efficiency_ratios.csv
│       └── ratio_edge_cases.log
│
├── tests/
│
├── requirements.txt
├── main.py
└── README.md
```

---

# Datasets

The platform processes **12 financial datasets**.

| Dataset |
|----------|
| Analysis |
| Balance Sheet |
| Cash Flow |
| Companies |
| Documents |
| Financial Ratios |
| Market Cap |
| Peer Groups |
| Profit & Loss |
| Pros and Cons |
| Sectors |
| Stock Prices |

---

# ETL Workflow

1. Load Excel datasets
2. Normalize column names
3. Validate datasets
4. Detect duplicate records
5. Handle missing values
6. Create SQLite database
7. Load datasets into database
8. Verify loaded tables
9. Generate validation reports

---

# Data Validation

The following quality checks are performed:

- Duplicate row detection
- Duplicate ID detection
- Missing value detection
- Negative value detection
- Data type verification
- Row count verification
- Database integrity checks

---

# Financial Analytics

## Profitability Ratios

- Net Profit Margin
- Operating Profit Margin
- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Return on Assets (ROA)

---

## Liquidity Ratios

- Current Ratio
- Quick Ratio
- Cash Ratio

---

## Efficiency Ratios

- Asset Turnover Ratio
- Fixed Asset Turnover
- Investment Turnover

---

## Leverage Ratios

- Debt to Equity Ratio
- Interest Coverage Ratio

---

## CAGR Analysis

- Revenue CAGR
- Profit CAGR
- EPS CAGR

---

## Cash Flow KPIs

- Free Cash Flow
- CFO Quality Score
- CapEx Intensity
- FCF Conversion Rate
- Cash Flow Pattern Analysis

---

# Outputs Generated

The project generates the following outputs:

- capital_allocation.csv
- efficiency_ratios.csv
- ratio_edge_cases.log

---

# Database

SQLite Database:

```
db/nifty100.db
```

Database Tables:

- analysis
- balancesheet
- cashflow
- companies
- documents
- financial_ratios
- market_cap
- peer_groups
- profitandloss
- prosandcons
- sectors
- stock_prices

---

# Testing

Unit testing is implemented using **Pytest**.

Run all tests:

```bash
python -m pytest
```

Example Output

```
========= test session starts =========

9 passed

==============================
```

---

# Running the Project

### Load Data

```bash
python -m src.etl.data_loader
```

### Verify Database

```bash
python -m src.etl.verify_database
```

### Run Analytics

```bash
python -m src.analytics.day08
python -m src.analytics.day09
python -m src.analytics.day10
python -m src.analytics.day11
python -m src.analytics.day12
python -m src.analytics.day13
python -m src.analytics.day14
python -m src.analytics.day15
python -m src.analytics.day16
python -m src.analytics.day17
```

---

# Project Highlights

- End-to-End ETL Pipeline
- Financial Data Validation
- SQLite Database Integration
- Financial KPI Engine
- CAGR Analysis
- Cash Flow Analysis
- Automated Testing
- Git Version Control
- Business Analytics Reports

---

# Future Enhancements

- Power BI Dashboard
- Streamlit Web Application
- REST API Integration
- Automated Data Refresh
- Cloud Deployment (AWS/Azure)

---

# Author

**Pulla Reddy Onteddu**

B.Tech – Artificial Intelligence & Machine Learning

Bluestock Fintech Internship

GitHub: https://github.com/Pullareddy9371/n100_financial_platform

---

# License

This project is developed for educational and internship purposes.