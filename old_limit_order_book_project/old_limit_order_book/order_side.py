
from enum import Enum

class OrderSide(Enum):
    BUY = 1
    SELL = 2

    def __str__(self) -> str:
        return str(self.name)
