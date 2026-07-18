import os

def test_summary_exists():
    assert os.path.exists("src/output/analytics_summary.csv")