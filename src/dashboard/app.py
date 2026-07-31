import streamlit as st

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* Main Background */
.stApp{
    background-color:#f5f7fb;
}

/* KPI Cards */
[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,.15);
}

/* Tables */
[data-testid="stDataFrame"]{
    border-radius:15px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#182848;
}

/* Sidebar Text */
section[data-testid="stSidebar"] *{
    color:white;
}

/* Buttons */
.stButton>button{
    border-radius:10px;
    background:#1f77b4;
    color:white;
    border:none;
}

/* Download Button */
.stDownloadButton>button{
    border-radius:10px;
    background:#28a745;
    color:white;
    border:none;
}

</style>
""", unsafe_allow_html=True)

st.logo("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png")

st.sidebar.title("📊 N100 Financial Intelligence Dashboard")

st.markdown("""
Analyze Nifty 100 companies using financial ratios, peer comparison,
stock screening, sector analytics, valuation metrics, and interactive dashboards.
""")

st.sidebar.markdown("---")

st.sidebar.success("Bluestock Fintech Internship")

st.sidebar.info(
    """
Developer

**Pulla Reddy Onteddu**

"""
)

pg = st.navigation([
    st.Page("pages/01_home.py", title="Home", icon="🏠"),
    st.Page("pages/02_profile.py", title="Company Profile", icon="🏢"),
    st.Page("pages/03_screener.py", title="Stock Screener", icon="📈"),
    st.Page("pages/04_peers.py", title="Peer Comparison", icon="👥"),
    st.Page("pages/05_trends.py", title="Financial Trends", icon="📊"),
    st.Page("pages/06_sectors.py", title="Sector Analysis", icon="🏭"),
    st.Page("pages/07_capital.py", title="Capital Allocation", icon="💰"),
    st.Page("pages/08_reports.py", title="Reports", icon="📄"),
    st.Page("pages/09_about.py", title="About", icon="ℹ️"),
    st.Page(
    "pages/10_valuation.py",
    title="Valuation",
    icon="💰"
),
])

pg.run()
st.divider()

st.caption(
    "N100 Financial Intelligence Platform | Developed using Python, Streamlit, SQLite and Plotly"
)