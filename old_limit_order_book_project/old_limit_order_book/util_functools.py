
from functools import reduce

from old_limit_order_book.order import Order


def consume(iterable):
    '''
    Consume an iterable to end and discard the results
    '''
    for _ in iterable:
        pass


# a count functional like `filter`, `map`, `reduce`
def count(iterable) -> int:
    return sum(1 for _ in iterable)


def count_matching_orders_by_order_id_from_list_of_orders(
    list_of_orders: list[Order],
    order_id: int,
) -> int:
    lambda_order_id_match = lambda order, order_id: order.order_id == order_id
    return (
        count(
            filter(
                lambda order: lambda_order_id_match(order, order_id),
                list_of_orders,
            )
        )
    )


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


def filter_orders_with_zero_volume_from_list_of_orders(
    list_of_orders: list[Order],
) -> list[Order]:
    lambda_order_volume_positive = lambda order: order.volume > 0
    return (
        list(
            filter(
                lambda order: lambda_order_volume_positive(order),
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

