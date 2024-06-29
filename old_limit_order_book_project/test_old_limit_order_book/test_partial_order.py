
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.limit_order_book import Order

def test_partial_order():
    order = Order(
        order_id=1,
        ticker='PYTH',
        order_side=OrderSide.BUY,
        int_price=1234,
        volume=10,
    )

    assert order.order_id == 1, 'unexpected value for order_id'
    assert order.ticker == 'PYTH', 'unexpected value for ticker'
    assert order.order_side == OrderSide.BUY, 'unexpected value for order_side'
    assert order.int_price == 1234, 'unexpected value for int_price'
    assert order.volume == 10, 'unexpected value for volume'

