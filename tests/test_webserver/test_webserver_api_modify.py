
from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app
from limit_order_book.types.order_id import OrderId
from limit_order_book.exceptions import DuplicateOrderIdError

from tests.test_webserver.helper import helper_generate_order_without_order_id
from tests.test_webserver.helper import helper_generate_order_id_price_volume
from tests.test_webserver.helper import helper_generate_order_id
from tests.test_webserver.helper import helper_generate_ticker
from tests.test_webserver.helper import helper_generate_top_of_book

client = TestClient(app)


def test_webserver_api_order_modify():
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

    json = helper_generate_order_id_price_volume(1, 1000, 9)
    response = client.post('/modify_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'trades': [],
    }
    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 9, None, None)

    json = helper_generate_order_id_price_volume(1, 1000, 12)
    response = client.post('/modify_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'trades': [],
    }
    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 12, None, None)

    json = helper_generate_order_id_price_volume(1, 1010, 12)
    response = client.post('/modify_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'trades': [],
    }
    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1010, 12, None, None)

    json = helper_generate_order_id_price_volume(1, 900, 20)
    response = client.post('/modify_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'trades': [],
    }
    json = helper_generate_ticker('PYTH')
    response = client.post('/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 900, 20, None, None)

