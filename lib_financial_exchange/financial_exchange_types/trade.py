
from lib_financial_exchange.financial_exchange_types.ticker import Ticker
from lib_financial_exchange.financial_exchange_types.trade_id import TradeId
from lib_financial_exchange.financial_exchange_types.order_id import OrderId
from lib_financial_exchange.financial_exchange_types.int_price import IntPrice
from lib_financial_exchange.financial_exchange_types.volume import Volume
from lib_financial_exchange.financial_exchange_types.order_side import OrderSide

from datetime import datetime

from typeguard import typechecked


@typechecked
class Trade():

    def __init__(
        self,
        trade_id: TradeId,
        order_id_maker: OrderId,
        order_id_taker: OrderId,
        timestamp: datetime,
        ticker: Ticker,
        int_price: IntPrice,
        volume: Volume,
    ) -> None:
        self._trade_id = trade_id
        self._order_id_maker = order_id_maker
        self._order_id_taker = order_id_taker
        self._timestamp = timestamp
        self._ticker = ticker
        self._int_price = int_price
        self._volume = volume

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Trade): return False
        if self._trade_id != value._trade_id: return False
        if self._order_id_maker != value._order_id_maker: return False
        if self._order_id_taker != value._order_id_taker: return False
        if self._ticker != value._ticker: return False
        if self._int_price != value._int_price: return False
        if self._volume != value._volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'Trade('
            f'trade_id={self._trade_id}, '
            f'order_id_maker={self._order_id_maker}, '
            f'order_id_taker={self._order_id_taker}, '
            f'timestamp={self._timestamp} '
            f'ticker={self._ticker}, '
            f'price={self._int_price}, '
            f'volume={self._volume}'
            f')'
        )

    def __repr__(self) -> str:
        return str(self)

    def to_trade_id(self) -> TradeId:
        return self._trade_id

    def order_id_maker(self) -> OrderId:
        return self._order_id_maker

    def order_id_taker(self) -> OrderId:
        return self._order_id_taker

    def to_timestamp(self) -> datetime:
        return self._timestamp

    def to_ticker(self) -> Ticker:
        return self._ticker

    def to_int_price(self) -> IntPrice:
        return self._int_price

    def to_volume(self) -> Volume:
        return self._volume
