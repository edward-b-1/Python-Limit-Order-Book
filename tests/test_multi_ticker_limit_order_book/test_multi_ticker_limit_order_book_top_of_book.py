
from limit_order_book.types import OrderId
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.types import OrderSide
from limit_order_book.types import Ticker
from limit_order_book.types import Order
from limit_order_book.types import TopOfBook
from limit_order_book.data_structures.multi_ticker_limit_order_book import MultiTickerLimitOrderBook


def test_multi_ticker_limit_order_book_top_of_book_buy_sequence():

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(ticker=ticker, int_price_buy=None, volume_buy=None, int_price_sell=None, volume_sell=None)

    ####

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    lob.insert(order_1)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(ticker=ticker, int_price_buy=IntPrice(1000), volume_buy=Volume(10), int_price_sell=None, volume_sell=None)

    ####

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(999),
        volume=Volume(10),
    )
    lob.insert(order_2)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(ticker=ticker, int_price_buy=IntPrice(1000), volume_buy=Volume(10), int_price_sell=None, volume_sell=None)

    ####

    order_3 = Order(
        order_id=OrderId(3),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1001),
        volume=Volume(10),
    )
    lob.insert(order_3)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(ticker=ticker, int_price_buy=IntPrice(1001), volume_buy=Volume(10), int_price_sell=None, volume_sell=None)

    ####

    order_4 = Order(
        order_id=OrderId(4),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(2000),
        volume=Volume(10),
    )
    lob.insert(order_4)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(ticker=ticker, int_price_buy=IntPrice(2000), volume_buy=Volume(10), int_price_sell=None, volume_sell=None)

    ####

    order_5 = Order(
        order_id=OrderId(5),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(500),
        volume=Volume(10),
    )
    lob.insert(order_5)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(ticker=ticker, int_price_buy=IntPrice(2000), volume_buy=Volume(10), int_price_sell=None, volume_sell=None)


def test_multi_limit_order_book_top_of_book_buy_and_sell():

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(ticker=ticker, int_price_buy=None, volume_buy=None, int_price_sell=None, volume_sell=None)

    ####

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    lob.insert(order_1)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(ticker=ticker, int_price_buy=IntPrice(1000), volume_buy=Volume(10), int_price_sell=None, volume_sell=None)

    ####

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(1010),
        volume=Volume(5),
    )
    lob.insert(order_2)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1000),
        volume_buy=Volume(10),
        int_price_sell=IntPrice(1010),
        volume_sell=Volume(5),
    )
