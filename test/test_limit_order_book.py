
from limit_order_book.limit_order_book import LimitOrderBook
from limit_order_book.partial_order import PartialOrder

from limit_order_book.util_parse import parse_price_string_and_convert_to_int_price


def test_limit_order_book():
    ticker_pyth = 'PYTH'
    ticker_cpp = 'CPP'
    order_side = 'BUY'
    int_price_1 = 1000

    limit_order_book = LimitOrderBook()

    limit_order_book.order_insert(1, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=10)
    limit_order_book.order_insert(2, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=20)
    limit_order_book.order_insert(3, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=30)

    limit_order_book.order_insert(4, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=40)
    limit_order_book.order_insert(5, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=50)
    limit_order_book.order_insert(6, ticker=ticker_cpp, order_side=order_side, int_price=int_price_1, volume=60)

    depth = limit_order_book.depth_aggregated()
    assert depth == 6, f'depth is not 6, depth = {depth}'

    # inserting a duplicate fails
    try:
        limit_order_book.order_insert(3, ticker=ticker_pyth, order_side=order_side, int_price=int_price_1, volume=30)
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
    limit_order_book = LimitOrderBook()
    limit_order_book.order_insert(1, 'PYTH', 'BUY', 1000, 20)
    removed_order = limit_order_book.order_cancel(1)
    expected_order = PartialOrder(
        order_id=1,
        ticker='PYTH',
        order_side='BUY',
        int_price=1000,
        volume=20,
    )
    assert removed_order == expected_order, f'removed order data does not match expected order data'

