
from lib_financial_exchange.financial_exchange_types import Order
from lib_webserver.webserver_types import FastAPI_Order

from lib_webserver.convert_order_to_fastapi_order import convert_order_to_fastapi_order


def convert_order_list_to_fastapi_order_list(order_list: list[Order]) -> list[FastAPI_Order]:

    fastapi_order_list = (
        list(
            map(
                lambda order: convert_order_to_fastapi_order(order),
                order_list,
            )
        )
    )
    return fastapi_order_list
