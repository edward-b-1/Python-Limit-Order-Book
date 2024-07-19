
import pytest

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.data_structures.single_side_limit_order_book import SingleSideLimitOrderBook

from datetime import datetime


def test_single_side_limit_order_book_order_id_exists():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    timestamp = datetime(year=2024, month=7, day=19)

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    lob.insert(order_1)

    assert lob.order_id_exists(OrderId(1))
    assert lob.order_id_exists(OrderId(2)) == False

