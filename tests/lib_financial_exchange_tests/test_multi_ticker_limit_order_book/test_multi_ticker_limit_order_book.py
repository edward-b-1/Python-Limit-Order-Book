
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.limit_order_book.data_structures.multi_ticker_limit_order_book import MultiTickerLimitOrderBook

from datetime import datetime


# TODO: test the timestamps
def test_multi_limit_order_book_update_order_wrong_order_id():

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')
    order_side = OrderSide("BUY")
    timestamp = datetime(year=2024, month=7, day=19)

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    # Wrong order id, so should do nothing
    order = lob.update(
        order_id=OrderId(2),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    assert order is None

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order == order_1


# TODO: test the timestamps
def test_multi_limit_order_book_update_order_no_change():

    lob = MultiTickerLimitOrderBook()
    order_side = OrderSide("BUY")
    timestamp = datetime(year=2024, month=7, day=19)

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=Ticker('PYTH'),
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    # No changes, so should do nothing
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    assert order is None

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order == order_1


# TODO: test the timestamps
def test_multi_limit_order_book_update_order():

    lob = MultiTickerLimitOrderBook()
    order_side = OrderSide("BUY")
    timestamp = datetime(year=2024, month=7, day=19)

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=Ticker('PYTH'),
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    # Changed price and volume
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(110),
        volume=Volume(12),
    )
    assert order == order_1
    assert order.to_int_price().to_int() == 110
    assert order.to_volume().to_int() == 12

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order is None


# TODO: test the timestamps
def test_multi_limit_order_book_update_order_int_price():

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=19)

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    # Wrong order side so should do nothing
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(110),
        volume=Volume(10),
    )
    assert order == order_1
    assert order.to_int_price().to_int() == 110

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order is None


# TODO: test the timestamps
def test_multi_limit_order_book_update_order_volume_increase():

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=19)

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    # Wrong order side so should do nothing
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(100),
        volume=Volume(11),
    )
    assert order == order_1
    assert order.to_volume().to_int() == 11

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order is None


# TODO: test the timestamps
def test_multi_limit_order_book_update_order_volume_decrease():

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=19)

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    # Wrong order side so should do nothing
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(100),
        volume=Volume(9),
    )
    assert order is None

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order == order_1
    assert order.to_volume().to_int() == 9

