
from lib_financial_exchange.financial_exchange_types.int_price import IntPrice
from lib_financial_exchange.financial_exchange_types.volume import Volume
from lib_financial_exchange.financial_exchange_types.order_side import OrderSide
from lib_financial_exchange.financial_exchange_types.ticker import Ticker

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


# TODO: the order message types are really distinct types, and do not have a common interface
# so why use inheritance
class OrderInsertMessage(AbstractMessage):

    def __init__(
        self,
        created_datetime: datetime,
        ticker: Ticker,
        order_side: OrderSide,
        int_price: IntPrice,
        volume: Volume,
    ) -> None:
        self._created_datetime = created_datetime
        self._ticker = ticker
        self._order_side = order_side
        self._int_price = int_price
        self._volume = volume


    # TODO: not finished working here, check if `=` works without a definition of __eq__
    # TODO: check if required - now using pydantic
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, OrderInsertMessage):
            return False
        if self._ticker != value._ticker: return False
        if self._order_side != value._order_side: return False
        if self._int_price != value._int_price: return False
        if self._volume != value._volume: return False
        return True

    def __str__(self) -> str:
        fields = [
            self._created_datetime,
            self._ticker,
            self._order_side,
            self._int_price,
            self._volume,
        ]
        fields_str = ', '.join(map(str, fields))
        return f'OrderInsertMessage({fields_str})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        created_datetime = datetime_to_string(self._created_datetime) # TODO
        ticker = self._ticker.to_str()
        order_side = str(self._order_side)
        int_price = str(self._int_price.to_int())
        volume = str(self._volume.to_int())
        return f'ORDER_INSERT {created_datetime} {ticker} {order_side} {int_price} {volume}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 6, f'number of components is {len(components)}, expected 6'
        created_datetime = string_to_datetime(components[1])
        ticker_str = components[2]
        order_side_str = components[3]
        int_price_str = components[4]
        volume_str = components[5]
        order_insert_message = OrderInsertMessage(
            created_datetime=created_datetime,
            ticker=Ticker(ticker_str),
            order_side=OrderSide(order_side_str),
            int_price=IntPrice(int(int_price_str)),
            volume=Volume(int(volume_str)),
        )
        return order_insert_message

    def to_timestamp(self) -> datetime:
        return self._created_datetime

    def to_ticker(self) -> Ticker:
        return self._ticker

    def to_order_side(self) -> OrderSide:
        return self._order_side

    def to_int_price(self) -> IntPrice:
        return self._int_price

    def to_volume(self) -> Volume:
        return self._volume