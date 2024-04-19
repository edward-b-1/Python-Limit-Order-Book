
from limit_order_book.limit_order_book import PartialOrder

def test_partial_order():
    partial_order = PartialOrder()

    try:
        partial_order.to_order()
    except RuntimeError as e:
        assert str(e) == f'PartialOrder has missing fields'

    partial_order.set_order_id(1).set_ticker('PYTH').set_order_side('BUY').set_int_price(1234)

    try:
        partial_order.to_order()
    except RuntimeError as e:
        assert str(e) == f'PartialOrder has missing fields'

    partial_order.set_volume(10)
    order = partial_order.to_order()

    assert order.order_id == 1, 'unexpected value for order_id'
    assert order.order_side == 'BUY', 'unexpected value for order_side'
    assert order.int_price == 1234, 'unexpected value for int_price'
    assert order.volume == 10, 'unexpected value for volume'

