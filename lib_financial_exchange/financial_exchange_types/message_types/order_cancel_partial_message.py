
from lib_financial_exchange.financial_exchange_types.order_id import OrderId
from lib_financial_exchange.financial_exchange_types.volume import Volume

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class OrderCancelPartialMessage(AbstractMessage):
    def __init__(
        self,
        created_datetime: datetime,
        order_id: OrderId,
        volume: Volume,
    ) -> None:
        self._created_datetime = created_datetime
        self._order_id = order_id
        self._volume = volume

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, OrderCancelPartialMessage):
            return False
        if self._created_datetime != value._created_datetime: return False
        if self._order_id != value._order_id: return False
        if self._volume != value._volume: return False
        return True

    def __str__(self) -> str:
        return f'OrderCancelPartialMessage({self._created_datetime}, {self._order_id}, {self._volume})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        created_datetime = datetime_to_string(self._created_datetime)
        order_id = str(self._order_id.to_int())
        volume = str(self._volume.to_int())
        return f'ORDER_CANCEL_PARTIAL {created_datetime} {order_id} {volume}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 4, f'number of components is {len(components)}, expected 4'
        created_datetime = string_to_datetime(components[1])
        order_id_str = components[2]
        volume_str = components[3]
        order_cancel_partial_message = OrderCancelPartialMessage(
            created_datetime=created_datetime,
            order_id=OrderId(int(order_id_str)),
            volume=Volume(int(volume_str)),
        )
        return order_cancel_partial_message

    def to_timestamp(self) -> datetime:
        return self._created_datetime

    def to_order_id(self) -> OrderId:
        return self._order_id

    def to_volume(self) -> Volume:
        return self._volume
