
from limit_order_book.types import OrderId
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.types import OrderSide
from limit_order_book.types import Ticker
from limit_order_book.types import OrderWithoutOrderId
from limit_order_book.types import Order
from limit_order_book.types import Trade
from limit_order_book.types import TopOfBook
from limit_order_book.limit_order_book import LimitOrderBook


def test_limit_order_book_trade_insert_new():

    # Book Setup:
    #
    #                                ts_recv                            ts_event  rtype  publisher_id  instrument_id action side  price  size  channel_id  order_id  flags  ts_in_delta  sequence symbol
    # 0  2024-01-05 09:00:11.023091471+00:00 2024-01-05 09:00:11.022925094+00:00    160             2          11667      A    B  480.3   200           0    167971    130       166377    301714   NVDA
    # 1  2024-01-05 09:00:15.833467732+00:00 2024-01-05 09:00:15.833295750+00:00    160             2          11667      T    A  480.3    70           0         0    130       171982    310185   NVDA
    # 2  2024-01-05 09:00:15.833467732+00:00 2024-01-05 09:00:15.833295750+00:00    160             2          11667      F    B  480.3    70           0    167971    130       171982    310185   NVDA
    # 3  2024-01-05 09:00:15.833467732+00:00 2024-01-05 09:00:15.833295750+00:00    160             2          11667      C    B  480.3    70           0    167971    130       171982    310185   NVDA
    # 4  2024-01-05 09:00:22.759005056+00:00 2024-01-05 09:00:22.758837452+00:00    160             2          11667      T    A  480.3   130           0         0    130       167604    316861   NVDA

    lob = LimitOrderBook()
    ticker = Ticker('NVDA')

    ####

    order_0 = OrderWithoutOrderId(
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(4803000),
        volume=Volume(200),
    )
    (order_id_0, trades) = lob.order_insert(order_0)
    assert trades == []

    ####

    order_1 = OrderWithoutOrderId(
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(4803000),
        volume=Volume(70),
    )
    (order_id_1, trades) = lob.order_insert(order_1)
    assert trades == [
        Trade(order_id_maker=order_id_0, order_id_taker=order_id_1, ticker=ticker, int_price=IntPrice(4803000), volume=Volume(70)),
    ]

    ####

    order_2 = OrderWithoutOrderId(
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(4803000),
        volume=Volume(130),
    )
    (order_id_2, trades) = lob.order_insert(order_2)
    assert trades == [
        Trade(order_id_maker=order_id_0, order_id_taker=order_id_2, ticker=ticker, int_price=IntPrice(4803000), volume=Volume(130)),
    ]

    top_of_book = lob.top_of_book(ticker)
    print(top_of_book)

    assert top_of_book == TopOfBook(
        ticker=ticker,
        int_price_buy=None,
        volume_buy=None,
        int_price_sell=None,
        volume_sell=None,
    )
