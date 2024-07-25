

from lib_financial_exchange.financial_exchange_types.message_types import AbstractMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderUpdateMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelPartialMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelMessage

from lib_financial_exchange.financial_exchange_types.message_types import TopOfBookMessage

from lib_financial_exchange.financial_exchange_types.message_types import ResetMessage
from lib_financial_exchange.financial_exchange_types.message_types import SessionStartMessage
from lib_financial_exchange.financial_exchange_types.message_types import SessionEndMessage

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
            return self._create_order_insert_message(serialized_message=serialized_message)

        elif instruction == 'ORDER_UPDATE':
            return self._create_order_update_message(serialized_message=serialized_message)

        elif instruction == 'ORDER_CANCEL':
            return self._create_order_cancel_message(serialized_message=serialized_message)

        elif instruction == 'ORDER_CANCEL_PARTIAL':
            return self._create_order_cancel_partial_message(serialized_message=serialized_message)

        elif instruction == 'TOP_OF_BOOK':
            return self._create_top_of_book_message(serialized_message=serialized_message)

        elif instruction == 'SESSION_START':
            return self._create_session_start_message(serialized_message=serialized_message)

        elif instruction == 'SESSION_END':
            return self._create_session_end_message(serialized_message=serialized_message)

        elif instruction == 'RESET':
            return self._create_reset_message(serialized_message=serialized_message)

        else:
            raise RuntimeError(f'instruction {instruction} not recognized')


    def _create_order_insert_message(self, serialized_message: str) -> OrderInsertMessage:
        return OrderInsertMessage.deserialize(serialized_message)

    def _create_order_update_message(self, serialized_message: str) -> OrderUpdateMessage:
        return OrderUpdateMessage.deserialize(serialized_message)

    def _create_order_cancel_partial_message(self, serialized_message: str) -> OrderCancelPartialMessage:
        return OrderCancelPartialMessage.deserialize(serialized_message)

    def _create_order_cancel_message(self, serialized_message: str) -> OrderCancelMessage:
        return OrderCancelMessage.deserialize(serialized_message)

    def _create_top_of_book_message(self, serialized_message: str) -> TopOfBookMessage:
        return TopOfBookMessage.deserialize(serialized_message)

    def _create_session_start_message(self, serialized_message: str) -> SessionStartMessage:
        return SessionStartMessage.deserialize(serialized_message)

    def _create_session_end_message(self, serialized_message: str) -> SessionEndMessage:
        return SessionEndMessage.deserialize(serialized_message)

    def _create_reset_message(self, serialized_message: str) -> ResetMessage:
        return ResetMessage.deserialize(serialized_message)

