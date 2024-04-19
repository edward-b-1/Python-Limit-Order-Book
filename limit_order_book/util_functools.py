
from functools import reduce

from limit_order_book.limit_order_book import Order


def filter_matching_orders_by_order_id_from_list_of_orders(
    list_of_orders: list[Order],
    order_id: int,
) -> list[Order]:
    lambda_order_id_match = lambda order, order_id: order.order_id == order_id
    return (
        list(
            filter(
                lambda order: lambda_order_id_match(order, order_id),
                list_of_orders,
            )
        )
    )

def filter_non_matching_orders_by_order_id_from_list_of_orders(
    list_of_orders: list[Order],
    order_id: int,
) -> list[Order]:
    lambda_order_id_match = lambda order, order_id: order.order_id == order_id
    return (
        list(
            filter(
                lambda order: not lambda_order_id_match(order, order_id),
                list_of_orders,
            )
        )
    )

def remove_order_by_order_id_from_list_of_orders(
    list_of_orders: list[Order],
    order_id: int,
) -> list[Order]:

    removed_orders = filter_matching_orders_by_order_id_from_list_of_orders(list_of_orders, order_id)
    list_of_orders = filter_non_matching_orders_by_order_id_from_list_of_orders(list_of_orders, order_id)
    return removed_orders

def remove_order_by_order_id_from_list_of_orders_2(
    list_of_orders: list[Order],
    order_id: int,
) -> list[Order]:
    # def filter_empty_list(list: list) -> bool:
    #     return len(list) > 0

    filter_empty_list = lambda list: len(list) > 0

    removed_orders = (
        list(
            reduce(
                list.__add__,
                filter(
                    filter_empty_list,
                    map(
                        lambda price_level: price_level._remove_orders_by_order_id(order_id),
                        list_of_orders,
                    ),
                ),
                [],
            )
        )
    )
    return removed_orders