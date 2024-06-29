

from dataclasses import dataclass


@dataclass
class Trade():
    order_id_1: int
    order_id_2: int
    quantity: int

    # def __init__(self, order_id_1: int, order_id_2: int, quantity: int) -> None:
    #     self.order_id_1 = order_id_1
    #     self.order_id_2 = order_id_2
    #     self.quantity = quantity


@dataclass
class Order():
    order_id: int
    order_side: str
    quantity: int

    def match(self, taker_order) -> Trade|None:
        if self.order_side == taker_order.order_side:
            return None

        matched_quantity = min(self.quantity, taker_order.quantity)

        self.quantity -= matched_quantity
        taker_order.quantity -= matched_quantity

        return Trade(
            order_id_1=self.order_id,
            order_id_2=taker_order.order_id,
            quantity=matched_quantity,
        )


class OrderBook():

    def __init__(self) -> None:
        self._buy_orders: list[Trade] = []
        self._sell_orders: list[Trade] = []

    def insert(self, order_id: int, order_side: str, quantity: int) -> list[Trade]:
        #assert order_side == 'buy' or order_side == 'sell'
        taker_order = Order(order_id, order_side, quantity)
        trades = []

        if order_side == 'buy':
            while taker_order.quantity > 0 and len(self._sell_orders) > 0:
                maker_order = self._sell_orders[0]
                trade = maker_order.match(taker_order)
                assert trade is not None
                trades.append(trade)
                if maker_order.quantity == 0:
                    self._sell_orders = self._sell_orders[1:]
            if taker_order.quantity > 0:
                self._buy_orders.append(taker_order)
        elif order_side == 'sell':
            while taker_order.quantity > 0 and len(self._buy_orders) > 0:
                maker_order = self._buy_orders[0]
                trade = maker_order.match(taker_order)
                assert trade is not None
                trades.append(trade)
                if maker_order.quantity == 0:
                    self._buy_orders = self._buy_orders[1:]
            if taker_order.quantity > 0:
                self._sell_orders.append(taker_order)
        return trades

        # if order_side == 'buy':
        #     same_side_order_queue = self._buy_orders
        #     other_side_order_queue = self._sell_orders
        # elif order_side == 'sell':
        #     same_side_order_queue = self._sell_orders
        #     other_side_order_queue = self._buy_orders

        # while taker_order.quantity > 0 and len(other_side_order_queue) > 0:
        #     maker_order = other_side_order_queue[0]
        #     trade = maker_order.match(taker_order)
        #     assert trade is not None
        #     trades.append(trade)
        #     if maker_order.quantity == 0:
        #         other_side_order_queue = other_side_order_queue[1:]
        # if taker_order.quantity > 0:
        #     same_side_order_queue.append(taker_order)

        # if order_side == 'buy':
        #     self._sell_orders = other_side_order_queue
        # elif order_side == 'self':
        #     self._buy_orders = other_side_order_queue


    def modify(self, order_id: int, quantity: int) -> None:
        existing_orders = (
            list(
                filter(
                    lambda order: order.order_id == order_id,
                    self._buy_orders,
                )
            ) + list(
                filter(
                    lambda order: order.order_id == order_id,
                    self._sell_orders,
                )
            )
        )
        assert len(existing_orders) == 1
        existing_order = existing_orders[0]
        existing_order.quantity = quantity

    def cancel(self, order_id: int) -> None:
        self._buy_orders = (
            list(
                filter(
                    lambda order: order.order_id != order_id,
                    self._buy_orders,
                )
            )
        )
        self._sell_orders = (
            list(
                filter(
                    lambda order: order.order_id != order_id,
                    self._sell_orders,
                )
            )
        )


def main():

    order_book = OrderBook()

    order_book.insert(
        order_id=1,
        order_side='buy',
        quantity=10,
    )
    order_book.cancel(order_id=1)

    trades = order_book.insert(
        order_id=2,
        order_side='sell',
        quantity=10,
    )
    assert trades == []

    order_book.modify(
        order_id=2,
        quantity=5,
    )

    trades = order_book.insert(
        order_id=3,
        order_side='buy',
        quantity=10,
    )
    assert trades == [Trade(order_id_1=2, order_id_2=3, quantity=5)]

    trades = order_book.insert(
        order_id=4,
        order_side='sell',
        quantity=5,
    )
    assert trades == [Trade(order_id_1=3, order_id_2=4, quantity=5)]


if __name__ == '__main__':
    main()

