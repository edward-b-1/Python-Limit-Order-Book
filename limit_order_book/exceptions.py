from limit_order_book.types.order_id import OrderId

class LimitOrderBookError(Exception):
    pass

class DuplicateOrderIdError(LimitOrderBookError):
    def __init__(self, order_id: OrderId) -> None:
        self.order_id = order_id

    def __str__(self) -> str:
        return f'duplicate order id {self.order_id}'

