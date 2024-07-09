
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import status

from fake_webserver.types import FastAPI_OrderId
from fake_webserver.types import FastAPI_OrderIdPriceVolume
from fake_webserver.types import FastAPI_Ticker
from fake_webserver.types import FastAPI_Order
from fake_webserver.types import FastAPI_OrderWithoutOrderId
from fake_webserver.types import FastAPI_Trade
from fake_webserver.types import FastAPI_TopOfBook
from fake_webserver.types import FastAPI_ReturnStatus
from fake_webserver.types import FastAPI_ReturnStatusWithOrder
from fake_webserver.types import FastAPI_ReturnStatusWithTrades
from fake_webserver.types import FastAPI_ReturnStatusWithTradesAndOrderId
from fake_webserver.types import FastAPI_ReturnStatusWithTopOfBook
from fake_webserver.types import FastAPI_ReturnStatusWithTickerList

from fastapi.middleware.cors import CORSMiddleware

import random

random.seed(1234)

def randomPrice():
    return 1000 + random.randint(-50, 50)

def randomVolume():
    return random.randint(0, 100)


origins = [
    'http://localhost:5555',
    'http://python-limit-order-book.co.uk:5555',
    'http://python-limit-order-book.co.uk:5173',
    'http://python-limit-order-book.co.uk:80',
]


print(f'__name__={__name__}')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# NOTE: different return structure
@app.post('/api/send_order')
def send_order(fastapi_order: FastAPI_OrderWithoutOrderId, response: Response):
    print(f'{fastapi_order}')
    return FastAPI_ReturnStatus(
        status='success',
        message='fake endpoint ignores this post request'
    )

# NOTE: different return structure
@app.post('/api/modify_order')
def modify_order(fastapi_order_id_price_volume: FastAPI_OrderIdPriceVolume):
    print(f'{fastapi_order_id_price_volume}')
    return FastAPI_ReturnStatus(
        status='success',
        message='fake endpoint ignores this post request'
    )

# NOTE: different return structure
@app.post('/api/cancel_order')
def cancel_order(fastapi_order_id: FastAPI_OrderId):
    print(f'{fastapi_order_id}')
    return FastAPI_ReturnStatus(
        status='success',
        message='fake endpoint ignores this post request'
    )

@app.post('/api/cancel_order_partial')
def cancel_order_partial(fastapi_order_id: FastAPI_OrderId):
    print(f'{fastapi_order_id}')
    return FastAPI_ReturnStatus(
        status='success',
        message='fake endpoint ignores this post request'
    )

@app.post('/api/top_of_book')
def top_of_book(fastapi_ticker: FastAPI_Ticker):
    fastapi_top_of_book = FastAPI_TopOfBook(
        ticker=fastapi_ticker.ticker,
        price_buy=randomPrice(),
        volume_buy=randomVolume(),
        price_sell=randomPrice(),
        volume_sell=randomVolume(),
    )
    r = FastAPI_ReturnStatusWithTopOfBook(
        status='success',
        message=None,
        top_of_book=fastapi_top_of_book,
    )
    return r

@app.post('/api/list_all_tickers')
def list_all_tickers():
    tickers = ['PYTH', 'RUST', 'CPP', 'JS']
    return FastAPI_ReturnStatusWithTickerList(
        status='success',
        message=None,
        tickers=tickers,
    )

@app.get('/')
def root():
    return {
        'homepage'
    }