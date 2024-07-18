
from lib_financial_exchange.financial_exchange_types.int_price import IntPrice
from lib_financial_exchange.financial_exchange_types.order_id import OrderId
from lib_financial_exchange.financial_exchange_types.volume import Volume

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class OrderUpdateMessage(AbstractMessage):
    ip: str
    created_datetime: datetime
    order_id: OrderId
    int_price: IntPrice
    volume: Volume

    # TODO: check that not defining __init__ is a runtime error [no longer required]
    # TODO: check that not defining __str__ is a runtime error

    def __str__(self) -> str:
        return f'OrderUpdateMessage({self.ip}, {self.created_datetime}, {self.order_id}, {self.int_price}, {self.volume})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        ip = self.ip
        created_datetime = datetime_to_string(self.created_datetime)
        order_id = str(self.order_id.to_int())
        int_price = str(self.int_price.to_int())
        volume = str(self.volume.to_int())
        return f'ORDER_UPDATE {ip} {created_datetime} {order_id} {int_price} {volume}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 6, f'number of components is {len(components)}, expected 6'
        ip = components[1]
        created_datetime = string_to_datetime(components[2])
        order_id_str = components[3]
        int_price_str = components[4]
        volume_str = components[5]
        order_update_message = OrderUpdateMessage(
            ip=ip,
            created_datetime=created_datetime,
            order_id=OrderId(int(order_id_str)),
            int_price=IntPrice(int(int_price_str)),
            volume=Volume(int(volume_str)),
        )
        return order_update_message

