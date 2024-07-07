
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import status

from limit_order_book.limit_order_book_wrapper import LimitOrderBook
from limit_order_book.order import Order
from limit_order_book.order_without_order_id import OrderWithoutOrderId
from limit_order_book.trade import Trade
from limit_order_book.types.order_id import OrderId
from limit_order_book.ticker import Ticker
from limit_order_book.order_side import OrderSide
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.exceptions import DuplicateOrderIdError

from limit_order_book_webserver.types import FastAPI_OrderId
from limit_order_book_webserver.types import FastAPI_OrderIdPriceVolume
from limit_order_book_webserver.types import FastAPI_Ticker
from limit_order_book_webserver.types import FastAPI_Order
from limit_order_book_webserver.types import FastAPI_OrderWithoutOrderId
from limit_order_book_webserver.types import FastAPI_Trade
from limit_order_book_webserver.types import FastAPI_TopOfBook
from limit_order_book_webserver.types import FastAPI_ReturnStatus
from limit_order_book_webserver.types import FastAPI_ReturnStatusWithOrder
from limit_order_book_webserver.types import FastAPI_ReturnStatusWithTrades
from limit_order_book_webserver.types import FastAPI_ReturnStatusWithTradesAndOrderId
from limit_order_book_webserver.types import FastAPI_ReturnStatusWithTopOfBook

from limit_order_book_webserver.convert_trades_to_fastapi_trades import convert_trades_to_fastapi_trades

import os
import threading

limit_order_book = LimitOrderBook()


print(f'__name__={__name__}')
app = FastAPI()

@app.get('/')
def root():
    return {
        'documentation_page:': 'https://github.com/edward-b-1/Python-Limit-Order-Book',
        'message': 'please download the client application from the documentation page to interact with this site'
    }

@app.post('/send_order')
def send_order(fastapi_order: FastAPI_OrderWithoutOrderId, response: Response):
    print(f'pid={os.getpid()}')
    print(f'threading.native_id={threading.get_native_id()}')
    order = OrderWithoutOrderId(
        ticker=Ticker(fastapi_order.ticker),
        order_side=OrderSide(value=fastapi_order.order_side),
        int_price=IntPrice(fastapi_order.price),
        volume=Volume(fastapi_order.volume),
    )
    try:
        (order_id, trades) = limit_order_book.order_insert(order)
        fastapi_order_id = FastAPI_OrderId(order_id=order_id.to_int()).order_id
        fastapi_trades = convert_trades_to_fastapi_trades(trades)
        return FastAPI_ReturnStatusWithTradesAndOrderId(
            status='success',
            message=None,
            order_id=fastapi_order_id,
            trades=fastapi_trades,
        )
    # NOTE: Since the OrderId is now automatically provided and incremented from
    # within the Limit Order Book Wrapper class, this can no longer happen
    except DuplicateOrderIdError as error:
        response.status_code = status.HTTP_409_CONFLICT
        return FastAPI_ReturnStatus(
            status='error',
            message=str(error),
        )
        # return JSONResponse(
        #     status_code=status.HTTP_409_CONFLICT,
        #     content=json.dumps(
        #         FastAPI_ReturnStatus(
        #             status='error',
        #             message=str(error),
        #         )
        #     )
        # )
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'status': 'error',
                'message': str(error),
            },
        )

@app.post('/cancel_order')
def cancel_order(fastapi_order_id: FastAPI_OrderId):
    print(f'pid={os.getpid()}')
    print(f'threading.native_id={threading.get_native_id()}')
    order_id = OrderId(fastapi_order_id.order_id)
    order = limit_order_book.order_cancel(order_id)

    if order is None:
        return FastAPI_ReturnStatus(
            status='success',
            message=f'order id {fastapi_order_id.order_id} does not exist, no order to cancel',
        )
    else:
        fastapi_order = FastAPI_Order(
            order_id=order._order_id.to_int(),
            ticker=order._ticker.to_str(),
            order_side=str(order._order_side),
            price=order._int_price.to_int(),
            volume=order._volume.to_int(),
        )
        return FastAPI_ReturnStatusWithOrder(
            status='success',
            message=f'order id {fastapi_order_id.order_id} cancelled',
            order=fastapi_order,
        )

@app.post('/modify_order')
def modify_order(fastapi_order_id_price_volume: FastAPI_OrderIdPriceVolume):
    print(f'pid={os.getpid()}')
    print(f'threading.native_id={threading.get_native_id()}')

    order_id=OrderId(fastapi_order_id_price_volume.order_id)
    int_price=IntPrice(fastapi_order_id_price_volume.price)
    volume=Volume(fastapi_order_id_price_volume.volume)

    trades = limit_order_book.order_update(order_id=order_id, int_price=int_price, volume=volume)
    fastapi_trades = convert_trades_to_fastapi_trades(trades)
    return FastAPI_ReturnStatusWithTrades(
        status='success',
        message=None,
        trades=fastapi_trades,
    )

@app.post('/top_of_book')
def top_of_book(fastapi_ticker: FastAPI_Ticker):
    print(f'pid={os.getpid()}')
    print(f'threading.native_id={threading.get_native_id()}')
    ticker = Ticker(
        ticker=fastapi_ticker.ticker,
    )
    top_of_book = limit_order_book.top_of_book(ticker)

    ticker = top_of_book._ticker.to_str()

    price_buy = top_of_book._int_price_buy
    if price_buy is not None:
        price_buy = price_buy._int_price

    price_sell = top_of_book._int_price_sell
    if price_sell is not None:
        price_sell = price_sell._int_price

    volume_buy = top_of_book._volume_buy
    if volume_buy is not None:
        volume_buy = volume_buy._volume

    volume_sell = top_of_book._volume_sell
    if volume_sell is not None:
        volume_sell = volume_sell._volume

    fastapi_top_of_book = FastAPI_TopOfBook(
        ticker=ticker,
        price_buy=price_buy,
        volume_buy=volume_buy,
        price_sell=price_sell,
        volume_sell=volume_sell,
    )
    r = FastAPI_ReturnStatusWithTopOfBook(
        status='success',
        message=None,
        top_of_book=fastapi_top_of_book,
    )
    return r

@app.get('/ping')
def ping():
    return {
        'status': 'success',
        'message': None,
        'ping': 'pong',
    }


# shared_data = None

# class FastAPI_Value(BaseModel):
#     value: str

# @app.post('/put')
# def put(value: FastAPI_Value):
#     print(f'value={value.value}')
#     global shared_data
#     shared_data = value
#     return {
#         'status': 'success',
#     }

# @app.get('/get')
# def get():
#     return {
#         'shared_data': shared_data,
#     }