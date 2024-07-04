
from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app
from limit_order_book.types.order_id import OrderId
from limit_order_book.exceptions import DuplicateOrderIdError


client = TestClient(app)


def test_ping():
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'ping': 'pong',
    }


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'documentation_page:': 'https://github.com/edward-b-1/Python-Limit-Order-Book',
        'message': 'please download the client application from the documentation page to interact with this site'
    }



def helper_generate_order(order_id: int, ticker: str, order_side: str, price: int, volume: int):
    return {
        'order_id': order_id,
        'ticker': ticker,
        'order_side': order_side,
        'price': price,
        'volume': volume,
    }


def helper_generate_top_of_book(
    ticker: str,
    price_buy: int|None,
    volume_buy: int|None,
    price_sell: int|None,
    volume_sell: int|None,
):
    return {
        'status': 'success',
        'message': None,
        'top_of_book': {
            'ticker': ticker,
            'price_buy': price_buy,
            'volume_buy': volume_buy,
            'price_sell': price_sell,
            'volume_sell': volume_sell,
        }
    }


def helper_generate_ticker(
    ticker: str,
):
    return {
        'ticker': ticker,
    }


def helper_generate_order_id(
    order_id: int,
):
    return {
        'order_id': order_id,
    }


def test_same_order_id():

    json = helper_generate_order(1, 'PYTH', 'BUY', 1000, 10)
    response = client.post('/send_order', json=json)
    assert response.status_code == 200

    json = helper_generate_order(1, 'PYTH', 'BUY', 1025, 15)
    response = client.post('/send_order', json=json)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        'status': 'error',
        'message': str(DuplicateOrderIdError(OrderId(1))),
    }


def test_top_of_book():
    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', None, None, None, None)

    json = helper_generate_order(1, 'PYTH', 'BUY', 1000, 10)
    response = client.post('/send_order', json=json)
    assert response.status_code == 200

    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 10, None, None)

    json = helper_generate_order(2, 'PYTH', 'SELL', 1025, 15)
    response = client.post('/send_order', json=json)
    assert response.status_code == 200

    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 10, 1025, 15)

    json = helper_generate_order_id(1)
    response = client.post('/cancel_order', json=json)
    assert response.status_code == 200

    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 0, 1025, 15)



def test_sequence():
    assert True