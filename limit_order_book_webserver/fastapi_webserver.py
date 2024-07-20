
import os
import threading

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi import Response
from fastapi import status

from fastapi.middleware.cors import CORSMiddleware

from limit_order_book_webserver.fastapi_webserver_logging import log

from lib_webserver.webserver_types import FastAPI_OrderInsertMessage
from lib_webserver.webserver_types import FastAPI_OrderUpdateMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelPartialMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelMessage
from lib_webserver.webserver_types import FastAPI_TopOfBookMessage

from lib_webserver.webserver_types import FastAPI_Ticker

from lib_webserver.webserver_types import FastAPI_ReturnStatus

from lib_webserver.webserver import Webserver

from lib_datetime import now


webserver_test_mode = False
if os.environ.get('ENABLE_WEBSERVER_TEST_MODE'):
    webserver_test_mode = True
webserver = Webserver(test_mode=webserver_test_mode)


origins_for_real_mode = [
    'http://www.python-limit-order-book.co.uk',
    'http://python-limit-order-book.co.uk',
]

origins_for_fake_mode = [
    'http://localhost:5555'
]
# more fake origins - delete or use
# origins = [
#     'http://localhost:5555',
#     'http://localhost:80',
#     'http://python-limit-order-book.co.uk:5555',
#     'http://python-limit-order-book.co.uk:5173',
#     'http://python-limit-order-book.co.uk:80',
# ]

origins = origins_for_real_mode
if webserver_test_mode:
    origins = origins_for_fake_mode


print(f'__name__={__name__}')


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# TODO: remove this? or change to `/api` - it conflicts with '/' on frontend
@app.get('/')
def root():
    log.info(f'GET /')
    return {
        'website_address': 'https://www.python-limit-order-book.co.uk',
        'documentation_page:': 'https://github.com/edward-b-1/Python-Limit-Order-Book',
        'message': 'please download the client application from the documentation page to interact with this site, or visit the website https://www.python-limit-order-book.co.uk'
    }


def debug_print_pid():
    print(f'pid={os.getpid()}')
    print(f'threading.native_id={threading.get_native_id()}')


@app.post('/api/send_order')
def send_order(
    fastapi_order_insert_message: FastAPI_OrderInsertMessage,
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/send_order ({ip}, {timestamp})')

    try:
        return webserver.send_order(fastapi_order_insert_message)

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


    # try:
    #     (order_id, trades) = limit_order_book.order_insert(ip, order)
    #     trade_record.add_trades(trades)

    #     fastapi_order_id = FastAPI_OrderId(order_id=order_id.to_int()).order_id
    #     fastapi_trades = convert_trades_to_fastapi_trades(trades)

    #     return FastAPI_ReturnStatusWithTradesAndOrderId(
    #         status='success',
    #         message=None,
    #         order_id=fastapi_order_id,
    #         trades=fastapi_trades,
    #     )
    # # # NOTE: Since the OrderId is now automatically provided and incremented from
    # # # within the Limit Order Book Wrapper class, this can no longer happen
    # # except DuplicateOrderIdError as error:
    # #     response.status_code = status.HTTP_409_CONFLICT
    # #     return FastAPI_ReturnStatus(
    # #         status='error',
    # #         message=str(error),
    # #     )
    # #     # return JSONResponse(
    # #     #     status_code=status.HTTP_409_CONFLICT,
    # #     #     content=json.dumps(
    # #     #         FastAPI_ReturnStatus(
    # #     #             status='error',
    # #     #             message=str(error),
    # #     #         )
    # #     #     )
    # #     # )
    # except RuntimeError as error:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail={
    #             'status': 'error',
    #             'message': str(error),
    #         },
    #     )


@app.post('/api/update_order')
def update_order(
    fastapi_order_update_message: FastAPI_OrderUpdateMessage,
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/update_order ({ip}, {timestamp})')

    try:
        return webserver.update_order(fastapi_order_update_message)

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.post('/api/cancel_order_partial')
def cancel_order_partial(
    fastapi_order_cancel_partial_message: FastAPI_OrderCancelPartialMessage,
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/cancel_order_partial ({ip}, {timestamp})')

    try:
        return webserver.cancel_order_partial(fastapi_order_cancel_partial_message)

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.post('/api/cancel_order')
def cancel_order(
    fastapi_order_cancel_message: FastAPI_OrderCancelMessage,
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/cancel_order ({ip}, {timestamp})')

    try:
        return webserver.cancel_order(fastapi_order_cancel_message)

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.post('/api/top_of_book')
def top_of_book(
    fastapi_top_of_book_message: FastAPI_TopOfBookMessage,
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/top_of_book ({ip}, {timestamp})')

    try:
        return webserver.top_of_book(fastapi_top_of_book_message)

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.post('/api/list_all_tickers')
def list_all_tickers(
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/list_all_tickers ({ip}, {timestamp})')

    try:
        return webserver.list_all_tickers()

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.get('/api/order_board')
def order_board(
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'GET /api/order_board ({ip}, {timestamp})')

    try:
        return webserver.order_board()

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.get('/api/trades')
def trades(
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'GET /api/trades ({ip}, {timestamp})')

    try:
        return webserver.trades()

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.get('/api/debug/ping')
def ping(
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'GET /api/debug/ping ({ip}, {timestamp})')

    try:
        return webserver.ping()

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.post('/api/debug/debug_log_top_of_book')
def debug_log_top_of_book(
    fastapi_ticker: FastAPI_Ticker,
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/debug/debug_log_top_of_book ({ip}, {timestamp})')

    try:
        return webserver.debug_log_top_of_book(fastapi_ticker)

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.post('/api/debug/debug_log_current_order_id')
def debug_log_current_order_id(
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/debug/debug_log_current_order_id ({ip}, {timestamp})')

    try:
        return webserver.debug_log_current_order_id()

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )


@app.post('/api/debug/debug_log_all_tickers')
def debug_log_all_tickers(
    request: Request,
    response: Response,
):
    debug_print_pid()
    timestamp = now()
    ip = request.client.host

    log.info(f'POST /api/debug/debug_log_all_tickers ({ip}, {timestamp})')

    try:
        return webserver.debug_log_all_tickers()

    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return FastAPI_ReturnStatus(
            status='error',
            message='internal server error',
        )




# # TODO remove and save for later
# @app.post('/api/login')
# def client_login(fastapi_client_data: FastAPI_ClientData, request: Request, response: Response):
#     now = datetime.now(timezone.utc)
#     ip = request.client.host
#     log.info(f'/api/login: {now} {ip}')

#     try:
#         client_name = ClientName(client_name=fastapi_client_data.client_name)
#         client_password = ClientPassword(client_password=fastapi_client_data.client_password)
#         if not client_database.client_exists(client_name):
#             client_database.add_client(client_name, client_password)
#         else:
#             if client_database.check_password(
#                 client_name=client_name,
#                 client_password=client_password,
#             ):
#                 # generate login token
#                 # return this token to the client
#                 return FastAPI_ReturnStatusWithLoginToken(
#                     status='ok',
#                     message='login success',
#                     token='login_token',
#                 )
#             else:
#                 return FastAPI_ReturnStatusFailedLogin(
#                     status='error',
#                     message='incorrect password',
#                     client_name=fastapi_client_data.client_name,
#                 )

#     except ClientNameAlreadyExistsError as error:
#         return FastAPI_ReturnStatusFailedLogin(
#             status='error',
#             message=str(error),
#             client_name=fastapi_client_data.client_name,
#         )

#     except MissingClientNameError as error:
#         return FastAPI_ReturnStatusFailedLogin(
#             status='error',
#             message=str(error),
#             client_name=fastapi_client_data.client_name,
#         )

#     except InvalidClientNameError as error:
#         return FastAPI_ReturnStatusInvalidClientName(
#             status='error',
#             message=str(error),
#             client_name=fastapi_client_data.client_name,
#         )

#     except InvalidClientPasswordError as error:
#         return FastAPI_ReturnStatusInvalidClientPassword(
#             status='error',
#             message=str(error),
#             client_name=fastapi_client_data.client_name,
#         )

#     except Exception as error:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return FastAPI_ReturnStatus(
#             message='error',
#             status=str(error),
#         )

