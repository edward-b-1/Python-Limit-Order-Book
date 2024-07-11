
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


def test_limit_order_book_trade_insert_new():

    # Book Setup:
    #
    # Bids:
    # - price=1020, volume=20 (a)
    # - price=1000, volume=10 (b)
    # - price=500, volume=1000
    #
    # Offer:
    # - price=990, volume=100
    #
    # This should produce matches @ price=990
    # a matches first, followed by b

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')

    ####

    order_no_match = OrderWithoutOrderId(
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(500),
        volume=Volume(1000),
    )
    (order_id_1, trades) = lob.order_insert(order_no_match)
    assert trades == []

    ####

    order_1 = OrderWithoutOrderId(
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    (order_id_2, trades) = lob.order_insert(order_1)
    assert trades == []

    ####

    order_2 = OrderWithoutOrderId(
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1020),
        volume=Volume(20),
    )
    (order_id_3, trades) = lob.order_insert(order_2)
    assert trades == []

    ####

    order_3 = OrderWithoutOrderId(
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(990),
        volume=Volume(100),
    )
    (order_id_4, trades) = lob.order_insert(order_3)

    assert trades == [
        Trade(order_id_maker=order_id_3, order_id_taker=order_id_4, ticker=ticker, int_price=IntPrice(990), volume=Volume(20)),
        Trade(order_id_maker=order_id_2, order_id_taker=order_id_4, ticker=ticker, int_price=IntPrice(990), volume=Volume(10)),
    ]
    order_3_internal = lob.order_cancel(order_id=order_id_4)
    assert order_3_internal == Order(order_id=order_id_4, ticker=ticker, order_side=OrderSide("SELL"), int_price=IntPrice(990), volume=Volume(70))
