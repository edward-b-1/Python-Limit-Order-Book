
from limit_order_book.types import OrderId
from limit_order_book.types import Ticker
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.types import OrderSide
from limit_order_book.trade import Trade

from typeguard import typechecked


@typechecked
class OrderWithoutOrderId:

    def __init__(
        self,
        ticker: Ticker,
        order_side: OrderSide,
        int_price: IntPrice,
        volume: Volume,
    ) -> None:
        self._ticker = ticker
        self._order_side = order_side
        self._int_price = int_price
        self._volume = volume

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, OrderWithoutOrderId): return False
        if self._ticker != value._ticker: return False
        if self._order_side != value._order_side: return False
        if self._int_price != value._int_price: return False
        if self._volume != value._volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'OrderWithoutOrderId('
            f'ticker={self._ticker}, '
            f'order_side={self._order_side}, '
            f'price={self._int_price}, '
            f'volume={self._volume}'
            f')'
        )

    def debug_str(self) -> str:
        return str(self)

    ############################################################################

    def set_volume(self, volume: Volume):
        self._volume = volume

    def set_int_price(self, int_price: IntPrice):
        self._int_price = int_price

    ############################################################################

    def to_ticker(self) -> Ticker:
        return self._ticker

    def to_order_side(self) -> OrderSide:
        return self._order_side

    def to_int_price(self) -> IntPrice:
            return self._int_price

    def to_volume(self) -> Volume:
        return self._volume
