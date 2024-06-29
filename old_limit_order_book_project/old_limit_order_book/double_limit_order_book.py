
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.limit_order_book import LimitOrderBook
from old_limit_order_book.order import Order
from old_limit_order_book.trade import Trade


class DoubleLimitOrderBook:

    def __init__(self):
        # SIDE -> TICKER -> PRICE_LEVEL -> list of volumes
        self._double_limit_order_book = {
            OrderSide.BUY: LimitOrderBook(order_side=OrderSide.BUY),
            OrderSide.SELL: LimitOrderBook(order_side=OrderSide.SELL),
        }

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        buy_side_tickers = self._double_limit_order_book[OrderSide.BUY].tickers()
        sell_side_tickers = self._double_limit_order_book[OrderSide.SELL].tickers()

        tickers = buy_side_tickers
        for ticker in sell_side_tickers:
            if not ticker in tickers:
                tickers.append(ticker)

        tickers = sorted(tickers)

        def format_order_book_ticker_str(ticker: str, include_buy_side: bool, include_sell_side: bool) -> str:
            order_book_str = f'==={ticker}==='
            if include_sell_side:
                order_book_sell_side_str = self._double_limit_order_book[OrderSide.SELL].to_str(ticker)
                order_book_str += f'\n{order_book_sell_side_str}'
            if include_buy_side:
                order_book_buy_side_str = self._double_limit_order_book[OrderSide.BUY].to_str(ticker)
                order_book_str += f'\n{order_book_buy_side_str}'
            #order_book_str += f'\n{order_book_sell_side_str}\n{order_book_buy_side_str}'
            return order_book_str

        order_book_strs = []
        for ticker in tickers:
            total_volume_sell_side = self._double_limit_order_book[OrderSide.SELL].volume(ticker)
            total_volume_buy_side = self._double_limit_order_book[OrderSide.BUY].volume(ticker)
            if total_volume_sell_side == 0 and total_volume_buy_side == 0:
                continue
            order_book_strs.append(
                format_order_book_ticker_str(ticker, total_volume_buy_side > 0, total_volume_sell_side > 0)
            )
        order_book_str = '\n'.join(order_book_strs)
        return order_book_str

    def debug_str(self) -> str:
        buy_side = self._double_limit_order_book[OrderSide.BUY]
        sell_side = self._double_limit_order_book[OrderSide.SELL]

        return (
            f'{buy_side.debug_str()}\n'
            f'{sell_side.debug_str()}'
        )

    def _find_order_side_by_order_id(self, order_id: int) -> str:
        limit_order_book_buy = self._double_limit_order_book[OrderSide.BUY]
        limit_order_book_sell = self._double_limit_order_book[OrderSide.SELL]

        # TODO: consider using count here instead
        order_exists_in_buy_side = limit_order_book_buy.order_id_exists(order_id)
        order_exists_in_sell_side = limit_order_book_sell.order_id_exists(order_id)

        if order_exists_in_buy_side and not order_exists_in_sell_side:
            return OrderSide.BUY
        elif not order_exists_in_buy_side and order_exists_in_sell_side:
            return OrderSide.SELL
        else:
            raise RuntimeError(f'order id {order_id} not found')

    def _find_limit_order_book_buy_order_side(self, order_side: str) -> LimitOrderBook:
        limit_order_book = None

        if order_side == OrderSide.BUY:
            limit_order_book = self._double_limit_order_book[OrderSide.BUY]
        elif order_side == OrderSide.SELL:
            limit_order_book = self._double_limit_order_book[OrderSide.SELL]

        if limit_order_book is None:
            raise RuntimeError(f'invalid order_side {order_side}')

        return limit_order_book

    def depth(self, order_side: str) -> int:
        return self._double_limit_order_book[order_side].depth()

    def depth_aggregated(self) -> int:
        return (
            sum(
                map(
                    lambda limit_order_book: limit_order_book.depth_aggregated(),
                    self._double_limit_order_book.values(),
                )
            )
        )

    def _order_side_opposite(order_side: str) -> str:
        if order_side == OrderSide.BUY:
            return OrderSide.SELL
        elif order_side == OrderSide.SELL:
            return OrderSide.BUY
        raise ValueError(f'invalid order_side {order_side}')

    def order_id_exists(self, order_id: int):
        return (
            any(
                filter(
                    lambda limit_order_book: limit_order_book.order_id_exists(order_id),
                    self._double_limit_order_book.values(),
                )
            )
        )

    def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int) -> list[Trade]:

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        order = Order(
            order_id=order_id,
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume,
        )

        # on new order arrival, test if there are any matches in the opposite side book
        order_side_opposite = DoubleLimitOrderBook._order_side_opposite(order_side)
        limit_order_book_opposite = self._find_limit_order_book_buy_order_side(order_side_opposite)
        # there are multiple price levels in limit_order_book_opposite
        # search ??? TODO

        # TODO: bug: trading does not reduce volume
        trade_list = limit_order_book_opposite.order_insert(order)
        if order.volume == 0:
            return trade_list

        # if order_side == OrderSide.BUY:
        #     # search price levels from the lowest sell to int_price (asc)
        #     # if lowest sell > int_price do nothing
        #     trades = limit_order_book_opposite.order_insert(order_id, ticker, order_side, int_price, volume)

        # elif order_side == OrderSide.SELL:
        #     trades = limit_order_book_opposite.order_insert(order_id, ticker, order_side, int_price, volume)
        #     # search price levels from the highest buy to int_price (desc)
        #     # if highest buy < int_price do nothign

        # limit_order_book = None

        # if order_side == OrderSide.BUY:
        #     limit_order_book = self.double_limit_order_book[OrderSide.BUY]
        # elif order_side == OrderSide.SELL:
        #     limit_order_book = self.double_limit_order_book[OrderSide.SELL]

        # if limit_order_book is None:
        #     raise RuntimeError(f'invalid order_side {order_side}')

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)   # TODO: use this kind of semantics in other structures

        # TODO: create Order here and set order side?
        no_trades = limit_order_book.order_insert(order)
        assert len(no_trades) == 0, f'unexpected trade generated'

        return trade_list

    def order_update(self, order_id: int, int_price: int, volume: int) -> list[Trade]:
        order_side = self._find_order_side_by_order_id(order_id)

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)

        # TODO: bug here - need to check to see if price is being changed
        # if the price is changed, cancel the order from here and then
        # insert from here to trigger matching algorithm
        order = limit_order_book.order_update(order_id, int_price, volume)

        if order is not None:
            order_side_opposite = DoubleLimitOrderBook._order_side_opposite(order_side)
            limit_order_book_opposite = self._find_limit_order_book_buy_order_side(order_side_opposite)
            trade_list = limit_order_book_opposite.order_insert(order)
            if order.volume > 0:
                no_trade = limit_order_book.order_insert(order)
                assert len(no_trade) == 0, f'unexpected trade'
            return trade_list
        return []

        # if order_side == OrderSide.BUY:
        #     limit_order_book_buy = self.double_limit_order_book[OrderSide.BUY]
        #     limit_order_book_buy.order_update(order_id, int_price, volume)
        # elif order_side == OrderSide.SELL:
        #     limit_order_book_sell = self.double_limit_order_book[OrderSide.SELL]
        #     limit_order_book_sell.order_update(order_id, int_price, volume)
        # else:
        #     raise RuntimeError(f'cannot update order which exists in both buy and sell side book with order_id {order_id}')

    def order_cancel(self, order_id: int):
        order_side = self._find_order_side_by_order_id(order_id)

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)
        limit_order_book.order_cancel(order_id)

        # if order_side == OrderSide.BUY:
        #     limit_order_book_buy = self.double_limit_order_book[OrderSide.BUY]
        #     limit_order_book_buy.order_cancel(order_id)
        # elif order_side == OrderSide.SELL:
        #     limit_order_book_sell = self.double_limit_order_book[OrderSide.SELL]
        #     limit_order_book_sell.order_cancel(order_id)
        # else:
        #     raise RuntimeError(f'cannot cancel order which exists in both buy and sell side book with order_id {order_id}')
