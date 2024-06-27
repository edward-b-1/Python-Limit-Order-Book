
from order import Order


class MultiTickerLimitOrderBook:

    def __init__(self):
        self._limit_order_book_by_ticker = dict()

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        pass

    def _order_trade(self, order: Order)

    def order_insert(self, order: Order):
        order_id = order.order_id

        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order id {order_id}')
        
        ticker = order.ticker

        self.