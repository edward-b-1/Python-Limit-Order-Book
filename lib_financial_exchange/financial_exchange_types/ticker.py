
class Ticker():

    def __init__(self, ticker) -> None:
        assert isinstance(ticker, str), f'ticker must be of type str'
        assert len(ticker) > 0, f'ticker cannot be empty string'
        self._ticker = ticker

    def __hash__(self) -> int:
        return hash(self._ticker)

    def __str__(self) -> str:
        return f'Ticker({self._ticker})'

    def __repr__(self) -> str:
        return f'Ticker({self._ticker})'

    def __eq__(self, ticker: object) -> bool:
        if isinstance(ticker, Ticker):
            return self._ticker == ticker._ticker
        return False

    def to_str(self) -> str:
        return self._ticker