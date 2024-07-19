
from lib_financial_exchange.financial_exchange_types.order_id import OrderId
from lib_financial_exchange.financial_exchange_types.ticker import Ticker
from lib_financial_exchange.financial_exchange_types.int_price import IntPrice
from lib_financial_exchange.financial_exchange_types.volume import Volume
from lib_financial_exchange.financial_exchange_types.order_side import OrderSide
from lib_financial_exchange.financial_exchange_types.trade import Trade

from datetime import datetime

from typeguard import typechecked


@typechecked
class Order():

    def __init__(
        self,
        order_id: OrderId,
        timestamp: datetime,
        ticker: Ticker,
        order_side: OrderSide,
        int_price: IntPrice,
        volume: Volume,
    ) -> None:
        self._order_id = order_id
        self._timestamp = timestamp
        self._ticker = ticker
        self._order_side = order_side
        self._int_price = int_price
        self._volume = volume

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Order): return False
        if self._order_id != value._order_id: return False
        if self._ticker != value._ticker: return False
        if self._order_side != value._order_side: return False
        if self._int_price != value._int_price: return False
        if self._volume != value._volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'Order('
            f'order_id={self._order_id}, '
            f'timestamp={self._timestamp} '
            f'ticker={self._ticker}, '
            f'order_side={self._order_side}, '
            f'price={self._int_price}, '
            f'volume={self._volume}'
            f')'
        )

    def __repr__(self) -> str:
        return str(self)

    def debug_str(self) -> str:
        return str(self)

    # def copy(self):
    #     return Order(
    #         order_id=self._order_id,
    #         ticker=self._ticker,
    #         order_side=self._order_side,
    #         int_price=self._int_price,
    #         volume=self._volume,
    #     )

    ############################################################################

    def set_volume(self, volume: Volume):
        self._volume = volume

    def reduce_volume(self, volume: Volume):
        '''Reduce order volume by `volume`

        Args:
            volume (Volume): Volume quantity to reduce by
        '''
        self._volume.reduce(volume)

    def set_int_price(self, int_price: IntPrice):
        self._int_price = int_price

    # def set_order_id(self, order_id: OrderId):
    #     if order_id is None: return self
    #     assert validate_order_id(order_id), VALIDATE_ORDER_ID_ERROR_STR
    #     self._order_id = order_id
    #     return self

    # def set_ticker(self, ticker: Ticker):
    #     if ticker is None: return self
    #     assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
    #     self._ticker = ticker
    #     return self

    # def set_order_side(self, order_side: OrderSide):
    #     if order_side is None: return self
    #     assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
    #     self._order_side = order_side
    #     return self

    # def set_int_price(self, int_price: IntPrice):
    #     if int_price is None: return self
    #     assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
    #     self._int_price = int_price
    #     return self

    # def set_volume(self, volume: Volume):
    #     if volume is None: return self
    #     assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR
    #     self._volume = volume
    #     return self

    ############################################################################

    # def with_order_id(self, order_id: int):
    #     return self.copy().set_order_id(order_id)

    # def with_ticker(self, ticker: str):
    #     assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
    #     return self.copy().set_ticker(ticker)

    # def with_order_side(self, order_side: str):
    #     assert validate_order_side(order_side), VALIDATE_ORDER_SIDE_ERROR_STR
    #     return self.copy().set_order_side(order_side)

    # def with_int_price(self, int_price: int):
    #     assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
    #     return self.copy().set_int_price(int_price)

    # def with_volume(self, volume: int):
    #     assert validate_volume(volume), VALIDATE_VOLUME_ERROR_STR
    #     return self.copy().set_volume(volume)

    ############################################################################

    # These methods are intended to be used when missing data should result
    # in an error. If the data is intended to be optional, then access the
    # member data directly.

    def to_order_id(self) -> OrderId:
        return self._order_id

    def to_ticker(self) -> Ticker:
        return self._ticker

    def to_order_side(self) -> OrderSide:
        return self._order_side

    def to_int_price(self) -> IntPrice:
            return self._int_price

    def to_volume(self) -> Volume:
        return self._volume

    ############################################################################

    def match(self, taker_order, timestamp: datetime) -> Trade|None:
        '''
            The Taker order must be self. The Maker order must be order.

            If price levels cross through, the Maker recieves the bonus/premium, meaning
            that the Taker price is used.

            The Maker order (`order`) is modified if a Trade occurs.
            The Taker order (self) is modified if a Trade occurs.

            Return:
                A Trade, if orders are compatiable, or None.
        '''
        maker_order = self

        if maker_order.to_ticker() != taker_order.to_ticker():
            return None

        if maker_order.to_order_side() == taker_order.to_order_side():
            return None

        if maker_order.to_order_side() == taker_order.to_order_side():
            return None

        if maker_order.to_order_side() == OrderSide.BUY and taker_order.to_order_side() == OrderSide.SELL:
            if maker_order.to_int_price() < taker_order.to_int_price():
                return None

        if maker_order.to_order_side() == OrderSide.SELL and taker_order.to_order_side() == OrderSide.BUY:
            if maker_order.to_int_price() > taker_order.to_int_price():
                return None

        match_int_price = taker_order.to_int_price()
        match_volume = min(maker_order.to_volume(), taker_order.to_volume())
        if match_volume == 0:
            return None

        maker_volume = maker_order.to_volume() - match_volume
        taker_volume = taker_order.to_volume() - match_volume

        # NOTE: it is the responsibility of the managing data structure to
        # filter orders which have zero remaining volume
        maker_order.set_volume(maker_volume)
        taker_order.set_volume(taker_volume)

        trade = Trade(
            order_id_maker=maker_order.to_order_id(),
            order_id_taker=taker_order.to_order_id(),
            timestamp=timestamp,
            ticker=self.to_ticker(),
            int_price=match_int_price,
            volume=match_volume,
        )

        return trade
