
from fastapi import status
from fastapi.testclient import TestClient

from limit_order_book_webserver.webserver import app

from tests.test_webserver.helper import helper_generate_order_without_order_id

client = TestClient(app)


def test_ping():
    response = client.get('/api/debug/ping')
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


def test_same_order_id():

    json = helper_generate_order_without_order_id('PYTH', 'BUY', 1000, 10)
    response = client.post('/api/send_order', json=json)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 1,
        'trades': []
    }

    json = helper_generate_order_without_order_id('PYTH', 'BUY', 1025, 15)
    response = client.post('/api/send_order', json=json)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 2,
        'trades': []
    }
