

class InputTextEventLog():

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._file = None
        self._iter = None

    def open(self) -> None:
        self._initialize()

    def close(self) -> None:
        self._cleanup()

    def _initialize(self) -> None:
        try:
            file = open(self._file_path, 'r')
            self._file = file
        except Exception as error:
            print(f'failed to open file {self._file_path}')
            print(error)
            raise

    def _cleanup(self) -> None:
        self._file.flush()
        self._file.close()

    def __enter__(self):
        self._initialize()
        return self

    def __exit__(self, exception_type, exception_value, exception_backtrace) -> bool:
        self._cleanup()

    def __iter__(self):
        self._iter = iter(self._file)
        return self

    def __next__(self):
        message_string = next(self._iter).rstrip()
        if len(message_string) > 0:
            return message_string
        else:
            raise StopIteration()



class OutputTextEventLog():

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._file = None

    def open(self) -> None:
        self._initialize()

    def close(self) -> None:
        self._cleanup()

    def _initialize(self) -> None:
        try:
            file = open(self._file_path, 'a')
            self._file = file
        except Exception as error:
            print(f'failed to open file {self._file_path}')
            print(error)
            raise

    def _cleanup(self) -> None:
        self._file.flush()
        self._file.close()

    def __enter__(self):
        self._initialize()
        return self

    def __exit__(self, exception_type, exception_value, exception_backtrace) -> bool:
        self._cleanup()

    def write(self, message: str) -> int:
        count = self._file.write(f'{message}\n')
        self._file.flush()
        return count

