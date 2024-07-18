
from lib_financial_exchange.financial_exchange_types.order_id import OrderId

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class OrderCancelMessage(AbstractMessage):
    ip: str
    created_datetime: datetime
    order_id: OrderId

    def __str__(self) -> str:
        return f'OrderCancelMessage({self.ip}, {self.created_datetime}, {self.order_id})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        ip = self.ip
        created_datetime = datetime_to_string(self.created_datetime)
        order_id = str(self.order_id.to_int())
        f'ORDER_CANCEL {ip} {created_datetime} {order_id}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 4, f'number of components is {len(components)}, expected 4'
        ip = components[1]
        created_datetime = string_to_datetime(components[2])
        order_id_str = components[3]
        order_cancel_message = OrderCancelMessage(
            ip=ip,
            created_datetime=created_datetime,
            order_id=OrderId(int(order_id_str)),
        )
        return order_cancel_message

