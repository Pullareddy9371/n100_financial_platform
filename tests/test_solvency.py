from src.analytics.ratios import RatioEngine


def test_debt_to_equity():
    assert RatioEngine.debt_to_equity(100, 200) == 0.5


def test_interest_coverage():
    assert RatioEngine.interest_coverage(200, 20) == 10.0


def test_debt_ratio():
    assert RatioEngine.debt_ratio(300, 600) == 0.5


def test_debt_to_equity_zero():
    assert RatioEngine.debt_to_equity(100, 0) is None


def test_interest_zero():
    assert RatioEngine.interest_coverage(100, 0) is None


def test_debt_ratio_zero():
    assert RatioEngine.debt_ratio(100, 0) is None