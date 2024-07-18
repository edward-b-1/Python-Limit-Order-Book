
from lib_financial_exchange.financial_exchange_types.order_id import OrderId
from lib_financial_exchange.financial_exchange_types.volume import Volume

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class OrderCancelPartialMessage(AbstractMessage):
    ip: str
    created_datetime: datetime
    order_id: OrderId
    volume: Volume

    def __str__(self) -> str:
        return f'OrderCancelPartialMessage({self.ip}, {self.created_datetime}, {self.order_id}, {self.volume})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        ip = self.ip
        created_datetime = datetime_to_string(self.created_datetime)
        order_id = str(self.order_id.to_int())
        volume = str(self.volume.to_int())
        return f'ORDER_CANCEL_PARTIAL {ip} {created_datetime} {order_id} {volume}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 5, f'number of components is {len(components)}, expected 5'
        ip = components[1]
        created_datetime = string_to_datetime(components[2])
        order_id_str = components[3]
        volume_str = components[4]
        order_cancel_partial_message = OrderCancelPartialMessage(
            ip=ip,
            created_datetime=created_datetime,
            order_id=OrderId(int(order_id_str)),
            volume=Volume(int(volume_str)),
        )
        return order_cancel_partial_message
