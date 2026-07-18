from src.analytics.ratios import RatioEngine


def test_current_ratio():
    assert RatioEngine.current_ratio(200, 100) == 2.0


def test_quick_ratio():
    assert RatioEngine.quick_ratio(200, 50, 100) == 1.5


def test_cash_ratio():
    assert RatioEngine.cash_ratio(50, 100) == 0.5


def test_current_ratio_zero():
    assert RatioEngine.current_ratio(100, 0) is None


def test_quick_ratio_zero():
    assert RatioEngine.quick_ratio(100, 20, 0) is None


def test_cash_ratio_zero():
    assert RatioEngine.cash_ratio(20, 0) is None