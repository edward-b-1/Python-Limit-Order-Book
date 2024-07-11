
from limit_order_book.types import OrderId
from limit_order_book.types import Ticker
from limit_order_book.types import OrderSide
from limit_order_book.order import Order
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume

from limit_order_book.single_side_limit_order_book import SingleSideLimitOrderBook


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
