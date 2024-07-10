
import pytest

from limit_order_book.types.order_id import OrderId
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.order_side import OrderSide
from limit_order_book.ticker import Ticker
from limit_order_book.order import Order
from limit_order_book.single_side_limit_order_book import SingleSideLimitOrderBook


def test_single_side_limit_order_book_no_trade_no_previous_order():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    order_side_other_side = order_side.other_side()

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side_other_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    trades = lob.trade(order_1)
    assert trades == []

    assert lob.order_id_exists(OrderId(1)) == False


def test_single_side_limit_order_book_no_trade_no_matching_price_level():

    ticker = Ticker('AAPL')

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=OrderSide("BUY"),
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(120),
        volume=Volume(10),
    )

    with pytest.raises(Exception):
        trades = lob.trade(order_1)
    lob.insert(order_1)
    trades = lob.trade(order_2)
    assert trades == []
    with pytest.raises(Exception):
        lob.insert(order_2)

    assert lob.order_id_exists(OrderId(1))
    assert lob.order_id_exists(OrderId(2)) == False
    assert lob.order_id_exists(OrderId(3)) == False

    assert lob.cancel(OrderId(1)) == order_1
    assert lob.cancel(OrderId(2)) == None


def test_single_side_limit_order_book_no_trade_no_matching_order_side():

    ticker = Ticker('AAPL')

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=OrderSide("BUY"),
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    with pytest.raises(Exception):
        trades = lob.trade(order_1)
    lob.insert(order_1)
    with pytest.raises(Exception):
        trades = lob.trade(order_2)
    lob.insert(order_2)

    assert lob.order_id_exists(OrderId(1))
    assert lob.order_id_exists(OrderId(2))
    assert lob.order_id_exists(OrderId(3)) == False

    assert lob.cancel(OrderId(1)) == order_1
    assert lob.cancel(OrderId(2)) == order_2
