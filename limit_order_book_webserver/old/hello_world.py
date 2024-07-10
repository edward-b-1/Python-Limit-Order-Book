
from flask import Flask, request
from limit_order_book.limit_order_book_wrapper import LimitOrderBook
from limit_order_book.order import Order
from limit_order_book.types.order_id import OrderId
from limit_order_book.ticker import Ticker
from limit_order_book.order_side import OrderSide
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume


print(f'__name__={__name__}')

limit_order_book = LimitOrderBook()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello world!</p>'


@app.post('/api/send_order')
def send_order():
    content = request.json
    print(content)

    try:

        order_id_str = content.get('order_id')
        ticker_str = content.get('ticker')
        order_side_str = content.get('order_side')
        int_price_str = content.get('price')
        volume_str = content.get('volume')

        order_id_int = int(order_id_str)
        int_price_int = int(int_price_str)
        volume_int = int(volume_str)

        order_id = OrderId(order_id_int)
        ticker = Ticker(ticker_str)
        order_side = OrderSide(order_side)
        int_price = IntPrice(int_price_int)
        volume = Volume(volume_int)

        order = Order(
            order_id=order_id,
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume
        )
        limit_order_book.order_insert(order)

        d = {
            'order_id': content.get('order_id'),
        }

        return d

    except Exception:
