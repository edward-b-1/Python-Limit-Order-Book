

from limit_order_book.util_functools import consume
from limit_order_book.util_functools import count
from limit_order_book.util_functools import count_matching_orders_by_order_id_from_list_of_orders
from limit_order_book.util_functools import filter_matching_orders_by_order_id_from_list_of_orders
from limit_order_book.util_functools import filter_non_matching_orders_by_order_id_from_list_of_orders

from limit_order_book.validate import *
from limit_order_book.order import Order
from limit_order_book.partial_order import PartialOrder
from limit_order_book.trade import Trade


class PriceLevel:

    def __init__(self, order_side: str):
        assert validate_order_side(order_side), VALIDATE_ORDER_ID_ERROR_STR
        self._order_side = order_side
        # PRICE_LEVEL: list of Order by priority
        self._price_level: list[Order] = []

    def _lambda_order_id_match(order: Order, order_id: int) -> bool:
        return order.order_id == order_id

    def _remove_orders_by_order_id(self, order_id: int) -> list[Order]:
        # TODO: use remove_orders_by_order_id_from_list_of_orders
        removed_orders = self._filter_orders_by_order_id(order_id)
        self._price_level = self._filter_orders_by_order_id_inverse(order_id)
        return removed_orders

    def _order_insert(self, order: Order) -> list[Trade]|None:
        # TODO: self.order_side -> implement it in all functions
        if order.order_side != self._order_side:
            trade_list = []
            while order.volume > 0 and len(self._price_level) > 0:
                maker_order = self._price_level[0]
                trade = maker_order.match(taker_order=order)
                if trade is not None:
                    trade_list.append(trade)
            return trade_list
        else:
            self._price_level.append(order)
            return None

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

    def order_insert(self, partial_order: PartialOrder):
        order_id = partial_order.order_id

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        #order = Order(order_id, ticker, order_side, int_price, volume)
        order = partial_order.to_order()
        return self._order_insert(order)

    def order_update(self, order_id: int, volume: int):
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
            assert self._order_insert(existing_order) is None, f'unexpected order match'

    # TODO: update semantics of others (return partialorder)
    def order_cancel(self, order_id: int) -> PartialOrder:

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
        return order.to_partial_order()