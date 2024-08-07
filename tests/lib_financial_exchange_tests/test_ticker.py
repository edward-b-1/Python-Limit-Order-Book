
from lib_financial_exchange.financial_exchange_types import Ticker


def test_ticker_str_not_equal():

    ticker_aapl = Ticker('AAPL')
    ticker_nvda = Ticker('NVDA')
    assert ticker_aapl != ticker_nvda


def test_ticker_str_equal():

    ticker_aapl = Ticker('AAPL')
    ticker_aapl_2 = Ticker('AAPL')
    assert ticker_aapl == ticker_aapl_2


# def test_ticker_str_int_not_equal():

#     ticker_1 = Ticker(1234)
#     ticker_2 = Ticker('1234')
#     assert ticker_1 != ticker_2


# def test_ticker_int_equal():

#     ticker_1 = Ticker(1)
#     ticker_2 = Ticker(1)
#     assert ticker_1 == ticker_2


# def test_ticker_int_not_equal():

#     ticker_1 = Ticker(1)
#     ticker_2 = Ticker(2)
#     assert ticker_1 != ticker_2