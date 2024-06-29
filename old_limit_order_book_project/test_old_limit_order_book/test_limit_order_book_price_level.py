
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.limit_order_book import Order
from old_limit_order_book.limit_order_book import LimitOrderBookPriceLevel


def test_limit_order_book_price_level():
    ticker = 'PYTH'
    order_side = OrderSide.BUY
    int_price_1 = 1000
    int_price_2 = 1010

    order_1 = Order(
        order_id=1,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price_1,
        volume=10,
    )

    order_2 = Order(
        order_id=2,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price_1,
        volume=20,
    )

    order_3 = Order(
        order_id=3,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price_1,
        volume=30,
    )

    order_4 = Order(
        order_id=4,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price_2,
        volume=40,
    )

    order_5 = Order(
        order_id=5,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price_2,
        volume=50,
    )

    limit_order_book_price_level = LimitOrderBookPriceLevel(order_side=order_side)

    limit_order_book_price_level.order_insert(order_1)
    limit_order_book_price_level.order_insert(order_2)
    limit_order_book_price_level.order_insert(order_3)
    limit_order_book_price_level.order_insert(order_4)
    limit_order_book_price_level.order_insert(order_5)

    depth = limit_order_book_price_level.depth_aggregated()
    assert depth == 5, f'depth is not 5, depth = {depth}'

    # inserting a duplicate fails
    try:
        limit_order_book_price_level.order_insert(order_2)
    except RuntimeError as e:
        assert str(e) == f'cannot insert order with existing order_id {order_2.order_id}'

    limit_order_book_price_level.order_cancel(order_id=2)

    # cancelling a non-existing/already cancelled order fails
    order_id = 2
    try:
        limit_order_book_price_level.order_cancel(order_id)
    except RuntimeError as e:
        assert str(e) == f'cannot cancel order with missing order_id {order_id}'

    limit_order_book_price_level.order_cancel(order_id=1)

    # TODO: can you update an order to change the price?
    limit_order_book_price_level.order_update(order_id=3, int_price=int_price_1, volume=50) # TODO: write a change price test
    assert limit_order_book_price_level._get_order_by_order_id(order_id=3).int_price == int_price_1, f'unexpected order int_price'
    assert limit_order_book_price_level._get_order_by_order_id(order_id=3).volume == 50, f'unexpected order volume'

    limit_order_book_price_level.order_cancel(order_id=3)

    limit_order_book_price_level.order_cancel(order_id=4)
    limit_order_book_price_level.order_cancel(order_id=5)

    depth = limit_order_book_price_level.depth_aggregated()
    assert depth == 0, f'depth is not 0, depth = {depth}'


# TODO: finish this impl, and write tests for update in other contexts
def test_limit_order_book_price_level_update():
    order_1 = Order(
        order_id=100,
        ticker='PYTH',
        order_side=OrderSide.BUY,
        int_price=1234,
        volume=10,
    )

    # lower priority
    order_2 = Order(
        order_id=101,
        ticker='PYTH',
        order_side=OrderSide.BUY,
        int_price=1234,
        volume=20,
    )

    limit_order_book_price_level = LimitOrderBookPriceLevel(order_side=OrderSide.BUY)

    limit_order_book_price_level.order_insert(order_2)

    # todo add function to check priority
    priority = limit_order_book_price_level._query_priority(order_2.order_id)
    assert priority == 0, f'unexpected order priority {priority}, expected priority {0}'

