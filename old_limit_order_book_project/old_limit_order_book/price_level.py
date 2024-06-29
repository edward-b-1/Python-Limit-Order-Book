

from old_limit_order_book.util_functools import count_matching_orders_by_order_id_from_list_of_orders
from old_limit_order_book.util_functools import filter_matching_orders_by_order_id_from_list_of_orders
from old_limit_order_book.util_functools import filter_non_matching_orders_by_order_id_from_list_of_orders
from old_limit_order_book.util_functools import filter_orders_with_zero_volume_from_list_of_orders

from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.validate import *
from old_limit_order_book.order import Order
from old_limit_order_book.trade import Trade

from util_io.util_encode import convert_int_price_to_price_string


class PriceLevel:

    def __init__(self, order_side: str, int_price: int):
        assert validate_order_side(order_side), VALIDATE_ORDER_ID_ERROR_STR
        self._order_side = order_side # TODO: validate orders inserted have correct values for order_side and int_price
        self._int_price = int_price
        # PRICE_LEVEL: list of Order by priority
        self._price_level: list[Order] = []

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        def format_price_level_str(order_side: str, int_price: int, total_volume: int):
            price = convert_int_price_to_price_string(int_price)
            return f'{order_side},{price},{total_volume}'

        total_volume = (
            sum(
                map(
                    lambda order: order.volume,
                    self._price_level,
                )
            )
        )

        int_price = self._int_price

        return format_price_level_str(self._order_side, int_price, total_volume)

    def debug_str(self) -> str:
        return (
            ' '.join(
                map(
                    lambda order: order.debug_str(),
                    self._price_level,
                )
            )
        )

    def _lambda_order_id_match(order: Order, order_id: int) -> bool:
        return order.order_id == order_id

    def _remove_orders_by_order_id(self, order_id: int) -> list[Order]:
        # TODO: use remove_orders_by_order_id_from_list_of_orders
        removed_orders = self._filter_orders_by_order_id(order_id)
        self._price_level = self._filter_orders_by_order_id_inverse(order_id)
        return removed_orders

    def _remove_orders_with_zero_volume(self) -> None:
        self._price_level = self._filter_orders_with_zero_volume()

    def _order_insert(self, order: Order) -> list[Trade]:
        if order.order_side != self._order_side:
            taker_order = order
            trade_list = []
            while taker_order.volume > 0 and len(self._price_level) > 0:
                maker_order = self._price_level[0]
                trade = maker_order.match(taker_order)
                if trade is not None:
                    trade_list.append(trade)
                    self._remove_orders_with_zero_volume()
            return trade_list
        else:
            self._price_level.append(order)
            return []

    def _filter_orders_with_zero_volume(self) -> None:
        return filter_orders_with_zero_volume_from_list_of_orders(
            self._price_level,
        )

    def _filter_orders_by_order_id(self, order_id: int) -> list[Order]:
        return filter_matching_orders_by_order_id_from_list_of_orders(
            self._price_level,
            order_id,
        )

    def _filter_orders_by_order_id_inverse(self, order_id: int) -> list[Order]:
        return filter_non_matching_orders_by_order_id_from_list_of_orders(
            self._price_level,
            order_id,
        )

    def _count_orders_by_order_id(self, order_id: int):
        return count_matching_orders_by_order_id_from_list_of_orders(
            self._price_level,
            order_id,
        )

    def order_id_exists(self, order_id: int) -> bool:
        return self._count_orders_by_order_id(order_id) > 0

    def order_id_count(self, order_id: int) -> int:
        return self._count_orders_by_order_id(order_id)

    # filter, get_or_none and get could perhaps be merged
    # filter just filters, doesn't care if there are 0, 1 or more orders
    # get requires that there is exactly 1 order
    # get_or_none requires 1 or none

    # TODO: might not have a use for this?
    def _get_order_or_none_by_order_id(self, order_id: int) -> Order|None:

        matching_orders = self._filter_orders_by_order_id(order_id)
        assert len(matching_orders) <= 1, 'get_order_or_none_by_order_id failed'

        existing_order: Order|None = None
        if len(matching_orders) == 1:
            existing_order = matching_orders[0]

        return existing_order

    # TODO: implement in terms of _get_order_or_none_by_order_id
    def _get_order_by_order_id(self, order_id: int) -> Order:

        matching_orders = self._filter_orders_by_order_id(order_id)
        assert len(matching_orders) == 1, '_get_order_by_order_id failed'

        existing_order: Order = matching_orders[0]
        return existing_order

    def _query_priority(self, order_id: int) -> int:
        #matching_order = next(order for order in self.price_level if _lambda_order_id_match(order, order_id))
        #priority = self.price_level.index(matching_order)
        _lambda_order_id_match = PriceLevel._lambda_order_id_match
        index = (
            next(
                index for (index, order) in enumerate(self._price_level)
                    if _lambda_order_id_match(order, order_id))
        )
        return index

    def depth(self) -> int:
        return len(self._price_level)

    def volume(self) -> int:
        return (
            sum(
                map(
                    lambda order: order.to_volume(),
                    self._price_level,
                )
            )
        )

    def order_insert(self, order: Order) -> list[Trade]:
        order_id = order.order_id

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        #order = Order(order_id, ticker, order_side, int_price, volume)
        trade_list = self._order_insert(order)
        return trade_list

    def order_update(self, order_id: int, volume: int) -> None:
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot update order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot update order with duplicate order_id {order_id}')

        existing_order = self._get_order_by_order_id(order_id)

        existing_order_volume = existing_order.volume
        existing_order.volume = volume

        if volume <= existing_order_volume:
            pass
        else:
            # reduce order priority if order volume is increased
            self._remove_orders_by_order_id(order_id)
            trade_list = self._order_insert(existing_order)
            assert len(trade_list) == 0, f'unexpected order match'

    # TODO: update semantics of others (return partialorder)
    def order_cancel(self, order_id: int) -> Order:

        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot cancel order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot cancel order with duplicate order_id {order_id}')

        # remove matching order
        #order = self._get_order_by_order_id(order_id)
        removed_orders = self._remove_orders_by_order_id(order_id)
        assert len(removed_orders) == 1, f'unexpected number of orders removed in order_cancel'
        order: Order = removed_orders[0]
        return order