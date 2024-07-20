
from lib_financial_exchange.financial_exchange_types import Order
from lib_webserver.webserver_types import FastAPI_Order

from lib_datetime import datetime_to_order_board_display_string


def convert_order_to_fastapi_order(order: Order) -> FastAPI_Order:

    fastapi_order = FastAPI_Order(
        order_id=order.to_order_id().to_int(),
        timestamp=datetime_to_order_board_display_string(order._timestamp),
        ticker=order.to_ticker().to_str(),
        order_side=str(order.to_order_side()),
        price=order.to_int_price().to_int(),
        volume=order.to_volume().to_int(),
    )
    return fastapi_order
