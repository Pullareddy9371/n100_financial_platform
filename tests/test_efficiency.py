from src.analytics.ratios import RatioEngine


def test_asset_turnover():
    assert RatioEngine.asset_turnover(1000, 500) == 2.0


def test_fixed_asset_turnover():
    assert RatioEngine.fixed_asset_turnover(1000, 250) == 4.0


def test_investment_turnover():
    assert RatioEngine.investment_turnover(1000, 200) == 5.0


def test_asset_turnover_zero():
    assert RatioEngine.asset_turnover(100, 0) is None


def test_fixed_asset_turnover_zero():
    assert RatioEngine.fixed_asset_turnover(100, 0) is None


def test_investment_turnover_zero():
    assert RatioEngine.investment_turnover(100, 0) is None