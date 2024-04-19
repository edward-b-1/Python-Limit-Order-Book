
from functools import reduce

from limit_order_book.validate import *
from limit_order_book.order import Order
from limit_order_book.partial_order import PartialOrder

from limit_order_book.price_level import PriceLevel


class LimitOrderBookPriceLevel:

    def __init__(self):
        # PRICE_LEVEL -> list of orders and volumes
        self.price_levels: dict[int, PriceLevel] = {}

    def _initialize_price_level(self, int_price: int):
        if not validate_int_price(int_price):
            raise ValueError(f'price \'{int_price}\' is not a valid integer price')

        if not int_price in self.price_levels:
            self.price_levels[int_price] = PriceLevel()

    def _insert_order(self, partial_order: PartialOrder):
        int_price = partial_order.to_int_price()
        self.price_levels[int_price].order_insert(partial_order)

    def _filter_orders_by_order_id(self, order_id: int):
        def filter_empty_list(list: list) -> bool:
            return len(list) > 0

        def extract_single_element_from_list(list: list):
            assert len(list) == 1, f'extract_single_element_from_list failed, length is {len(list)}'
            return list[0]

        return (
            list(
                map(
                    extract_single_element_from_list, # TODO: find better way to do this
                    filter(
                        filter_empty_list,
                        map(
                            lambda price_level: price_level._filter_orders_by_order_id(order_id),
                            self.price_levels.values(),
                        ),
                    ),
                )
            )
        )

    # Note: will actually remove all orders with order_id
    def _remove_orders_by_order_id(self, order_id: int) -> list[Order]:
        def filter_empty_list(list: list) -> bool:
            return len(list) > 0

        removed_orders = (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda price_level: price_level._remove_orders_by_order_id(order_id),
                        self.price_levels.values(),
                    ),
                    [],
                )
            )
        )
        return removed_orders

        # TODO
        return remove_order_by_order_id_from_list_of_orders(self.price_levels.values())

    def _find_order_price_level_by_order_id(self, order_id: int) -> int:

        def select_int_price_level(key_value: tuple[int, PriceLevel]) -> int:
            return key_value[0]

        def filter_by_order_id(key_value: tuple[int, PriceLevel]) -> bool:
            price_level = key_value[1]
            return price_level.order_id_exists(order_id)

        int_price_levels = (
            set(
                map(
                    select_int_price_level,
                    filter(
                        filter_by_order_id,
                        self.price_levels.items(),
                    )
                )
            )
        )

        if len(int_price_levels) == 0:
            raise RuntimeError(f'order_id not found in price_levels')
        elif len(int_price_levels) > 1:
            raise RuntimeError(f'order_id duplicated in multiple price_levels')

        [int_price_level] = int_price_levels
        return int_price_level

    def _get_order_by_order_id(self, order_id: int) -> Order:
        def filter_empty_list(list: list) -> bool:
            return len(list) > 0

        def extract_single_element_from_list(list: list):
            assert len(list) == 1, f'extract_single_element_from_list failed'
            return list[0]

        matching_orders = (
            list(
                map(
                    extract_single_element_from_list,
                    filter(
                        filter_empty_list,
                        map(
                            lambda price_level: price_level._filter_orders_by_order_id(order_id),
                            self.price_levels.values(),
                        ),
                    ),
                )
            )
        )
        assert len(matching_orders) == 1, f'_get_order_by_order_id failed'

        existing_order: Order = matching_orders[0]
        return existing_order

    def _query_priority(self, order_id: int) -> int:
        int_price = self._find_order_price_level_by_order_id(order_id)
        price_level = self.price_levels[int_price]
        return price_level._query_priority(order_id)

    def order_id_exists(self, order_id: int):
        return (
            any(
                filter(
                    lambda price_level: price_level.order_id_exists(order_id),
                    self.price_levels.values(),
                )
            )
        )

    def order_id_count(self, order_id: int) -> int:
        return (
            sum(
                map(
                    lambda price_level: price_level.order_id_count(order_id),
                    self.price_levels.values(),
                )
            )
        )

    def depth(self, int_price: int) -> int:
        self._initialize_price_level(int_price)
        return self.price_levels[int_price].depth()

    def depth_aggregated(self) -> int:
        return (
            sum(
                map(
                    lambda price_level: price_level.depth(),
                    self.price_levels.values(),
                )
            )
        )

    # def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
    #     assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
    #     assert validate_order_side(order_side), VALIDATE_INT_PRICE_ERROR_STR
    #     assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
    #     assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

    def order_insert(self, partial_order: PartialOrder):
        int_price = partial_order.to_int_price()
        self._initialize_price_level(int_price)

        order_id = partial_order.order_id

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        partial_order = partial_order.with_int_price(int_price)
        self._insert_order(partial_order)

    def order_update(self, order_id: int, int_price: int, volume: int):
        assert validate_int_price(int_price) > 0, VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        self._initialize_price_level(int_price)

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot update order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot update order with duplicate order_id {order_id}')

        existing_order_int_price = self._find_order_price_level_by_order_id(order_id)
        if existing_order_int_price == int_price:
            self.price_levels[existing_order_int_price].order_update(order_id, volume)
        else:
            ##existing_order: Order = self._get_order_by_order_id(order_id)
            ##existing_order.set_int_price(int_price)
            # TODO: add order_cancel_pop to return order or make order_cancel return the order
            # should it return a partial order with the int_price removed? (probably no?)
            partial_order = self.price_levels[existing_order_int_price].order_cancel(order_id)
            partial_order.set_int_price(int_price)
            self.price_levels[int_price].order_insert(partial_order)
            # TODO write a test for both of these cases

    def order_cancel(self, order_id: int):
        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot cancel order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot cancel order with duplicate order_id {order_id}')

        # remove matching order
        removed_orders = self._remove_orders_by_order_id(order_id)
        assert len(removed_orders) == 1, f'unexpected number of orders removed in order_cancel'
        order: Order = removed_orders[0]
        return order.to_partial_order()