
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app

from tests.webserver_tests.test_whole_system.helper import helper_generate_order_without_order_id
from tests.webserver_tests.test_whole_system.helper import helper_generate_order_id

client = TestClient(app)

import lib_datetime


from datetime import datetime

def monkeypatch_now() -> datetime:
    return datetime(year=2024, month=7, day=20)


# TODO: this test is trying to test the internal logic via the FastAPI webserver interface
# it is a legitimate test, but not really testing the FastAPI webserver paths by themselves
def test_order_trade():
    lib_datetime.now = monkeypatch_now()

    json = helper_generate_order_without_order_id('PYTH', 'BUY', 1000, 10)
    response = client.post('/api/send_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 1,
        'trades': []
    }

    json = helper_generate_order_without_order_id('PYTH', 'SELL', 995, 5)
    response = client.post('/api/send_order', json=json)
    assert response.status_code == 200
    print(response.json()['trades'])
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 2,
        'trades': [
            {
                'trade_id': 1,
                'timestamp': monkeypatch_now(),
                'ticker': 'PYTH',
                'order_id_maker': 1,
                'order_id_taker': 2,
                'price': 995,
                'volume': 5,
            }
        ]
    }

    json = helper_generate_order_id(1)
    response = client.post('/api/cancel_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': 'order id 1 cancelled',
        'order': {
            'order_id': 1,
            'ticker': 'PYTH',
            'order_side': 'BUY',
            'price': 1000,
            'volume': 5,
        }
    }
