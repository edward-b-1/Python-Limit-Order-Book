
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.validate import *
from old_limit_order_book.trade import Trade


class Order:

    def __init__(
        self,
        order_id: int,
        ticker: str,
        order_side: str,
        int_price: int,
        volume: int,
    ) -> None:
        assert validate_order_id(order_id), VALIDATE_ORDER_ID_ERROR_STR
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR
        self.order_id = order_id
        self.ticker = ticker
        self.order_side = order_side
        self.int_price = int_price
        self.volume = volume

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Order): return False
        if self.order_id != value.order_id: return False
        if self.ticker != value.ticker: return False
        if self.order_side != value.order_side: return False
        if self.int_price != value.int_price: return False
        if self.volume != value.volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'Order('
            f'{self.order_id}, '
            f'{self.ticker}, '
            f'{self.order_side}, '
            f'price={self.int_price}, '
            f'volume={self.volume}'
            f')'
        )

    def debug_str(self) -> str:
        return str(self)

    def copy(self):
        return Order(
            order_id=self.order_id,
            ticker=self.ticker,
            order_side=self.order_side,
            int_price=self.int_price,
            volume=self.volume,
        )

    ############################################################################

    def set_order_id(self, order_id: int):
        if order_id is None: return self
        assert validate_order_id(order_id), VALIDATE_ORDER_ID_ERROR_STR
        self.order_id = order_id
        return self

    def set_ticker(self, ticker: str):
        if ticker is None: return self
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        self.ticker = ticker
        return self

    def set_order_side(self, order_side: str):
        if order_side is None: return self
        assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        self.order_side = order_side
        return self

    def set_int_price(self, int_price: int):
        if int_price is None: return self
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        self.int_price = int_price
        return self

    def set_volume(self, volume: int):
        if volume is None: return self
        assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR
        self.volume = volume
        return self

    ############################################################################

    def with_order_id(self, order_id: int):
        return self.copy().set_order_id(order_id)

    def with_ticker(self, ticker: str):
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        return self.copy().set_ticker(ticker)

    def with_order_side(self, order_side: str):
        assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        return self.copy().set_order_side(order_side)

    def with_int_price(self, int_price: int):
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        return self.copy().set_int_price(int_price)

    def with_volume(self, volume: int):
        assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR
        return self.copy().set_volume(volume)

    ############################################################################

    # These methods are intended to be used when missing data should result
    # in an error. If the data is intended to be optional, then access the
    # member data directly.

    def to_order_id(self) -> int:
        assert validate_order_id(self.order_id), VALIDATE_ORDER_ID_ERROR_STR
        return self.order_id

    def to_ticker(self) -> str:
        assert validate_ticker(self.ticker), VALIDATE_TICKER_ERROR_STR
        return self.ticker

    def to_order_side(self) -> str:
        assert validate_order_side(self.order_side), VALIDATE_ORDER_SIDE_ERROR_STR
        return self.order_side

    def to_int_price(self) -> int:
        assert validate_int_price(self.int_price), VALIDATE_INT_PRICE_ERROR_STR
        return self.int_price

    def to_volume(self) -> int:
        assert validate_volume(self.volume), VALIDATE_VOLUME_ERROR_STR
        return self.volume

    ############################################################################

    def match(self, taker_order) -> Trade|None:
        '''
            The Maker order must be self. The Taker order must be order.

            If price levels cross through, the Maker recieves the bonus/premium, meaning
            that the Taker price is used.

            The Maker order (self) is modified if a Trade occurs.
            The Taker order (`order`) is modified if a Trade occurs.

            Return:
                A Trade, if orders are compatiable, or None.
        '''
        maker_order = self

        if maker_order.ticker != taker_order.ticker:
            return None

        if maker_order.order_side == taker_order.order_side:
            return None

        if maker_order.order_side == OrderSide.BUY and taker_order.order_side == OrderSide.SELL:
            if maker_order.int_price < taker_order.int_price:
                return None

        if maker_order.order_side == OrderSide.SELL and taker_order.order_side == OrderSide.BUY:
            if maker_order.int_price > taker_order.int_price:
                return None

        match_int_price = taker_order.int_price

        match_volume = min(maker_order.volume, taker_order.volume)
        if match_volume == 0:
            return None

        maker_volume = maker_order.volume - match_volume
        taker_volume = taker_order.volume - match_volume

        # NOTE: it is the responsibility of the managing data structure to
        # filter orders which have zero remaining volume
        maker_order.volume = maker_volume
        taker_order.volume = taker_volume

        trade = Trade(
            order_id_maker=maker_order.order_id,
            order_id_taker=taker_order.order_id,
            ticker=self.ticker,
            int_price=match_int_price,
            volume=match_volume,
        )

        return trade
