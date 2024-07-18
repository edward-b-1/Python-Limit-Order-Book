
from lib_financial_exchange.financial_exchange_types.order import Order
from lib_financial_exchange.financial_exchange_types.trade import Trade
from lib_financial_exchange.financial_exchange_types.top_of_book import TopOfBook

from lib_datetime import datetime_to_string
from lib_datetime import string_to_datetime

from pydantic import BaseModel

from datetime import datetime

from abc import ABC

# TODO: remove ip!


class AbstractMessage(ABC, BaseModel):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def serialize(self) -> str:
        pass

    @classmethod
    def deserialize(cls, serialized_message: str):
        pass












