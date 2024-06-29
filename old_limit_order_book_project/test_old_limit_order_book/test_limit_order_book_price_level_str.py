
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.order import Order
from old_limit_order_book.limit_order_book_price_level import LimitOrderBookPriceLevel


def test_limit_order_book_price_level_str_buy():

    order_1 = Order(order_id=1, ticker='PYTH', order_side=OrderSide.BUY, int_price=12345678, volume=10)
    order_2 = Order(order_id=2, ticker='PYTH', order_side=OrderSide.BUY, int_price=12345678, volume=20)
    order_3 = Order(order_id=3, ticker='PYTH', order_side=OrderSide.BUY, int_price=12345678, volume=30)

    order_4 = Order(order_id=4, ticker='PYTH', order_side=OrderSide.BUY, int_price=12340000, volume=100)
    order_5 = Order(order_id=5, ticker='PYTH', order_side=OrderSide.BUY, int_price=12340000, volume=200)

    order_6 = Order(order_id=6, ticker='PYTH', order_side=OrderSide.BUY, int_price=10000, volume=200)

    limit_order_book_price_level = LimitOrderBookPriceLevel(order_side=OrderSide.BUY)

    limit_order_book_price_level.order_insert(order_1)
    limit_order_book_price_level.order_insert(order_2)
    limit_order_book_price_level.order_insert(order_3)
    limit_order_book_price_level.order_insert(order_4)
    limit_order_book_price_level.order_insert(order_5)
    limit_order_book_price_level.order_insert(order_6)

    limit_order_book_price_level_str = str(limit_order_book_price_level)

    expected_str = (
        f'BUY,1234.5678,60\n'
        f'BUY,1234,300\n'
        f'BUY,1,200'
    )

    assert limit_order_book_price_level_str == expected_str, 'test_limit_order_book_price_level_str failed'


def test_limit_order_book_price_level_str_sell():

    order_1 = Order(order_id=1, ticker='PYTH', order_side=OrderSide.SELL, int_price=12345678, volume=10)
    order_2 = Order(order_id=2, ticker='PYTH', order_side=OrderSide.SELL, int_price=12345678, volume=20)
    order_3 = Order(order_id=3, ticker='PYTH', order_side=OrderSide.SELL, int_price=12345678, volume=30)

    order_4 = Order(order_id=4, ticker='PYTH', order_side=OrderSide.SELL, int_price=12340000, volume=100)
    order_5 = Order(order_id=5, ticker='PYTH', order_side=OrderSide.SELL, int_price=12340000, volume=200)

    order_6 = Order(order_id=6, ticker='PYTH', order_side=OrderSide.SELL, int_price=10000, volume=200)

    limit_order_book_price_level = LimitOrderBookPriceLevel(order_side=OrderSide.SELL)

    limit_order_book_price_level.order_insert(order_1)
    limit_order_book_price_level.order_insert(order_2)
    limit_order_book_price_level.order_insert(order_3)
    limit_order_book_price_level.order_insert(order_4)
    limit_order_book_price_level.order_insert(order_5)
    limit_order_book_price_level.order_insert(order_6)

    limit_order_book_price_level_str = str(limit_order_book_price_level)

    expected_str = (
        f'SELL,1234.5678,60\n'
        f'SELL,1234,300\n'
        f'SELL,1,200'
    )

    assert limit_order_book_price_level_str == expected_str, 'test_limit_order_book_price_level_str failed'
