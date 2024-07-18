
from limit_order_book.types import OrderId
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.types import OrderSide
from limit_order_book.types import Ticker
from limit_order_book.types import OrderWithoutOrderId
from limit_order_book.types import Order
from limit_order_book.types import Trade
from limit_order_book.types import TopOfBook
from limit_order_book.limit_order_book import LimitOrderBook


def test_limit_order_book_order_cancel_partial():

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')

    order = OrderWithoutOrderId(
        ticker=ticker,
        order_side=OrderSide('BUY'),
        int_price=IntPrice(0),
        volume=Volume(100),
    )
    (order_id, _) = lob.order_insert(order)
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
