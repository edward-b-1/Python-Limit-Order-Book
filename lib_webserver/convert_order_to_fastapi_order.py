
from lib_financial_exchange.financial_exchange_types import Order
from lib_webserver.webserver_types import FastAPI_Order


def convert_order_to_fastapi_order(order: Order) -> FastAPI_Order:

    fastapi_order = FastAPI_Order(
        order_id=order._order_id.to_int(),
        ticker=order._ticker.to_str(),
        order_side=str(order._order_side),
        price=order._int_price.to_int(),
        volume=order._volume.to_int(),
    )
    return fastapi_order
