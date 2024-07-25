
from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class ResetMessage(AbstractMessage):

    def __init__(
        self,
        created_datetime: datetime,
    ) -> None:
        self._created_datetime = created_datetime

    def __str__(self) -> str:
        return f'ResetMessage({self._created_datetime})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        created_datetime = datetime_to_string(self._created_datetime)
        return f'RESET {created_datetime}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 2, f'number of components is {len(components)}, expected 2'
        created_datetime = string_to_datetime(components[1])
        reset_message = ResetMessage(
            created_datetime=created_datetime,
        )
        return reset_message

    def to_timestamp(self) -> datetime:
        return self._created_datetime

