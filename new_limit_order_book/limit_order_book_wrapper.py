

from new_limit_order_book.types.order_id import OrderId
from new_limit_order_book.order_side import OrderSide
from new_limit_order_book.order import Order
from new_limit_order_book.trade import Trade
from new_limit_order_book.ticker import Ticker
from new_limit_order_book.top_of_book import TopOfBook
from new_limit_order_book.multi_ticker_limit_order_book import MultiTickerLimitOrderBook


class LimitOrderBook():

    def __init__(self) -> None:
        self._multi_ticker_limit_order_book = MultiTickerLimitOrderBook()

    def order_insert(self, order: Order) -> list[Trade]:
        trades = self._multi_ticker_limit_order_book.trade(order)

        if order.to_volume().is_not_zero():
            self._multi_ticker_limit_order_book.insert(order)

        number_of_orders = self.number_of_orders()
        print(f'number of orders: {number_of_orders}')

        return trades

    def order_modify(self, order: Order) -> list[Trade]:
        modified_order = self._multi_ticker_limit_order_book.update(order)

        number_of_orders = self.number_of_orders()
        print(f'number of orders: {number_of_orders}')

        if modified_order is not None:
            trades = self._multi_ticker_limit_order_book.trade(modified_order)

            if modified_order.to_volume().is_not_zero():
                self._multi_ticker_limit_order_book.insert(modified_order)

            return trades
        else:
            return []

    def order_cancel(self, order_id: OrderId) -> Order|None:
        order = self._multi_ticker_limit_order_book.cancel(order_id)

        number_of_orders = self.number_of_orders()
        print(f'number of orders: {number_of_orders}')

        #if order is None:
        #    raise RuntimeError(f'LimitOrderBook.cancel failed to cancel order with order id {order_id}')

        return order

    def top_of_book(self, ticker: Ticker) -> TopOfBook:
        number_of_orders = self.number_of_orders()
        print(f'number of orders: {number_of_orders}')

        top_of_book = self._multi_ticker_limit_order_book.top_of_book(ticker)
        return top_of_book

    def number_of_orders(self) -> int:
        number_of_orders = self._multi_ticker_limit_order_book.number_of_orders()
        print(f'number of orders: {number_of_orders}')
        return number_of_orders

