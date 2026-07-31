import streamlit as st
import os

st.title("📄 Reports & Downloads")

files = [
    "src/output/financial_metrics.csv",
    "src/output/analytics_summary.csv",
    "src/output/liquidity_ratios.csv",
    "src/output/profitability_ratios.csv",
    "src/output/valuation_ratios.csv",
    "src/output/growth_ratios.csv",
    "src/output/efficiency_ratios.csv",
    "src/output/solvency_ratios.csv",
    "src/output/capital_allocation.csv",
    "src/output/peer_comparison.xlsx",
    "src/output/screener_output.xlsx"
]

st.write("Download generated reports from the project.")

for file in files:

    if os.path.exists(file):

        with open(file, "rb") as f:

            st.download_button(
                label=f"📥 {os.path.basename(file)}",
                data=f,
                file_name=os.path.basename(file)
            )
            # ---------------------------------
# Footer
# ---------------------------------

st.divider()

st.caption(
    "© 2026 N100 Financial Intelligence Platform | Bluestock Fintech Internship | Developed by Pulla Reddy Onteddu"
)