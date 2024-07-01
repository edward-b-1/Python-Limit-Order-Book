
from limit_order_book.types.order_id import OrderId
from limit_order_book.ticker import Ticker
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.order_side import OrderSide
from limit_order_book.trade import Trade
from limit_order_book.order import Order

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


    def number_of_orders(self) -> int:
        return len(self._queue)


    def trade(self, taker_order: Order) -> list[Trade]:
        assert taker_order.to_ticker() == self._ticker, f'OrderPriorityQueue.trade ticker mismatch'
        assert taker_order.to_order_side().other_side() == self._order_side, f'OrderPriorityQueue.trade order side mismatch'
        #assert taker_order.to_int_price() == self._int_price, f'OrderPriorityQueue.trade int price mismatch'

        trade_list = []
        while taker_order.to_volume() > Volume(0) and len(self._queue) > 0:
            maker_order = self._queue[0]
            trade = maker_order.match(taker_order)
            if trade is not None:
                trade_list.append(trade)
                if maker_order.to_volume().is_zero():
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
            raise RuntimeError(f'duplicate order id {order_id}')

        self._queue.append(order)


    def update(self, order: Order) -> Order|None:
        assert order.to_ticker() == self._ticker, f'OrderPriorityQueue.update ticker mismatch'
        assert order.to_order_side() == self._order_side, f'OrderPriorityQueue.update order side mismatch'
        #assert order.to_int_price() == self._int_price, f'OrderPriorityQueue.update int price mismatch'
        # price might be changing

        order_id = order.to_order_id()
        existing_orders = self._filter_orders_matching_order_id(order_id)
        assert len(existing_orders) <= 1, f'OrderPriorityQueue.update invalid number of orders found'

        if len(existing_orders) < 1:
            return None
        else:
            existing_order = existing_orders[0]

            int_price = order.to_int_price()
            existing_int_price = existing_order.to_int_price()

            if int_price != existing_int_price:
                # if the price level is different, it is possible to generate a
                # trade, and the order needs to be sent to a different price
                # level - not something we can do here

                volume = order.to_volume()
                existing_volume = existing_order.to_volume()

                if volume == existing_volume:
                    pass
                elif volume != existing_volume:
                    existing_order.set_volume(volume)

                # remove order
                self._queue = self._filter_orders_not_matching_order_id(order_id)
                existing_order.set_int_price(int_price)
                return existing_order
            else:
                volume = order.to_volume()
                existing_volume = existing_order.to_volume()

                if volume == existing_volume:
                    pass
                elif volume < existing_volume:
                    existing_order.set_volume(volume)
                else:
                    # priority reduced
                    self._queue = self._filter_orders_not_matching_order_id(order_id)
                    existing_order.set_volume(volume)
                    self.insert(existing_order)

                return None


    # def update(self, order: Order) -> Order|None:
    #     assert order.to_ticker() == self._ticker, f'OrderPriorityQueue.update ticker mismatch'
    #     assert order.to_order_side() == self._order_side, f'OrderPriorityQueue.update order side mismatch'
    #     assert order.to_int_price() == self._int_price, f'OrderPriorityQueue.update int price mismatch'

    #     order_id = order.to_order_id()
    #     existing_order = self.find_order_by_order_id(order_id)
    #     assert existing_order is not None, f'order not found'

    #     volume = order.to_volume()
    #     existing_volume = existing_order.to_volume()

    #     if volume > existing_volume:
    #         # priority reduced
    #         existing_order = self.cancel(order_id)
    #         existing_order.set_volume(volume)
    #         self.insert(existing_order)
    #         return None
    #     else:
    #         existing_order.set_volume(volume)
    #         return None

    #     # how I think the semantics for this should work
    #     # if the order volume is made smaller, just make that change to the order
    #     # doing so requires checking that the order id can be found in the queue
    #     # and the usual checks in ticker, order_side and int_price should also
    #     # be done.
    #     # if the order volume is made larger, then remove the order and replace
    #     # it with an appended new order (this lowers the priority). otherwise the
    #     # checks are the same
    #     # if the int_price is changed, then the order should be returned. this
    #     # implies that None should be returned in the above two cases. also -
    #     # the int_price is allowed to be different
    #     #
    #     # remaining questions: if the order id is not found, should that be an
    #     # error? or will we call update on all queues for all price levels in
    #     # an order_side for a limit order book?
    #     # in other words, a LOB contains 2x order sides
    #     # LOB->2x OrderSide, OrderSide->PriceLevels->Queue
    #     # do we call update() on all levels of an OrderSide?
    #     #
    #     # what if the order side changes? well - you can't change the order side
    #     # so if the order id isn't found in the side specified then this presumably
    #     # has to be an error


    # TODO: use same semantics here as update?
    def cancel(self, order_id: OrderId) -> Order|None:
        orders = self._remove_orders_matching_order_id(order_id)

        assert len(orders) <= 1, f'OrderPriorityQueue.cancel invalid number of orders found'

        if len(orders) == 1:
            return orders[0]
        return None


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


    # def find_order_by_order_id(self, order_id: OrderId) -> Order|None:
    #     matching_orders = self._filter_orders_matching_order_id(order_id)

    #     assert len(matching_orders) <= 1, f'OrderPriorityQueue.find_order_by_order_id invalid number of orders found'

    #     if len(matching_orders) == 1:
    #         return matching_orders[0]
    #     return None


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
        total_volume = (
            sum(
                map(
                    lambda order: order.to_volume()._volume,
                    self._queue,
                )
            )
        )
        return Volume(total_volume)

