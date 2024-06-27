
from new_limit_order_book.types.order_id import OrderId
from new_limit_order_book.ticker import Ticker
from new_limit_order_book.order_side import OrderSide
from new_limit_order_book.order import Order
from new_limit_order_book.types.int_price import IntPrice
from new_limit_order_book.types.volume import Volume

from new_limit_order_book.single_side_limit_order_book import SingleSideLimitOrderBook


def test_single_side_limit_order_book_find_order_by_order_id_no_orders():

    single_side_lob = SingleSideLimitOrderBook(
        ticker=Ticker('PYTH'),
        order_side=OrderSide.BUY,
    )
    maybe_order = single_side_lob.find_order_by_order_id(OrderId(1))
    assert maybe_order is None


def test_single_side_limit_order_book_find_order_by_order_id_1_order():

    ticker = Ticker('PYTH')
    order_side = OrderSide.BUY

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    single_side_lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )

    single_side_lob.insert(order_1)

    maybe_order = single_side_lob.find_order_by_order_id(OrderId(1))
    assert maybe_order is not None
    assert maybe_order == order_1
