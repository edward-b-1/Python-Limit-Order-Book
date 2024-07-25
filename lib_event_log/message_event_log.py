
from lib_event_log.text_event_log import InputTextEventLog
from lib_event_log.text_event_log import OutputTextEventLog

from lib_financial_exchange.message_factory.message_factory import MessageFactory
from lib_financial_exchange.financial_exchange_types.message_types import AbstractMessage


'''
Ideas Board:

Can I split this into two types? One which handles input, and one which handles output? [Done]

Seems to be better to separate the input and output behaviours, similar to having
and input stream and an output stream. Code less complex, but now the class
cannot automatically re-process existing data when opened. (Could build a wrapper
class for this.)

Older:

Dependency injection: A last resort. Provide an ABC with a process_event() function,
reprocess_events/read_event_log_file/__init__ function takes an argument of this type.

Alternatively, don't use OOP for this. Put the reading file logic in main, and
then put the write file logic in main.

with InputType as input:
    pass

with OutputType as output:
    something.dependency_inject(output)

If I take a ContextManager approach then both the input and output versions of
an EventLog object need to be able to come into existance and disappear without
breaking the logic of a LimitOrderBook.
'''


class InputMessageEventLog():

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._event_log = None
        self._iter = None
        self._message_factory = MessageFactory()

    def open(self) -> None:
        self._initialize()

    def close(self) -> None:
        self._cleanup()

    def _initialize(self) -> None:
        try:
            event_log = InputTextEventLog(file_path=self._file_path)
            event_log.open()
            self._event_log = event_log
        except Exception as error:
            print(error)
            raise

    def _cleanup(self) -> None:
        self._event_log.close()

    def __enter__(self):
        self._initialize()
        return self

    def __exit__(self, exception_type, exception_value, exception_backtrace) -> bool:
        self._cleanup()

    def __iter__(self):
        self._iter = iter(self._event_log)
        return self

    def __next__(self):
        message_string = next(self._iter)
        try:
            message = self._message_factory.create(message_string)
            return message
        except Exception as error:
            print(f'could not read from file {self._file_path}')
            print(error)
            raise


class OutputMessageEventLog():

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._event_log = None

    def open(self) -> None:
        self._initialize()

    def close(self) -> None:
        self._cleanup()

    def _initialize(self) -> None:
        try:
            event_log = OutputTextEventLog(file_path=self._file_path)
            event_log.open()
            self._event_log = event_log
        except Exception as error:
            print(f'failed to open file {self._file_path}')
            print(error)
            raise

    def _cleanup(self) -> None:
        self._event_log.close()

    def __enter__(self):
        self._initialize()
        return self

    def __exit__(self, exception_type, exception_value, exception_backtrace) -> bool:
        self._cleanup()

    def write(self, message: AbstractMessage) -> int:
        message_string = message.serialize()
        count = self._event_log.write(message=message_string)
        return count

