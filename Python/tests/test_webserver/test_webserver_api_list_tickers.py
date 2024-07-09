
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


def test_list_all_tickers():
    json = helper_generate_ticker('PYTH')
    response = client.post('/api/top_of_book', json=json)
    assert response.status_code == 200

    json = helper_generate_ticker('CPP')
    response = client.post('/api/top_of_book', json=json)
    assert response.status_code == 200

    json = helper_generate_ticker('RUST')
    response = client.post('/api/top_of_book', json=json)
    assert response.status_code == 200

    json = helper_generate_ticker('JS')
    response = client.post('/api/top_of_book', json=json)
    assert response.status_code == 200

    response = client.post('/api/list_all_tickers')
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        'status': 'success',
        'message': None,
        'tickers': [
            'PYTH',
            'CPP',
            'RUST',
            'JS',
        ],
    }