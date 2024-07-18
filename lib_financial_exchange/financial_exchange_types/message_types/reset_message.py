
from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class ResetMessage(AbstractMessage):
    created_datetime: datetime

    def __str__(self) -> str:
        return f'ResetMessage({self.created_datetime})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        created_datetime = datetime_to_string(self.created_datetime)
        f'RESET {created_datetime}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')
        # TODO
