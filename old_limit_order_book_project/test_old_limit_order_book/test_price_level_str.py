
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.order import Order
from old_limit_order_book.price_level import PriceLevel


def test_price_level_str():

    order_1 = Order(order_id=1, ticker='PYTH', order_side=OrderSide.BUY, int_price=12345678, volume=10)
    order_2 = Order(order_id=2, ticker='PYTH', order_side=OrderSide.BUY, int_price=12345678, volume=20)
    order_3 = Order(order_id=3, ticker='PYTH', order_side=OrderSide.BUY, int_price=12345678, volume=30)

    price_level = PriceLevel(order_side=OrderSide.BUY, int_price=12345678)

    price_level.order_insert(order_1)
    price_level.order_insert(order_2)
    price_level.order_insert(order_3)

    price_level_str = str(price_level)

    assert price_level_str == f'BUY,1234.5678,60', 'test_price_level_str failed'
