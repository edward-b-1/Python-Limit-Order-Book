
from limit_order_book.ticker import Ticker
from limit_order_book.types.order_id import OrderId
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume

from typeguard import typechecked

@typechecked
class TopOfBook():

    def __init__(
        self,
        ticker: Ticker,
        int_price_buy: IntPrice|None,
        volume_buy: Volume|None,
        int_price_sell: IntPrice|None,
        volume_sell: Volume|None,
    ) -> None:
        self._ticker = ticker
        self._int_price_buy = int_price_buy
        self._volume_buy = volume_buy
        self._int_price_sell = int_price_sell
        self._volume_sell = volume_sell

    def __repr__(self) -> str:
        return f'TopOfBook(ticker={self._ticker}, price_buy={self._int_price_buy}, volume_buy={self._volume_buy}, price_sell={self._int_price_sell}, volume_sell={self._volume_sell})'

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TopOfBook):
            return False
        if self._ticker != value._ticker:
            return False
        if self._int_price_buy != value._int_price_buy:
            return False
        if self._volume_buy != value._volume_buy:
            return False
        if self._int_price_sell != value._int_price_sell:
            return False
        if self._volume_sell != value._volume_sell:
            return False

        return True

