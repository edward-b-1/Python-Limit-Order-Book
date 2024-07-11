
from limit_order_book.types import OrderId
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.types import OrderSide
from limit_order_book.types import Ticker
from limit_order_book.order import Order
from limit_order_book.trade import Trade
from limit_order_book.top_of_book import TopOfBook
from limit_order_book.multi_ticker_limit_order_book import MultiTickerLimitOrderBook


def test_multi_limit_order_book_order_insert():

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

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')

    ####

    order_no_match = Order(
        order_id=OrderId(1000),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(500),
        volume=Volume(1000),
    )
    trades = lob.trade(order_no_match)
    lob.insert(order_no_match)

    ####

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    trades = lob.trade(order_1)
    lob.insert(order_1)

    ####

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1020),
        volume=Volume(20),
    )
    trades = lob.trade(order_2)
    lob.insert(order_2)

    ####

    order_3 = Order(
        order_id=OrderId(3),
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(990),
        volume=Volume(100),
    )
    trades = lob.trade(order_3)
    lob.insert(order_3)

    assert trades == [
        Trade(order_id_maker=OrderId(2), order_id_taker=OrderId(3), ticker=ticker, int_price=IntPrice(990), volume=Volume(20)),
        Trade(order_id_maker=OrderId(1), order_id_taker=OrderId(3), ticker=ticker, int_price=IntPrice(990), volume=Volume(10)),
    ]
    assert order_3 == Order(order_id=OrderId(3), ticker=ticker, order_side=OrderSide("SELL"), int_price=IntPrice(990), volume=Volume(70))
