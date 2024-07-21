

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import TopOfBook

from lib_financial_exchange.trade_id_generator import TradeIdGenerator

from lib_financial_exchange.data_structures.multi_ticker_limit_order_book import MultiTickerLimitOrderBook

from lib_financial_exchange.logging import log

from datetime import datetime

from typeguard import typechecked

'''
Need to perform processing on the Databento data first to create a list of
messages which can be used to test the order book.
'''


@typechecked
class LimitOrderBook():

    def __init__(self) -> None:
        self._next_order_id_value: int = 1
        self._trade_id_generator = TradeIdGenerator()
        self._multi_ticker_limit_order_book = MultiTickerLimitOrderBook()

    def order_insert(
        self,
        ticker: Ticker,
        order_side: OrderSide,
        int_price: IntPrice,
        volume: Volume,
        timestamp: datetime,
    ) -> tuple[OrderId, list[Trade]]:
        log.info(f'order insert: {ticker}, {order_side}, {int_price}, {volume}, {timestamp}')

        order_id = OrderId(self._next_order_id_value)
        self._next_order_id_value += 1

        order = Order(
            order_id=order_id,
            timestamp=timestamp,
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume,
        )

        trades = (
            self._multi_ticker_limit_order_book.trade(
                order,
                trade_id_generator=self._trade_id_generator,
                timestamp=timestamp,
            )
        )

        if len(trades) > 0:
            log.info(f'order insert: trades generated:')
            for trade in trades:
                log.info(f'{trade}')

        if order.to_volume().is_not_zero():
            self._multi_ticker_limit_order_book.insert(order)

        return (order_id, trades)


    def order_update(
        self,
        order_id: OrderId,
        int_price: IntPrice|None,
        volume: Volume|None,
        timestamp: datetime,
    ) -> list[Trade]:
        log.info(f'order update: {order_id}, {int_price}, {volume}, {timestamp}')

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
            trades = (
                self._multi_ticker_limit_order_book.trade(
                    modified_order,
                    trade_id_generator=self._trade_id_generator,
                    timestamp=timestamp,
                )
            )

            if len(trades) > 0:
                log.info(f'order update: trades generated:')
                for trade in trades:
                    log.info(f'{trade}')
            if modified_order.to_volume().is_not_zero():
                self._multi_ticker_limit_order_book.insert(modified_order)
            return trades
        return []


    def order_cancel(self, order_id: OrderId) -> Order|None:
        log.info(f'order cancel: {order_id}')

        order = self._multi_ticker_limit_order_book.cancel(order_id)

        #if order is None:
        #    raise RuntimeError(f'LimitOrderBook.cancel failed to cancel order with order id {order_id}')

        return order


    def order_cancel_partial(self, order_id: OrderId, volume: Volume) -> None:
        '''
        Note: There is currently no way to know if this succeeded or failed
        '''
        log.info(f'order cancel partial: {order_id}, {volume}')

        self._multi_ticker_limit_order_book.cancel_partial(order_id, volume)


    def top_of_book(self, ticker: Ticker) -> TopOfBook:
        top_of_book = self._multi_ticker_limit_order_book.top_of_book(ticker)
        return top_of_book

    def number_of_orders(self) -> int:
        number_of_orders = self._multi_ticker_limit_order_book.number_of_orders()
        return number_of_orders

    def list_all_tickers(self) -> list[Ticker]:
        ticker_list = self._multi_ticker_limit_order_book._list_all_tickers()
        return ticker_list

    def order_board(self) -> list[Order]:
        return self._multi_ticker_limit_order_book.order_board()

    def debug_current_order_id(self) -> OrderId:
        return OrderId(order_id=self._next_order_id_value)

    # TODO: some of these might be better done at a higher level of implementation
    def debug_log_current_order_id(self) -> None:
        log.info(f'next order id: {self._next_order_id_value}')

    def debug_log_top_of_book(self, ticker: Ticker) -> None:
        top_of_book = self._multi_ticker_limit_order_book.top_of_book(ticker)
        log.info(f'top of book: {ticker}')
        log.info(f'{top_of_book}')

    def debug_log_all_tickers(self) -> None:
        tickers = self._multi_ticker_limit_order_book._list_all_tickers_as_str()
        tickers_str = ' '.join(tickers)
        log.info(f'all tickers: {tickers_str}')