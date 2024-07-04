
from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app
from limit_order_book.types.order_id import OrderId
from limit_order_book.exceptions import DuplicateOrderIdError

from tests.test_webserver.helper import helper_generate_order_without_order_id
from tests.test_webserver.helper import helper_generate_order_id
from tests.test_webserver.helper import helper_generate_ticker
from tests.test_webserver.helper import helper_generate_top_of_book

client = TestClient(app)


def test_top_of_book():
    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', None, None, None, None)

    json = helper_generate_order_without_order_id('PYTH', 'BUY', 1000, 10)
    response = client.post('/send_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 1,
        'trades': [],
    }

    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 10, None, None)

    json = helper_generate_order_without_order_id('PYTH', 'SELL', 1025, 15)
    response = client.post('/send_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 2,
        'trades': [],
    }

    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 10, 1025, 15)

    json = helper_generate_order_id(1)
    response = client.post('/cancel_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': 'order id 1 cancelled',
        'order': {
            'order_id': 1,
            'ticker': 'PYTH',
            'order_side': 'BUY',
            'price': 1000,
            'volume': 10,
        }
    }

    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', None, None, 1025, 15)