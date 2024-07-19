from lib_financial_exchange.financial_exchange_types import Ticker

d = {}

ticker = Ticker('PYTH')

if not ticker in d:
    print(f'adding ticker {ticker} to dict')
    d[ticker] = 'hello world'
    print(d[ticker])

if not ticker in d:
    print(f'adding ticker {ticker} to dict')
    d[ticker] = 'goodbye world'
    print(d[ticker])

