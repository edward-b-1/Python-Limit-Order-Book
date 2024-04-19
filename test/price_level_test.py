
from limit_order_book.limit_order_book import PartialOrder
from limit_order_book.limit_order_book import PriceLevel


def test_price_level():
    ticker = 'PYTH'
    order_side = 'BUY'
    int_price = 1000
    partial_order = PartialOrder().set_ticker(ticker).set_order_side(order_side).set_int_price(int_price)

    partial_order_1 = partial_order.with_order_id(1).with_volume(10)
    partial_order_2 = partial_order.with_order_id(2).with_volume(20)
    partial_order_3 = partial_order.with_order_id(3).with_volume(30)

    price_level = PriceLevel()

    # price_level.order_insert(order_id=1, ticker=ticker, order_side=order_side, int_price=int_price, volume=10)
    # price_level.order_insert(order_id=2, ticker=ticker, order_side=order_side, int_price=int_price, volume=20)
    # price_level.order_insert(order_id=3, ticker=ticker, order_side=order_side, int_price=int_price, volume=30)
    price_level.order_insert(partial_order_1)
    price_level.order_insert(partial_order_2)
    price_level.order_insert(partial_order_3)

    try:
        price_level.order_insert(partial_order_2)
    except RuntimeError as e:
        assert str(e) == f'cannot insert order with existing order_id {partial_order_2.order_id}'

    remaining_partial_order_2 = price_level.order_cancel(order_id=2)
    assert remaining_partial_order_2 == partial_order_2, (
        f'remaining PartialOrder {remaining_partial_order_2} does not match original PartialOrder {partial_order_2}'
    )

    order_id = 2
    try:
        price_level.order_cancel(order_id)
    except RuntimeError as e:
        assert str(e) == f'cannot cancel order with missing order_id {order_id}'

    remaining_partial_order_1 = price_level.order_cancel(order_id=1)
    assert remaining_partial_order_1 == partial_order_1, (
        f'remaining PartialOrder {remaining_partial_order_1} does not match original PartialOrder {partial_order_1}'
    )

    price_level.order_update(order_id=3, volume=50)
    assert price_level._get_order_by_order_id(order_id=3).volume == 50, f'unexpected order volume'

    remaining_partial_order_3 = price_level.order_cancel(order_id=3)
    assert remaining_partial_order_3 == partial_order_3.with_volume(50), (
        f'remaining PartialOrder {remaining_partial_order_3} does not match original PartialOrder {partial_order_3}'
    )

    depth = price_level.depth()
    assert depth == 0, f'depth is not 0, depth = {depth}'

