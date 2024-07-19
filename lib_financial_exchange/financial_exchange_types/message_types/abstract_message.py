
from abc import ABC

# TODO: remove ip!


class AbstractMessage(ABC):
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












