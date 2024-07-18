
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.exceptions import DuplicateOrderIdError

from typeguard import typechecked


@typechecked
class OrderPriorityQueue():

    def __init__(
        self,
        ticker: Ticker,
        order_side: OrderSide,
        int_price: IntPrice,
    ) -> None:
        self._ticker = ticker
        self._order_side = order_side
        self._int_price = int_price
        self._queue: list[Order] = []

    def __len__(self) -> int:
        '''Return the queue length. This is the same as the number of orders in
        the queue.

        Returns:
            int: Number of orders in the queue
        '''
        return len(self._queue)

    def number_of_orders(self) -> int:
        '''Calculate the number of orders in the queue

        Returns:
            int: Number of orders in the queue
        '''
        return len(self._queue)


    def trade(self, taker_order: Order) -> list[Trade]:
        assert taker_order.to_ticker() == self._ticker, f'OrderPriorityQueue.trade ticker mismatch'
        assert taker_order.to_order_side().other_side() == self._order_side, f'OrderPriorityQueue.trade order side mismatch'

        trade_list = []
        while taker_order.to_volume() > Volume(0) and len(self._queue) > 0:
            maker_order = self._queue[0]
            trade = maker_order.match(taker_order)
            if trade is not None:
                trade_list.append(trade)
                self._queue = (
                    list(
                        filter(
                            lambda order: order.to_volume().is_not_zero(),
                            self._queue,
                        )
                    )
                )
            else:
                raise RuntimeError(f'OrderPriorityQueue.trade: unreachable condition')
        return trade_list


    def insert(self, order: Order):
        assert order.to_ticker() == self._ticker, f'OrderPriorityQueue.insert ticker mismatch'
        assert order.to_order_side() == self._order_side, f'OrderPriorityQueue.insert order side mismatch'
        assert order.to_int_price() == self._int_price, f'OrderPriorityQueue.insert int price mismatch'

        order_id = order.to_order_id()

        if self.order_id_exists(order_id):
            raise DuplicateOrderIdError(order_id)

        self._queue.append(order)


    def update(self, order_id: OrderId, int_price: IntPrice, volume: Volume) -> Order|None:
        '''Update an order price or volume

        Args:
            order_id (OrderId): order id of target order
            int_price (IntPrice): new price value
            volume (Volume): new volume value

        One or both of `int_price` and `volume` must be specified. If both
        values are missing, an error is raised.

        If the values of the price and volume match the existing values, then
        the order priority is unchanged. Otherwise, if the price changes, or the
        volume is increased, the order loses priority. In this case it is
        removed from the queue and returned. If the only change is the volume
        is decreased, the order does not lose priority and None is returned.

        Returns:
            Order|None: If the update operation causes the order to lose priority
            then the order is returned. It must be re-inserted by the caller.
        '''
        existing_orders = self._filter_orders_matching_order_id(order_id)
        assert len(existing_orders) <= 1, f'OrderPriorityQueue.update invalid number of orders found'

        if len(existing_orders) < 1:
            return None

        existing_order = existing_orders[0]
        existing_int_price = existing_order.to_int_price()
        existing_volume = existing_order.to_volume()
        existing_order.set_int_price(int_price)
        existing_order.set_volume(volume)

        if int_price == existing_int_price:
            if existing_volume < volume:
                # priority reduced
                self._queue = self._filter_orders_not_matching_order_id(order_id)
                # to reduce the priority, remove the order from the queue and
                # return it to the calling data structures
                return existing_order
            else:
                return None
        else:
            # remove order
            self._queue = self._filter_orders_not_matching_order_id(order_id)
            return existing_order


    def update_int_price(self, order_id: OrderId, int_price: IntPrice) -> Order|None:
        '''Update an order price

        Args:
            order_id (OrderId): order id of target order
            int_price (IntPrice): new price value

        If the value of the price matches the existing value, then the order
        priority is unchanged. Otherwise, if the price changes, the order loses
        priority. In this case it is removed from the queue and returned.

        Returns:
            Order|None: If the update operation causes the order to lose priority
            then the order is returned. It must be re-inserted by the caller.
        '''
        existing_orders = self._filter_orders_matching_order_id(order_id)
        assert len(existing_orders) <= 1, f'OrderPriorityQueue.update_int_price invalid number of orders found'

        if len(existing_orders) < 1:
            return None

        existing_order = existing_orders[0]
        existing_int_price = existing_order.to_int_price()
        existing_order.set_int_price(int_price)

        if int_price == existing_int_price:
            return None
        else:
            # remove order
            self._queue = self._filter_orders_not_matching_order_id(order_id)
            return existing_order


    def update_volume(self, order_id: OrderId, volume: Volume) -> Order|None:
        '''Update an order volume

        Args:
            order_id (OrderId): order id of target order
            volume (Volume): new volume value

        If the value of volume matches the existing value, then the order
        priority is unchanged. Otherwise, if the volume is increased, the order
        loses priority. In this case it is removed from the queue and returned.
        If the only change is the volume is decreased, the order does not lose
        priority and None is returned.

        Returns:
            Order|None: If the update operation causes the order to lose priority
            then the order is returned. It must be re-inserted by the caller.
        '''
        existing_orders = self._filter_orders_matching_order_id(order_id)
        assert len(existing_orders) <= 1, f'OrderPriorityQueue.update_volume invalid number of orders found'

        if len(existing_orders) < 1:
            return None

        existing_order = existing_orders[0]
        existing_volume = existing_order.to_volume()
        existing_order.set_volume(volume)

        if existing_volume < volume:
            # priority reduced
            self._queue = self._filter_orders_not_matching_order_id(order_id)
            # to reduce the priority, remove the order from the queue and
            # return it to the calling data structures
            return existing_order
        else:
            return None


    def cancel(self, order_id: OrderId) -> Order|None:
        '''Cancel an order. The order is returned if it is found

        Args:
            order_id (OrderId): Order id of target order to cancel

        Returns:
            Order|None: If an order is found and cancelled, it is returned
        '''
        orders = self._remove_orders_matching_order_id(order_id)

        assert len(orders) <= 1, f'OrderPriorityQueue.cancel invalid number of orders found'

        if len(orders) == 1:
            return orders[0]
        return None


    def cancel_partial(self, order_id: OrderId, volume: Volume) -> None:
        '''Partially cancel an existing order by reducing the order volume by `volume`

        Args:
            order_id (OrderId): Order id of target order
            volume (Volume): Quantity to reduce volume by
        '''
        existing_orders = self._filter_orders_matching_order_id(order_id)
        assert len(existing_orders) <= 1, f'OrderPriorityQueue.cancel_partial invalid number of orders found'

        if len(existing_orders) < 1:
            return None

        existing_order = existing_orders[0]
        existing_order.reduce_volume(volume)

        if existing_order.to_volume().is_zero():
            existing_orders = self._remove_orders_matching_order_id(order_id)
            assert len(existing_orders) <= 1, f'OrderPriorityQueue.cancel_partial invalid number of orders found'


    def order_id_exists(self, order_id: OrderId) -> bool:
        matching_order_ids = (
            list(
                filter(
                    lambda order_order_id: order_order_id == order_id,
                    map(
                        lambda order: order.to_order_id(),
                        self._queue,
                    )
                )
            )
        )

        assert len(matching_order_ids) <= 1, f'OrderPriorityQueue.order_id_exists invalid number of order ids found'
        return len(matching_order_ids) == 1


    def _filter_orders_matching_order_id(self, order_id: OrderId) -> list[Order]:
        return (
            list(
                filter(
                    lambda order: order.to_order_id() == order_id,
                    self._queue,
                )
            )
        )

    def _filter_orders_not_matching_order_id(self, order_id: OrderId) -> list[Order]:
        return (
            list(
                filter(
                    lambda order: order.to_order_id() != order_id,
                    self._queue,
                )
            )
        )

    def _remove_orders_matching_order_id(self, order_id: OrderId) -> list[Order]:
        matched_orders = self._filter_orders_matching_order_id(order_id)
        self._queue = self._filter_orders_not_matching_order_id(order_id)
        return matched_orders

    def total_volume(self) -> Volume:
        '''Calculate the total volume of all orders in the queue

        Returns:
            Volume: Total volume of all orders in the queue
        '''
        total_volume = (
            sum(
                map(
                    lambda order: order.to_volume()._volume,
                    self._queue,
                )
            )
        )
        return Volume(total_volume)

