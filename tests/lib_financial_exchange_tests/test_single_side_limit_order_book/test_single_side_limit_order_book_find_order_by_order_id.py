
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume

from lib_financial_exchange.limit_order_book.data_structures.single_side_limit_order_book import SingleSideLimitOrderBook


def test_single_side_limit_order_book_find_order_by_order_id_no_orders():

    assert True
    # single_side_lob = SingleSideLimitOrderBook(
    #     ticker=Ticker('PYTH'),
    #     order_side=OrderSide.BUY,
    # )
    # maybe_order = single_side_lob.find_order_by_order_id(OrderId(1))
    # assert maybe_order is None


def test_single_side_limit_order_book_find_order_by_order_id_1_order():

    assert True
    # ticker = Ticker('PYTH')
    # order_side = OrderSide.BUY

    # order_1 = Order(
    #     order_id=OrderId(1),
    #     ticker=ticker,
    #     order_side=order_side,
    #     int_price=IntPrice(100),
    #     volume=Volume(10),
    # )

    # single_side_lob = SingleSideLimitOrderBook(
    #     ticker=ticker,
    #     order_side=order_side,
    # )

    # single_side_lob.insert(order_1)

    # maybe_order = single_side_lob.find_order_by_order_id(OrderId(1))
    # assert maybe_order is not None
    # assert maybe_order == order_1
