
from lib_financial_exchange.financial_exchange_types.ticker import Ticker

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from datetime import datetime


class TopOfBookMessage(AbstractMessage):
    def __init__(
        self,
        created_datetime: datetime,
        ticker: Ticker,
    ) -> None:
        self._created_datetime = created_datetime
        self._ticker = ticker

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TopOfBookMessage):
            return False
        if self._created_datetime != value._created_datetime: return False
        if self._ticker != value._ticker: return False
        return True

    def __str__(self) -> str:
        return f'TopOfBookMessage({self._created_datetime}, {self._ticker})'

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        created_datetime = datetime_to_string(self._created_datetime)
        ticker = str(self._ticker.to_str())
        return f'TOP_OF_BOOK {created_datetime} {ticker}'

    @classmethod
    def deserialize(cls, serialized_message: str):
        components = serialized_message.split(' ')

        assert len(components) == 3, f'number of components is {len(components)}, expected 3'
        created_datetime = string_to_datetime(components[1])
        ticker_str = components[2]
        top_of_book_message = TopOfBookMessage(
            created_datetime=created_datetime,
            ticker=Ticker(ticker_str),
        )
        return top_of_book_message

    def to_timestamp(self) -> datetime:
        return self._created_datetime

    def to_ticker(self) -> Ticker:
        return self._ticker
