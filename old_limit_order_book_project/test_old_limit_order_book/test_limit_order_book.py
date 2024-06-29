
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.limit_order_book import LimitOrderBook
from old_limit_order_book.order import Order


def test_limit_order_book():
    ticker_pyth = 'PYTH'
    ticker_cpp = 'CPP'
    order_side = OrderSide.BUY
    int_price_1 = 1000

    limit_order_book = LimitOrderBook(order_side=order_side)

    order_1 = Order(1, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=10)
    order_2 = Order(2, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=20)
    order_3 = Order(3, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=30)

    order_4 = Order(4, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=40)
    order_5 = Order(5, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=50)
    order_6 = Order(6, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=60)

    limit_order_book.order_insert(order_1)
    limit_order_book.order_insert(order_2)
    limit_order_book.order_insert(order_3)

    limit_order_book.order_insert(order_4)
    limit_order_book.order_insert(order_5)
    limit_order_book.order_insert(order_6)

    depth = limit_order_book.depth_aggregated()
    assert depth == 6, f'depth is not 6, depth = {depth}'

    # inserting a duplicate fails
    try:
        limit_order_book.order_insert(order_3)
    except RuntimeError as e:
        assert str(e) == f'cannot insert order with existing order_id {3}'

    limit_order_book.order_cancel(order_id=2)

    # cancelling a non-existing/already cancelled order fails
    order_id = 2
    try:
        limit_order_book.order_cancel(order_id)
    except RuntimeError as e:
        assert str(e) == f'cannot cancel order with missing order_id {order_id}'

    limit_order_book.order_cancel(order_id=1)

    # TODO: can you update an order to change the price?
    limit_order_book.order_update(order_id=3, int_price=int_price_1, volume=50)
    assert limit_order_book._get_order_by_order_id(order_id=3).int_price == int_price_1, f'unexpected order int_price'
    assert limit_order_book._get_order_by_order_id(order_id=3).volume == 50, f'unexpected order volume'

    limit_order_book.order_cancel(order_id=3)

    limit_order_book.order_cancel(order_id=4)
    limit_order_book.order_cancel(order_id=5)
    limit_order_book.order_cancel(order_id=6)

    depth = limit_order_book.depth_aggregated()
    assert depth == 0, f'depth is not 0, depth = {depth}'


def test_order_cancel():
    limit_order_book = LimitOrderBook(order_side=OrderSide.BUY)

    order = Order(
        order_id=1,
        ticker='PYTH',
        order_side=OrderSide.BUY,
        int_price=1000,
        volume=20,
    )

    limit_order_book.order_insert(order)
    removed_order = limit_order_book.order_cancel(1)

    assert removed_order == order, f'removed order data does not match expected order data'

