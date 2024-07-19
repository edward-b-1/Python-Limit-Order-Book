
from lib_financial_exchange.financial_exchange_types.order_id import OrderId

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class OrderCancelMessage(AbstractMessage):
    def __init__(
        self,
        created_datetime: datetime,
        order_id: OrderId,
    ) -> None:
        self._created_datetime = created_datetime
        self._order_id = order_id

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, OrderCancelMessage):
            return False
        if self._created_datetime != value._created_datetime: return False
        if self._order_id != value._order_id: return False
        return True

    def __str__(self) -> str:
        return f'OrderCancelMessage({self._created_datetime}, {self._order_id})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        created_datetime = datetime_to_string(self._created_datetime)
        order_id = str(self._order_id.to_int())
        return f'ORDER_CANCEL {created_datetime} {order_id}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 3, f'number of components is {len(components)}, expected 3'
        created_datetime = string_to_datetime(components[1])
        order_id_str = components[2]
        order_cancel_message = OrderCancelMessage(
            created_datetime=created_datetime,
            order_id=OrderId(int(order_id_str)),
        )
        return order_cancel_message

    def to_timestamp(self) -> datetime:
        return self._created_datetime

    def to_order_id(self) -> OrderId:
        return self._order_id
