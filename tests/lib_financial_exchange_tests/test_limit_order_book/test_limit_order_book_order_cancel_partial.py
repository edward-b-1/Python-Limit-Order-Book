
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types import TopOfBook
from lib_financial_exchange.limit_order_book import LimitOrderBook

from datetime import datetime


def test_limit_order_book_order_cancel_partial():

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=11)

    (order_id, _) = lob.order_insert(
        ticker=ticker,
        order_side=OrderSide('BUY'),
        int_price=IntPrice(0),
        volume=Volume(100),
        timestamp=timestamp,
    )

    top_of_book = lob.top_of_book(ticker=ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(0),
        volume_buy=Volume(100),
        int_price_sell=None,
        volume_sell=None
    )

    lob.order_cancel_partial(order_id=order_id, volume=Volume(10))
    top_of_book = lob.top_of_book(ticker=ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(0),
        volume_buy=Volume(90),
        int_price_sell=None,
        volume_sell=None
    )

    lob.order_cancel_partial(order_id=order_id, volume=Volume(50))
    top_of_book = lob.top_of_book(ticker=ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(0),
        volume_buy=Volume(40),
        int_price_sell=None,
        volume_sell=None
    )

    lob.order_cancel_partial(order_id=order_id, volume=Volume(39))
    top_of_book = lob.top_of_book(ticker=ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(0),
        volume_buy=Volume(1),
        int_price_sell=None,
        volume_sell=None
    )

    lob.order_cancel_partial(order_id=order_id, volume=Volume(1))
    top_of_book = lob.top_of_book(ticker=ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=None,
        volume_buy=None,
        int_price_sell=None,
        volume_sell=None
    )
