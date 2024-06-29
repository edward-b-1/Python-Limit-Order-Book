
from new_limit_order_book.ticker import Ticker
from new_limit_order_book.types.order_id import OrderId
from new_limit_order_book.types.int_price import IntPrice
from new_limit_order_book.types.volume import Volume
from new_limit_order_book.order_side import OrderSide

from typeguard import typechecked


@typechecked
class Trade():

    def __init__(
        self,
        order_id_maker: OrderId,
        order_id_taker: OrderId,
        ticker: Ticker,
        int_price: IntPrice,
        volume: Volume,
    ) -> None:
        self._order_id_maker = order_id_maker
        self._order_id_taker = order_id_taker
        self._ticker = ticker
        self._int_price = int_price
        self._volume = volume

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Trade): return False
        if self._order_id_maker != value._order_id_maker: return False
        if self._order_id_taker != value._order_id_taker: return False
        if self._ticker != value._ticker: return False
        if self._int_price != value._int_price: return False
        if self._volume != value._volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'Trade('
            f'order_id_maker={self._order_id_maker}, '
            f'order_id_taker={self._order_id_taker}, '
            f'ticker={self._ticker}, '
            f'price={self._int_price}, '
            f'volume={self._volume}'
            f')'
        )

    def __repr__(self) -> str:
        return str(self)

