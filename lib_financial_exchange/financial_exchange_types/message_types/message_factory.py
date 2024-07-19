

from lib_financial_exchange.financial_exchange_types.message_types.abstract_message import AbstractMessage
from lib_financial_exchange.financial_exchange_types.message_types.order_insert_message import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types.message_types.order_update_message import OrderUpdateMessage
from lib_financial_exchange.financial_exchange_types.message_types.order_cancel_partial_message import OrderCancelPartialMessage
from lib_financial_exchange.financial_exchange_types.message_types.order_cancel_message import OrderCancelMessage
from lib_financial_exchange.financial_exchange_types.message_types.reset_message import ResetMessage
from lib_financial_exchange.financial_exchange_types.message_types.session_start_message import SessionStartMessage
from lib_financial_exchange.financial_exchange_types.message_types.session_end_message import SessionEndMessage

from typeguard import typechecked


@typechecked
class MessageFactory():

    def __init__(self) -> None:
        pass

    def create(self, serialized_message: str) -> AbstractMessage:

        components = serialized_message.split(' ', maxsplit=1)
        assert len(components) > 0
        instruction = components[0]

        if instruction == 'ORDER_INSERT':
            return self.create_order_insert_message(serialized_message=serialized_message)

        elif instruction == 'ORDER_UPDATE':
            return self.create_order_update_message(serialized_message=serialized_message)

        elif instruction == 'ORDER_CANCEL':
            return self.create_order_cancel_message(serialized_message=serialized_message)

        elif instruction == 'ORDER_CANCEL_PARTIAL':
            return self.create_order_cancel_partial_message(serialized_message=serialized_message)

        elif instruction == 'SESSION_START':
            return self.create_session_start_message(serialized_message=serialized_message)

        elif instruction == 'SESSION_END':
            return self.create_session_end_message(serialized_message=serialized_message)

        elif instruction == 'RESET':
            return self.create_reset_message(serialized_message=serialized_message)

        else:
            raise RuntimeError(f'instruction {instruction} not recognized')


    def create_order_insert_message(self, serialized_message: str) -> OrderInsertMessage:
        return OrderInsertMessage.deserialize(serialized_message)

    def create_order_update_message(self, serialized_message: str) -> OrderUpdateMessage:
        return OrderUpdateMessage.deserialize(serialized_message)

    def create_order_cancel_partial_message(self, serialized_message: str) -> OrderCancelPartialMessage:
        return OrderCancelPartialMessage.deserialize(serialized_message)

    def create_order_cancel_message(self, serialized_message: str) -> OrderCancelMessage:
        return OrderCancelMessage.deserialize(serialized_message)

    def create_session_start_message(self, serialized_message: str) -> SessionStartMessage:
        return SessionStartMessage.deserialize(serialized_message)

    def create_session_end_message(self, serialized_message: str) -> SessionEndMessage:
        return SessionEndMessage.deserialize(serialized_message)

    def create_reset_message(self, serialized_message: str) -> ResetMessage:
        return ResetMessage.deserialize(serialized_message)