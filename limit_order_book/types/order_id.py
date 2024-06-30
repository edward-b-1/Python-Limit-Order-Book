
class OrderId():

    def __init__(self, order_id: int) -> None:
        assert order_id >= 0, f'OrderId.__init__ negative int price not valid'
        self._order_id = order_id

    def __str__(self) -> str:
        return f'OrderId({self._order_id})'

    def __eq__(self, value: object) -> bool:
        if isinstance(value, OrderId):
            return self._order_id == value._order_id
        return False

    def to_int(self) -> int:
        return self._order_id
