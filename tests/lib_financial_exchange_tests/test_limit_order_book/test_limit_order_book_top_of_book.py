
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types import TopOfBook

from lib_financial_exchange.limit_order_book.limit_order_book import LimitOrderBook

from datetime import datetime


def test_limit_order_book_top_of_book_buy_sequence():

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=11)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=None,
        volume_buy=None,
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_1 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    (order_id, _) = lob.order_insert(
        order_1.to_ticker(),
        order_1.to_order_side(),
        order_1.to_int_price(),
        order_1.to_volume(),
        order_1.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1000),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_2 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(999),
        volume=Volume(10),
    )
    (order_id, _) = lob.order_insert(
        order_2.to_ticker(),
        order_2.to_order_side(),
        order_2.to_int_price(),
        order_2.to_volume(),
        order_2.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1000),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_3 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1001),
        volume=Volume(10),
    )
    (order_id, _) = lob.order_insert(
        order_3.to_ticker(),
        order_3.to_order_side(),
        order_3.to_int_price(),
        order_3.to_volume(),
        order_3.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1001),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_4 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(2000),
        volume=Volume(10),
    )
    (order_id, _) = lob.order_insert(
        order_4.to_ticker(),
        order_4.to_order_side(),
        order_4.to_int_price(),
        order_4.to_volume(),
        order_4.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(2000),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
        )

    ####

    order_5 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(500),
        volume=Volume(10),
    )
    (order_id, _) = lob.order_insert(
        order_5.to_ticker(),
        order_5.to_order_side(),
        order_5.to_int_price(),
        order_5.to_volume(),
        order_5.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(2000),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
    )


def test_limit_order_book_top_of_book_buy_and_sell():

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=11)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=None,
        volume_buy=None,
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_1 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    lob.order_insert(
        order_1.to_ticker(),
        order_1.to_order_side(),
        order_1.to_int_price(),
        order_1.to_volume(),
        order_1.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1000),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_2 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(1010),
        volume=Volume(5),
    )
    lob.order_insert(
        order_2.to_ticker(),
        order_2.to_order_side(),
        order_2.to_int_price(),
        order_2.to_volume(),
        order_2.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1000),
        volume_buy=Volume(10),
        int_price_sell=IntPrice(1010),
        volume_sell=Volume(5),
    )


def test_limit_order_book_top_of_book_after_trade():

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=11)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=None,
        volume_buy=None,
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_1 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    (order_id, _) = lob.order_insert(
        order_1.to_ticker(),
        order_1.to_order_side(),
        order_1.to_int_price(),
        order_1.to_volume(),
        order_1.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1000),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_2 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1010),
        volume=Volume(10),
    )
    (order_id, _) = lob.order_insert(
        order_2.to_ticker(),
        order_2.to_order_side(),
        order_2.to_int_price(),
        order_2.to_volume(),
        order_2.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1010),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_3 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(1005),
        volume=Volume(15),
    )
    (order_id, trades) = lob.order_insert(
        order_3.to_ticker(),
        order_3.to_order_side(),
        order_3.to_int_price(),
        order_3.to_volume(),
        order_3.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1000),
        volume_buy=Volume(10),
        int_price_sell=IntPrice(1005),
        volume_sell=Volume(5),
    )


def test_limit_order_book_top_of_book_update_order():

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=11)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=None,
        volume_buy=None,
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    order_1 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    (order_id, _) = lob.order_insert(
        order_1.to_ticker(),
        order_1.to_order_side(),
        order_1.to_int_price(),
        order_1.to_volume(),
        order_1.to_timestamp(),
    )

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(1000),
        volume_buy=Volume(10),
        int_price_sell=None,
        volume_sell=None,
    )

    ####

    lob.order_update(order_id=order_id, int_price=IntPrice(950), volume=Volume(5), timestamp=timestamp)

    top_of_book = lob.top_of_book(ticker)
    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=IntPrice(950),
        volume_buy=Volume(5),
        int_price_sell=None,
        volume_sell=None,
    )
