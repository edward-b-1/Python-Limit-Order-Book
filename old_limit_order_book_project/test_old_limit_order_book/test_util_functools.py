
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.order import Order
from old_limit_order_book.util_functools import remove_order_by_order_id_from_list_of_orders


def test_remove_order_by_order_id_from_list_of_orders():
    ticker = 'PYTH'
    order_side = OrderSide.BUY
    int_price = 1000
    volume = 20

    order_1 = Order(1, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)
    order_2 = Order(2, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)
    order_3 = Order(3, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)
    order_4 = Order(4, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)
    order_5 = Order(5, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)

    list_of_orders = [
        order_1,
        order_2,
        order_3,
        order_4,
        order_5,
    ]

    removed_orders = remove_order_by_order_id_from_list_of_orders(
        list_of_orders=list_of_orders,
        order_id=3,
    )
    assert len(removed_orders) == 1, f'test_remove_order_by_order_id_from_list_of_orders failed'
    removed_order = removed_orders[0]
    assert removed_order.order_id == 3, f'test_remove_order_by_order_id_from_list_of_orders failed'
    assert removed_order.ticker == ticker, f'test_remove_order_by_order_id_from_list_of_orders failed'
    assert removed_order.order_side == order_side, f'test_remove_order_by_order_id_from_list_of_orders failed'
    assert removed_order.int_price == int_price, f'test_remove_order_by_order_id_from_list_of_orders failed'
    assert removed_order.volume == volume, f'test_remove_order_by_order_id_from_list_of_orders failed'


def test_remove_order_by_order_id_from_list_of_orders_2():
    ticker = 'PYTH'
    order_side = OrderSide.BUY
    int_price = 1000
    volume = 20

    order_1 = Order(1, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)
    order_2 = Order(2, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)
    order_3 = Order(3, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)
    order_4 = Order(4, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)
    order_5 = Order(5, ticker=ticker, order_side=order_side, int_price=int_price, volume=volume)

    list_of_orders = [
        order_1,
        order_2,
        order_3,
        order_4,
        order_5,
    ]

    removed_orders = remove_order_by_order_id_from_list_of_orders(
        list_of_orders=list_of_orders,
        order_id=3,
    )

    assert len(removed_orders) == 1, f'test_remove_order_by_order_id_from_list_of_orders_2 failed'