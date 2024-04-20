
from functools import reduce

from limit_order_book.validate import *
from limit_order_book.order import Order
from limit_order_book.partial_order import PartialOrder
from limit_order_book.trade import Trade

from limit_order_book.price_level import PriceLevel


class LimitOrderBookPriceLevel:

    def __init__(self, order_side: str):
        assert validate_order_side(order_side), VALIDATE_ORDER_ID_ERROR_STR
        self._order_side = order_side
        # PRICE_LEVEL -> list of orders and volumes
        self._price_levels: dict[int, PriceLevel] = {}

    def _initialize_price_level(self, int_price: int):
        if not validate_int_price(int_price):
            raise ValueError(f'price \'{int_price}\' is not a valid integer price')

        if not int_price in self._price_levels:
            self._price_levels[int_price] = PriceLevel(self._order_side)

    def _order_insert(self, partial_order: PartialOrder) -> list[Trade]|None:
        order_side = partial_order.to_order_side()
        int_price = partial_order.to_int_price()

        #if order_side != self.order_side:
        if order_side == 'BUY' and self._order_side == 'SELL':
            # price_level_min = min(self._price_levels.keys())
            # price_level_max = max(self._price_levels.keys())
            price_levels = sorted(self._price_levels.keys())

            matching_price_levels = (
                list(
                    filter(
                        lambda price_level: price_level <= int_price,
                        price_levels,
                    )
                )
            )

            trades = []
            for price_level in matching_price_levels:
                # if partial_order.volume > 0:
                trades.append(
                    self._price_levels[price_level].order_insert(partial_order)
                )
                # else:
                #     break
            return trades
        elif order_side == 'SELL' and self._order_side == 'BUY':
            price_levels = (
                list(
                    reversed(
                        sorted(
                            self._price_levels.keys()
                        )
                    )
                )
            )

            matching_price_levels = (
                list(
                    filter(
                        lambda price_level: price_level >= int_price,
                        price_levels,
                    )
                )
            )

            trades = []
            for price_level in matching_price_levels:
                trades.append(
                    self._price_levels[price_level].order_insert(partial_order)
                )
            return trades
        else:
            return self._price_levels[int_price].order_insert(partial_order)

        # it does not matter if order_side is the same or different,
        # call the same logic (NOTE: can't be done remove this comment)
        # trades = None
        # if order_side == 'BUY':
        #     # search price levels from the lowest sell to int_price (asc)
        #     # if lowest sell > int_price do nothing
        #     trades = limit_order_book_opposite.order_insert(order_id, ticker, order_side, int_price, volume)

        # elif order_side == 'SELL':
        #     trades = limit_order_book_opposite.order_insert(order_id, ticker, order_side, int_price, volume)
        #     # search price levels from the highest buy to int_price (desc)
        #     # if highest buy < int_price do nothing


    def _filter_orders_by_order_id(self, order_id: int) -> list[Order]:
        return (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda price_level: price_level._filter_orders_by_order_id(order_id),
                        self._price_levels.values(),
                    ),
                    [],
                )
            )
        )

    def _remove_orders_by_order_id(self, order_id: int) -> list[Order]:
        '''
        Remove all orders with matching order_id

        Return:
            - list of removed orders
        '''
        return (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda price_level: price_level._remove_orders_by_order_id(order_id),
                        self._price_levels.values(),
                    ),
                    [],
                )
            )
        )

    def _find_order_price_level_by_order_id(self, order_id: int) -> int:
        '''
        Find price level containing an order with matching order_id

        Return:
            - price level (int)
        '''

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
                        self._price_levels.items(),
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
        '''
        Get Order by order id. Assumes that order id exists in this data structure

        Return:
            - Order with order id = `order_id`
        '''
        matching_orders = (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda price_level: price_level._filter_orders_by_order_id(order_id),
                        self._price_levels.values(),
                    ),
                    [],
                )
            )
        )
        assert len(matching_orders) == 1, f'_get_order_by_order_id failed'

        existing_order: Order = matching_orders[0]
        return existing_order

    def _query_priority(self, order_id: int) -> int:
        int_price = self._find_order_price_level_by_order_id(order_id)
        price_level = self._price_levels[int_price]
        return price_level._query_priority(order_id)

    def order_id_exists(self, order_id: int):
        return (
            any(
                filter(
                    lambda price_level: price_level.order_id_exists(order_id),
                    self._price_levels.values(),
                )
            )
        )

    def order_id_count(self, order_id: int) -> int:
        return (
            sum(
                map(
                    lambda price_level: price_level.order_id_count(order_id),
                    self._price_levels.values(),
                )
            )
        )

    def depth(self, int_price: int) -> int:
        self._initialize_price_level(int_price)
        return self._price_levels[int_price].depth()

    def depth_aggregated(self) -> int:
        return (
            sum(
                map(
                    lambda price_level: price_level.depth(),
                    self._price_levels.values(),
                )
            )
        )

    # def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int):
    #     assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
    #     assert validate_order_side(order_side), VALIDATE_INT_PRICE_ERROR_STR
    #     assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
    #     assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

    def order_insert(self, partial_order: PartialOrder) -> list[Trade]|None:
        int_price = partial_order.to_int_price()
        self._initialize_price_level(int_price)

        order_id = partial_order.order_id

        # check the order id doesn't exist
        # TODO: check this logic exists in LimitOrderBook and DoubleLimitOrderBook
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        # TODO: why was this here? does nothing
        #partial_order = partial_order.with_int_price(int_price)
        return self._order_insert(partial_order)

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
            self._price_levels[existing_order_int_price].order_update(order_id, volume)
        else:
            ##existing_order: Order = self._get_order_by_order_id(order_id)
            ##existing_order.set_int_price(int_price)
            # TODO: add order_cancel_pop to return order or make order_cancel return the order
            # should it return a partial order with the int_price removed? (probably no?)
            partial_order = self._price_levels[existing_order_int_price].order_cancel(order_id)
            partial_order.set_int_price(int_price)
            assert self._price_levels[int_price].order_insert(partial_order) is None, f'unexpected order match'
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