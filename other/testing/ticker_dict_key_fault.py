from limit_order_book.ticker import Ticker

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

