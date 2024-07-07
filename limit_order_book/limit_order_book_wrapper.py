

from limit_order_book.types.order_id import OrderId
from limit_order_book.order_side import OrderSide
from limit_order_book.order import Order
from limit_order_book.order_without_order_id import OrderWithoutOrderId
from limit_order_book.trade import Trade
from limit_order_book.ticker import Ticker
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.top_of_book import TopOfBook
from limit_order_book.multi_ticker_limit_order_book import MultiTickerLimitOrderBook

from typeguard import typechecked

'''
TODO: Maybe DO NOT support the Databento style interface. Just support the API
style interface. Perhaps Databento data feed contains too much data, and some
of this data can be removed when feeding data to the LimitOrderBook.

Need to perform processing on the Databento data first to create a list of
messages which can be used to test the order book.
'''


@typechecked
class LimitOrderBook():

    def __init__(self) -> None:
        self._next_order_id_value = 1
        self._multi_ticker_limit_order_book = MultiTickerLimitOrderBook()


    def order_insert(self, order: OrderWithoutOrderId) -> tuple[OrderId, list[Trade]]:
        order_id = OrderId(self._next_order_id_value)
        self._next_order_id_value += 1
        order_with_order_id = Order(
            order_id=order_id,
            ticker=order.to_ticker(),
            order_side=order.to_order_side(),
            int_price=order.to_int_price(),
            volume=order.to_volume(),
        )
        trades = self._multi_ticker_limit_order_book.trade(order_with_order_id)

        if order_with_order_id.to_volume().is_not_zero():
            #print(f'order_with_order_id.to_volume()={order_with_order_id.to_volume()}')
            self._multi_ticker_limit_order_book.insert(order_with_order_id)

        # print(f'top of book:')
        # print(self.top_of_book(ticker=Ticker('NVDA')))

        return (order_id, trades)


    def order_update(self, order_id: OrderId, int_price: IntPrice|None, volume: Volume|None) -> list[Trade]:
        modified_order = None
        if int_price is None:
            assert volume is not None
            self._multi_ticker_limit_order_book.update_volume(order_id, volume)
        elif volume is None:
            assert int_price is not None
            modified_order = self._multi_ticker_limit_order_book.update_int_price(order_id, int_price)
        else:
            # int_price and volume both not None
            modified_order = self._multi_ticker_limit_order_book.update(order_id, int_price, volume)

        if modified_order is not None:
            trades = self._multi_ticker_limit_order_book.trade(modified_order)
            if modified_order.to_volume().is_not_zero():
                self._multi_ticker_limit_order_book.insert(modified_order)
            return trades
        return []


    # def order_modify_databento(self, order: Order) -> list[Trade]:
    #     modified_order = self._multi_ticker_limit_order_book.modify_databento(order)

    #     if modified_order is not None:
    #         trades = self._multi_ticker_limit_order_book.trade(modified_order)

    #         if modified_order.to_volume().is_not_zero():
    #             self._multi_ticker_limit_order_book.insert(modified_order)

    #         return trades
    #     else:
    #         return []


    # def order_cancel_databento(self, order: Order) -> None:
    #     self._multi_ticker_limit_order_book.cancel_databento(order)

    def order_cancel(self, order_id: OrderId) -> Order|None:
        order = self._multi_ticker_limit_order_book.cancel(order_id)

        #if order is None:
        #    raise RuntimeError(f'LimitOrderBook.cancel failed to cancel order with order id {order_id}')

        return order


    def order_cancel_partial(self, order_id: OrderId, volume: Volume) -> None:
        self._multi_ticker_limit_order_book.cancel_partial(order_id, volume)


    # TODO: not sure about the return value for this
    # TODO: this function is not implemented using the same semantics as order_cancel
    # Change it to follow the same logic
    # TODO: moving this to `order_cancel_databento`
    # def order_cancel_partial(self, order_id: OrderId, volume: Volume) -> Order|None:
    #     order = self._multi_ticker_limit_order_book.cancel_partial(order_id, volume)
    #     return order

    #     # TODO: remove
    #     existing_order = self._multi_ticker_limit_order_book._query_by_order_id(order_id)
    #     if existing_order is None:
    #         raise RuntimeError(f'this is temporary and will be removed when this function is implemented differently')
    #     existing_order_volume = existing_order.to_volume()
    #     if volume == existing_order_volume:

    #     elif volume < existing_order_volume:

    #     else:
    #         raise RuntimeError(f'cannot partially cancel more than existing order quantity')

    def top_of_book(self, ticker: Ticker) -> TopOfBook:
        top_of_book = self._multi_ticker_limit_order_book.top_of_book(ticker)
        return top_of_book

    def number_of_orders(self) -> int:
        number_of_orders = self._multi_ticker_limit_order_book.number_of_orders()
        return number_of_orders

