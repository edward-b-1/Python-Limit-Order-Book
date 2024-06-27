




class Ticker():

    def __init__(self, ticker: object):
        if isinstance(ticker, str):
            self._ticker = TickerStr(ticker)
        elif isinstance(ticker, int):
            self._ticker = TickerInt(ticker)
        else:
            raise TypeError(f'unsupported type {type(ticker)} for ticker')

    def __str__(self) -> str:
        return str(self._ticker)

    def __eq__(self, ticker: object) -> bool:
        if isinstance(ticker, Ticker):
            return self._ticker._get_value() == ticker._ticker._get_value()
        return False


class TickerStr():

    def __init__(self, ticker_str) -> None:
        assert isinstance(ticker_str, str), f'ticker must be of type str'
        assert len(ticker_str) > 0, f'ticker cannot be empty string'
        self._ticker_str = ticker_str

    def __str__(self) -> str:
        return f'Ticker[str]({self._ticker_str})'

    def _get_value(self) -> str:
        return self._ticker_str


class TickerInt():

    def __init__(self, ticker_int) -> None:
        assert isinstance(ticker_int, int), f'ticker must be of type int'
        assert ticker_int > 0, f'ticker must be > 0'
        self._ticker_int = ticker_int

    def __str__(self) -> str:
        return f'Ticker[int]({self._ticker_int})'

    def _get_value(self) -> int:
        return self._ticker_int
