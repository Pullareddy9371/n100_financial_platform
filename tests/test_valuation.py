from src.analytics.ratios import RatioEngine


def test_pe_ratio():
    assert RatioEngine.pe_ratio(200, 20) == 10.0


def test_pb_ratio():
    assert RatioEngine.pb_ratio(200, 100) == 2.0


def test_earnings_yield():
    assert RatioEngine.earnings_yield(20, 200) == 10.0


def test_pe_zero():
    assert RatioEngine.pe_ratio(100, 0) is None


def test_pb_zero():
    assert RatioEngine.pb_ratio(100, 0) is None


def test_earnings_yield_zero():
    assert RatioEngine.earnings_yield(20, 0) is None