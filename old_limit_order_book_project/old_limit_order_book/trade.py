
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.validate import *


class Trade:

    def __init__(self, order_id_maker: int, order_id_taker: int, ticker: str, int_price: int, volume: int):
        assert validate_order_id(order_id_maker), VALIDATE_ORDER_ID_ERROR_STR
        assert validate_order_id(order_id_taker), VALIDATE_ORDER_ID_ERROR_STR
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
        assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
        assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR

        self.order_id_maker = order_id_maker
        self.order_id_taker = order_id_taker
        self.ticker = ticker
        self.int_price = int_price
        self.volume = volume

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Trade): return False
        if self.order_id_maker != value.order_id_maker: return False
        if self.order_id_taker != value.order_id_taker: return False
        if self.ticker != value.ticker: return False
        if self.int_price != value.int_price: return False
        if self.volume != value.volume: return False
        return True

    def __str__(self) -> str:
        return (
            f'Trade('
            f'order_id_maker={self.order_id_maker}, '
            f'order_id_taker={self.order_id_taker}, '
            f'{self.ticker}, '
            f'price={self.int_price}, '
            f'volume={self.volume}'
            f')'
        )

    def __repr__(self) -> str:
        return str(self)

