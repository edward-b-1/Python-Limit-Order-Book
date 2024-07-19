
from lib_financial_exchange.financial_exchange_types.int_price import IntPrice
from lib_financial_exchange.financial_exchange_types.order_id import OrderId
from lib_financial_exchange.financial_exchange_types.volume import Volume

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class OrderUpdateMessage(AbstractMessage):

    def __init__(
        self,
        created_datetime: datetime,
        order_id: OrderId,
        int_price: IntPrice,
        volume: Volume,
    ) -> None:
        self._created_datetime = created_datetime
        self._order_id = order_id
        self._int_price = int_price
        self._volume = volume

    # TODO: check that not defining __init__ is a runtime error [no longer required]
    # TODO: check that not defining __str__ is a runtime error

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, OrderUpdateMessage):
            return False
        if self._created_datetime != value._created_datetime: return False
        if self._order_id != value._order_id: return False
        if self._int_price != value._int_price: return False
        if self._volume != value._volume: return False
        return True

    def __str__(self) -> str:
        return f'OrderUpdateMessage({self._created_datetime}, {self._order_id}, {self._int_price}, {self._volume})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        created_datetime = datetime_to_string(self._created_datetime)
        order_id = str(self._order_id.to_int())
        int_price = str(self._int_price.to_int())
        volume = str(self._volume.to_int())
        return f'ORDER_UPDATE {created_datetime} {order_id} {int_price} {volume}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 5, f'number of components is {len(components)}, expected 5'
        created_datetime = string_to_datetime(components[1])
        order_id_str = components[2]
        int_price_str = components[3]
        volume_str = components[4]
        order_update_message = OrderUpdateMessage(
            created_datetime=created_datetime,
            order_id=OrderId(int(order_id_str)),
            int_price=IntPrice(int(int_price_str)),
            volume=Volume(int(volume_str)),
        )
        return order_update_message

    def to_timestamp(self) -> datetime:
        return self._created_datetime

    def to_order_id(self) -> OrderId:
        return self._order_id

    def to_int_price(self) -> IntPrice:
        return self._int_price

    def to_volume(self) -> Volume:
        return self._volume

