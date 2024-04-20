
from limit_order_book.limit_order_book import LimitOrderBook
from limit_order_book.trade import Trade


class DoubleLimitOrderBook:

    def __init__(self):
        # SIDE -> TICKER -> PRICE_LEVEL -> list of volumes
        self.double_limit_order_book = {
            'BUY': LimitOrderBook(order_side='BUY'),
            'SELL': LimitOrderBook(order_side='SELL'),
        }

    def _find_order_side_by_order_id(self, order_id: int) -> str:
        limit_order_book_buy = self.double_limit_order_book['BUY']
        limit_order_book_sell = self.double_limit_order_book['SELL']

        # TODO: consider using count here instead
        order_exists_in_buy_side = limit_order_book_buy.order_id_exists(order_id)
        order_exists_in_sell_side = limit_order_book_sell.order_id_exists(order_id)

        if order_exists_in_buy_side and not order_exists_in_sell_side:
            return 'BUY'
        elif not order_exists_in_buy_side and order_exists_in_sell_side:
            return 'SELL'

    def _find_limit_order_book_buy_order_side(self, order_side: str) -> LimitOrderBook:
        # if order_side == 'BUY':
        #     return True
        # elif order_side == 'SELL':
        #     return True
        # else:
        #     return False

        limit_order_book = None

        if order_side == 'BUY':
            limit_order_book = self.double_limit_order_book['BUY']
        elif order_side == 'SELL':
            limit_order_book = self.double_limit_order_book['SELL']

        if limit_order_book is None:
            raise RuntimeError(f'invalid order_side {order_side}')

        return limit_order_book

    def depth(self, order_side: str) -> int:
        return self.double_limit_order_book[order_side].depth()

    def depth_aggregated(self) -> int:
        return (
            sum(
                map(
                    lambda limit_order_book: limit_order_book.depth_aggregated(),
                    self.double_limit_order_book.values(),
                )
            )
        )

    def _order_side_opposite(order_side: str) -> str:
        if order_side == 'BUY':
            return 'SELL'
        elif order_side == 'SELL':
            return 'BUY'
        raise ValueError(f'invalid order_side {order_side}')

    def order_id_exists(self, order_id: int):
        return (
            any(
                filter(
                    lambda limit_order_book: limit_order_book.order_id_exists(order_id),
                    self.double_limit_order_book.values(),
                )
            )
        )

    def order_insert(self, order_id: int, ticker: str, order_side: str, int_price: int, volume: int) -> list[Trade]|None:
        print(f'DoubleLimitOrderBook.order_insert: order_id={order_id}, ticker={ticker}, order_side={order_side}, int_price={int_price}, volume={volume}')

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        # on new order arrival, test if there are any matches in the opposite side book
        order_side_opposite = DoubleLimitOrderBook._order_side_opposite(order_side)
        limit_order_book_opposite = self._find_limit_order_book_buy_order_side(order_side_opposite)
        # there are multiple price levels in limit_order_book_opposite
        # search ??? TODO

        trades = limit_order_book_opposite.order_insert(order_id, ticker, order_side, int_price, volume)

        # if order_side == 'BUY':
        #     # search price levels from the lowest sell to int_price (asc)
        #     # if lowest sell > int_price do nothing
        #     trades = limit_order_book_opposite.order_insert(order_id, ticker, order_side, int_price, volume)

        # elif order_side == 'SELL':
        #     trades = limit_order_book_opposite.order_insert(order_id, ticker, order_side, int_price, volume)
        #     # search price levels from the highest buy to int_price (desc)
        #     # if highest buy < int_price do nothign

        # limit_order_book = None

        # if order_side == 'BUY':
        #     limit_order_book = self.double_limit_order_book['BUY']
        # elif order_side == 'SELL':
        #     limit_order_book = self.double_limit_order_book['SELL']

        # if limit_order_book is None:
        #     raise RuntimeError(f'invalid order_side {order_side}')

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)   # TODO: use this kind of semantics in other structures

        # TODO: create PartialOrder here and set order side?
        no_trades = limit_order_book.order_insert(
            order_id=order_id,
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume,
        )
        assert no_trades is None, f'unexpected trade generated'

        print(f'DoubleLimitOrderBook returning trades {trades}')
        return trades

    def order_update(self, order_id: int, int_price: int, volume: int):
        print(f'DoubleLimitOrderBook.order_update: order_id={order_id}, int_price={int_price}, volume={volume}')
        order_side = self._find_order_side_by_order_id(order_id)

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)

        # TODO: bug here - need to check to see if price is being changed
        # if the price is changed, cancel the order from here and then
        # insert from here to trigger matching algorithm
        limit_order_book.order_update(order_id, int_price, volume)

        # if order_side == 'BUY':
        #     limit_order_book_buy = self.double_limit_order_book['BUY']
        #     limit_order_book_buy.order_update(order_id, int_price, volume)
        # elif order_side == 'SELL':
        #     limit_order_book_sell = self.double_limit_order_book['SELL']
        #     limit_order_book_sell.order_update(order_id, int_price, volume)
        # else:
        #     raise RuntimeError(f'cannot update order which exists in both buy and sell side book with order_id {order_id}')

    def order_cancel(self, order_id: int):
        print(f'DoubleLimitOrderBook.order_cancel: order_id={order_id}')
        order_side = self._find_order_side_by_order_id(order_id)

        # TODO: _find_limit_order_book_by_order_id
        limit_order_book = self._find_limit_order_book_buy_order_side(order_side)
        limit_order_book.order_cancel(order_id)

        # if order_side == 'BUY':
        #     limit_order_book_buy = self.double_limit_order_book['BUY']
        #     limit_order_book_buy.order_cancel(order_id)
        # elif order_side == 'SELL':
        #     limit_order_book_sell = self.double_limit_order_book['SELL']
        #     limit_order_book_sell.order_cancel(order_id)
        # else:
        #     raise RuntimeError(f'cannot cancel order which exists in both buy and sell side book with order_id {order_id}')