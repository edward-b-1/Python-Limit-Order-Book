
import pytest

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order

from lib_financial_exchange.trade_id_generator import TradeIdGenerator

from lib_financial_exchange.data_structures.single_side_limit_order_book import SingleSideLimitOrderBook

from datetime import datetime


def test_single_side_limit_order_book_no_trade_no_previous_order():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    order_side_other_side = order_side.other_side()
    timestamp = datetime(year=2024, month=7, day=19)
    timestamp_trade = timestamp

    trade_id_generator = TradeIdGenerator()

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side_other_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    trades = lob.trade(order_1, trade_id_generator=trade_id_generator, timestamp=timestamp_trade)
    assert trades == []

    assert lob.order_id_exists(OrderId(1)) == False


def test_single_side_limit_order_book_no_trade_no_matching_price_level():

    ticker = Ticker('AAPL')
    timestamp = datetime(year=2024, month=7, day=19)
    timestamp_trade = timestamp

    trade_id_generator = TradeIdGenerator()

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=OrderSide("BUY"),
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(120),
        volume=Volume(10),
    )

    with pytest.raises(Exception):
        trades = lob.trade(order_1, trade_id_generator=trade_id_generator, timestamp=timestamp_trade)
    lob.insert(order_1)
    trades = lob.trade(order_2, trade_id_generator=trade_id_generator, timestamp=timestamp_trade)
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
    timestamp = datetime(year=2024, month=7, day=19)
    timestamp_trade = timestamp

    trade_id_generator = TradeIdGenerator()

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=OrderSide("BUY"),
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    with pytest.raises(Exception):
        trades = lob.trade(order_1, trade_id_generator=trade_id_generator, timestamp=timestamp_trade)
        # TODO: check full exception
    lob.insert(order_1)
    with pytest.raises(Exception):
        trades = lob.trade(order_2, trade_id_generator=trade_id_generator, timestamp=timestamp_trade)
        # TODO: check full exception
    lob.insert(order_2)

    assert lob.order_id_exists(OrderId(1))
    assert lob.order_id_exists(OrderId(2))
    assert lob.order_id_exists(OrderId(3)) == False

    assert lob.cancel(OrderId(1)) == order_1
    assert lob.cancel(OrderId(2)) == order_2
