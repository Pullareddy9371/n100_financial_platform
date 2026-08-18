# 📊 N100 Financial Intelligence Platform

A comprehensive Financial Intelligence Platform built using **Python, SQLite, Pandas, Streamlit, Plotly, Matplotlib, and ReportLab**. The platform provides end-to-end financial analysis for Nifty 100 companies, including ETL pipelines, financial ratio analytics, valuation, NLP-based insights, cash flow intelligence, automated PDF reports, sector analysis, and an interactive dashboard.

---

# 🚀 Project Overview

The N100 Financial Intelligence Platform helps investors, analysts, and students analyze the financial performance of Nifty 100 companies using structured financial data and automated analytics.

The platform includes:

- ETL Pipeline
- SQLite Database
- Financial Ratio Engine
- Stock Screener
- Peer Comparison
- Valuation Analytics
- Financial Trend Analysis
- Capital Allocation Intelligence
- NLP-based Pros & Cons Generator
- Cash Flow Intelligence
- Company Tearsheet Reports
- Sector Reports
- Portfolio Summary Report
- Interactive Streamlit Dashboard

---

# ✅ Project Modules

| Module | Status |
|---------|--------|
| ETL Pipeline | ✅ Completed |
| SQLite Database | ✅ Completed |
| Financial Ratio Engine | ✅ Completed |
| Profitability Analytics | ✅ Completed |
| Liquidity Analytics | ✅ Completed |
| Solvency Analytics | ✅ Completed |
| Growth Analytics | ✅ Completed |
| Efficiency Analytics | ✅ Completed |
| Stock Screener | ✅ Completed |
| Peer Comparison | ✅ Completed |
| Valuation Analytics | ✅ Completed |
| Financial Trend Analysis | ✅ Completed |
| Capital Allocation Engine | ✅ Completed |
| NLP Analysis Parser | ✅ Completed |
| Pros & Cons Generator | ✅ Completed |
| Cash Flow Intelligence | ✅ Completed |
| Distress Detection | ✅ Completed |
| Company Tearsheet Reports | ✅ Completed |
| Sector Reports | ✅ Completed |
| Portfolio Summary PDF | ✅ Completed |
| Interactive Dashboard | ✅ Completed |

---

# 📊 Dashboard Features

## 🏠 Home Dashboard

- Total Companies
- Average ROE
- Average Debt-to-Equity
- Average Net Profit Margin
- Asset Turnover
- Sector Distribution
- KPI Cards

---

## 🏢 Company Profile

Displays:

- Company Information
- Book Value
- ROE
- ROCE
- Company Overview
- Financial Highlights

---

## 🔍 Stock Screener

Supports filtering by:

- Company
- ROE
- Debt to Equity
- PE Ratio
- PB Ratio
- Sector
- Market Capitalization

---

## 🤝 Peer Comparison

Compare companies using:

- ROE
- Profit Margin
- Debt to Equity
- Interest Coverage
- Asset Turnover
- Free Cash Flow

---

## 📈 Financial Trends

Visualizations for:

- Revenue Trend
- Net Profit Trend
- ROE Trend
- Operating Margin Trend

---

## 🏭 Sector Analysis

Provides:

- Sector Distribution
- Sector KPIs
- Company Rankings
- Sector Comparison

---

## 💰 Valuation Dashboard

Calculates:

- Free Cash Flow Yield
- Dividend Yield
- Sector Median PE
- Sector Median PB
- Valuation Classification

---

## 📑 Reports Dashboard

Generate:

- CSV Reports
- Excel Reports
- PDF Reports

---

# 🧠 Sprint 5 Features

## NLP Analysis Parser

- Parses CAGR information from company analysis
- Extracts structured financial metrics
- Generates:
  - analysis_parsed.csv
  - parse_failures.csv

---

## NLP Pros & Cons Generator

Automatically generates company strengths and weaknesses using rule-based analysis.

Features:

- 12 Pro Rules
- 12 Con Rules
- Confidence Score (0–100)
- Minimum confidence threshold
- One pro and one con for every company

Outputs:

- pros_cons_generated.csv

---

## Cash Flow Intelligence

Computes:

- CFO Quality Score
- Free Cash Flow
- CapEx Intensity
- FCF Conversion Rate
- Distress Detection
- Deleveraging Detection
- Capital Allocation Pattern

Outputs:

- cashflow_intelligence.xlsx
- distress_alerts.csv

---

## Capital Allocation Analysis

Identifies cash flow patterns including:

- Reinvestor
- Growth Funded by Debt
- Cash Rich
- Cash Accumulator
- Debt Reduction
- Distress
- Mixed
- Pre-Revenue

Outputs:

- capital_allocation.csv
- pattern_changes.csv

---

## Company Tearsheet Reports

Automatically generates professional two-page PDF reports containing:

### Page 1

- Company Header
- KPI Cards
- Revenue Trend
- Net Profit Trend
- ROE Trend

### Page 2

- Balance Sheet Composition
- Cash Flow Summary
- Pros
- Cons
- Capital Allocation Badge

Generated for all available companies.

---

## Sector Reports

Automatically generates sector-wise PDF reports containing:

- Sector Summary
- Median KPIs
- Company Comparison Table

Generated for all sectors.

---

## Portfolio Summary Report

Generates a consolidated PDF containing:

- Company Overview
- Top KPIs
- Financial Trends
- Performance Summary

---

# 📂 Project Structure

```text
n100_financial_platform/
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
│   ├── tearsheets/
│   ├── sector/
│   ├── portfolio/
│   ├── tearsheet.py
│   └── sector_report.py
│
├── src/
│   ├── analytics/
│   ├── dashboard/
│   ├── etl/
│   ├── nlp/
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

# 🗄 Database Tables

- Companies
- Financial Ratios
- Profit & Loss
- Balance Sheet
- Cash Flow
- Analysis
- Documents
- Market Cap
- Peer Groups
- Sectors
- Stock Prices

---

# 📁 Generated Outputs

## CSV

- profitability_ratios.csv
- liquidity_ratios.csv
- growth_ratios.csv
- solvency_ratios.csv
- efficiency_ratios.csv
- valuation_flags.csv
- analysis_parsed.csv
- parse_failures.csv
- pros_cons_generated.csv
- distress_alerts.csv
- capital_allocation.csv
- pattern_changes.csv
- skipped_tearsheets.csv

---

## Excel

- screener_output.xlsx
- peer_comparison.xlsx
- valuation_summary.xlsx
- cashflow_intelligence.xlsx

---

## PDF Reports

### Company Reports

```
reports/tearsheets/
```

Individual company financial tearsheets.

### Sector Reports

```
reports/sector/
```

Sector-wise financial summaries.

### Portfolio Report

```
reports/portfolio/
```

Portfolio summary PDF.

---

# 🛠 Technologies Used

- Python 3.11
- SQLite
- Pandas
- NumPy
- Streamlit
- Plotly
- Matplotlib
- ReportLab
- OpenPyXL
- PyYAML
- Pytest
- Git
- GitHub

---

# 📈 Analytics Performed

- Profitability Analysis
- Liquidity Analysis
- Solvency Analysis
- Efficiency Analysis
- Growth Analysis
- Valuation Analysis
- Peer Comparison
- Financial Trend Analysis
- Cash Flow Intelligence
- Distress Detection
- Capital Allocation Analysis
- NLP Rule-Based Analysis
- Sector Analytics

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Pullareddy9371/n100_financial_platform.git
```

Move into the project:

```bash
cd n100_financial_platform
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Run analytics:

```bash
python -m src.analytics.valuation
```

Run Streamlit dashboard:

```bash
streamlit run src/dashboard/app.py
```

Run tests:

```bash
pytest
```

---

# 🎯 Learning Outcomes

This project demonstrates practical experience in:

- Python Programming
- Financial Data Analytics
- ETL Pipelines
- SQLite Database Design
- Data Cleaning
- Pandas Data Processing
- Financial Ratio Analysis
- Rule-Based NLP
- Cash Flow Intelligence
- Automated PDF Report Generation
- Data Visualization
- Streamlit Dashboard Development
- Testing and Debugging
- Git & GitHub Version Control

---

# 🔮 Future Enhancements

- Live NSE/BSE Data Integration
- AI-based Investment Recommendation Engine
- Machine Learning Stock Prediction
- Portfolio Optimization
- User Authentication
- Cloud Deployment (AWS/Azure)
- REST API Support

---

# 👨‍💻 Author

**Pulla Reddy Onteddu**

B.Tech – Artificial Intelligence & Machine Learning

GitHub:

**https://github.com/Pullareddy9371/n100_financial_platform**

---

# 📄 License

This project was developed for educational, internship, and portfolio purposes.