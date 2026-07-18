from src.analytics.ratios import RatioEngine


def test_sales_growth():
    assert RatioEngine.sales_growth(120, 100) == 20.0


def test_profit_growth():
    assert RatioEngine.profit_growth(150, 100) == 50.0


def test_asset_growth():
    assert RatioEngine.asset_growth(220, 200) == 10.0


def test_sales_growth_zero():
    assert RatioEngine.sales_growth(100, 0) is None


def test_profit_growth_zero():
    assert RatioEngine.profit_growth(100, 0) is None


def test_asset_growth_zero():
    assert RatioEngine.asset_growth(100, 0) is None