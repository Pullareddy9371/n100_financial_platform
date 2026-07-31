# 📊 N100 Financial Intelligence Platform

A comprehensive Financial Intelligence Dashboard developed using **Python, SQLite, Streamlit, Pandas, and Plotly**. This project provides an end-to-end solution for analyzing Nifty 100 companies through financial analytics, stock screening, peer comparison, valuation analysis, sector insights, and interactive dashboards.

---

# Project Overview

The N100 Financial Intelligence Platform is designed to help investors, analysts, and learners explore the financial performance of Nifty 100 companies.

The project includes:

- Data Engineering (ETL)
- SQLite Database Management
- Financial Ratio Analytics
- Stock Screening
- Peer Comparison
- Valuation Analytics
- Interactive Streamlit Dashboard
- CSV & Excel Report Generation

---

# Project Modules

| Module | Status |
|---------|--------|
| ✅ ETL Pipeline | Completed |
| ✅ SQLite Database | Completed |
| ✅ Financial Ratio Analytics | Completed |
| ✅ Stock Screener | Completed |
| ✅ Peer Comparison | Completed |
| ✅ Financial Trends | Completed |
| ✅ Sector Analysis | Completed |
| ✅ Capital Allocation | Completed |
| ✅ Reports Module | Completed |
| ✅ Valuation Analytics | Completed |
| ✅ Interactive Dashboard | Completed |

---

# Dashboard Pages

## 🏠 Home Dashboard

Displays:

- Total Companies
- Average ROE
- Average Debt to Equity
- Average Net Profit Margin
- Asset Turnover
- Sector Distribution
- KPI Cards

---

## 🏢 Company Profile

Displays:

- Company Details
- ROE
- ROCE
- Book Value
- Company Overview

---

## 🔍 Stock Screener

Supports filtering by:

- Company Name
- Sector
- PE Ratio
- PB Ratio
- ROE
- Debt to Equity
- Market Capitalization

---

## 🤝 Peer Comparison

Compare companies based on:

- ROE
- Net Profit Margin
- PE Ratio
- PB Ratio
- Debt to Equity
- Interest Coverage

---

## 📈 Financial Trends

Interactive visualizations of:

- Revenue Trend
- Profit Trend
- ROE Trend
- Margin Trend

---

## 🏭 Sector Analysis

Provides:

- Sector Distribution
- Company Count
- Market Cap Category
- Sector Comparison

---

## 💰 Capital Allocation

Displays:

- Free Cash Flow
- Capital Expenditure
- Operating Cash Flow
- Debt Analysis

---

## 📑 Reports

Generate and download:

- CSV Reports
- Excel Reports

---

## 💎 Valuation Dashboard

Calculates:

- Free Cash Flow Yield
- Sector Median PE
- Sector Median PB
- Dividend Yield
- Valuation Classification

Categories:

- Discount
- Fair
- Caution
- Unknown

---

# Technologies Used

- Python 3.11
- Streamlit
- Pandas
- SQLite
- Plotly
- OpenPyXL
- Matplotlib
- PyYAML
- Pytest
- Git
- GitHub

---

# Project Structure

```
n100_financial_platform
│
├── config/
│
├── data/
│   ├── raw/
│   └── supporting_datasets/
│
├── db/
│   └── nifty100.db
│
├── reports/
│
├── src/
│   ├── analytics/
│   ├── dashboard/
│   │   ├── app.py
│   │   └── pages/
│   ├── etl/
│   ├── output/
│   ├── screener/
│   └── utils/
│
├── tests/
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Database Tables

- Companies
- Financial Ratios
- Market Capitalization
- Sectors
- Balance Sheet
- Profit & Loss
- Cash Flow
- Documents
- Analysis
- Pros & Cons
- Peer Groups
- Stock Prices

---

# Features

- Interactive Streamlit Dashboard
- Financial Ratio Analysis
- KPI Cards
- Stock Screening
- Peer Comparison
- Company Search
- Sector Filters
- Financial Trend Analysis
- Capital Allocation Analysis
- Valuation Engine
- CSV Export
- Excel Export
- Interactive Plotly Charts

---

# Analytics Performed

- Profitability Analysis
- Liquidity Analysis
- Solvency Analysis
- Efficiency Analysis
- Growth Analysis
- Valuation Analysis
- Free Cash Flow Yield
- Sector Median PE & PB Analysis
- Dividend Yield Analysis

---

# Output Files

Generated reports include:

- profitability_ratios.csv
- liquidity_ratios.csv
- solvency_ratios.csv
- growth_ratios.csv
- valuation_ratios.csv
- efficiency_ratios.csv
- financial_metrics.csv
- analytics_summary.csv
- screener_output.xlsx
- peer_comparison.xlsx
- valuation_flags.csv
- valuation_summary.xlsx

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Pullareddy9371/n100_financial_platform.git
```

Move into the project:

```bash
cd n100_financial_platform
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run Analytics

```bash
python -m src.analytics.valuation
```

---

# Run Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

# Testing

Run all tests:

```bash
pytest
```

All project modules were tested successfully.

---

# Learning Outcomes

This project demonstrates practical skills in:

- Python Programming
- Data Engineering
- Financial Analytics
- SQLite Database Design
- Pandas Data Processing
- Streamlit Dashboard Development
- Plotly Visualization
- Report Automation
- Data Validation
- Git & GitHub
- Debugging and Testing

---

# Future Enhancements

- Live Stock Market API Integration
- Machine Learning-based Stock Prediction
- Portfolio Tracking
- User Authentication
- Cloud Deployment (AWS/Azure)
- AI-powered Investment Recommendations

---

# Author

**Pulla Reddy Onteddu**

**B.Tech – Artificial Intelligence & Machine Learning**

GitHub Repository:

https://github.com/Pullareddy9371/n100_financial_platform

---

# License

This project was developed for educational, internship, and portfolio purposes.