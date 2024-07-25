

from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app

from lib_webserver.webserver import Webserver

from lib_datetime import datetime_to_string
from lib_datetime import datetime_to_order_board_display_string

from datetime import datetime
from datetime import timezone

from limit_order_book_webserver.get_webserver_instance import get_webserver_instance

# client = TestClient(app)

webserver_fake = Webserver(test_mode=True)

def override_get_webserver_instance():
    return webserver_fake

app.dependency_overrides[get_webserver_instance] = override_get_webserver_instance


def test_send_order():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {
            'ticker': 'EXAMPLE_TICKER',
            'order_side': 'BUY',
            'price': 1000,
            'volume': 10,
        }
        response = client.post('/api/send_order', json=json)
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
            'order_id': 2,
            'trades': [
                {
                    'trade_id': 1,
                    'order_id_maker': 1,
                    'order_id_taker': 2,
                    'timestamp': datetime_to_string(timestamp),
                    'ticker': 'EXAMPLE_TICKER',
                    'price': 1000,
                    'volume': 10,
                }
            ]
        }


def test_update_order():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {
            'order_id': 1,
            'price': 1000,
            'volume': 10,
        }
        response = client.post('/api/update_order', json=json)
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
            'trades': [
                {
                    'trade_id': 1,
                    'order_id_maker': 1,
                    'order_id_taker': 2,
                    'timestamp': datetime_to_string(timestamp),
                    'ticker': 'EXAMPLE_TICKER',
                    'price': 1000,
                    'volume': 10,
                }
            ]
        }


def test_cancel_order_partial():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {
            'order_id': 1,
            'volume': 10,
        }
        response = client.post('/api/cancel_order_partial', json=json)
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
        }


def test_cancel_order():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {
            'order_id': 1,
        }
        response = client.post('/api/cancel_order', json=json)
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
            'order': {
                'order_id': 1,
                'timestamp': datetime_to_string(timestamp),
                'ticker': 'EXAMPLE_TICKER',
                'order_side': 'BUY',
                'price': 1000,
                'volume': 10,
            }
        }


def test_top_of_book():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {
            'ticker': 'EXAMPLE_TICKER',
        }
        response = client.post('/api/top_of_book', json=json)
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
            'top_of_book': {
                'ticker': 'EXAMPLE_TICKER',
                'price_buy': 1000,
                'volume_buy': 100,
                'price_sell': 990,
                'volume_sell': 50,
            }
        }


def test_list_all_tickers():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {}
        response = client.post('/api/list_all_tickers', json=json)
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
            'tickers': [
                'EXAMPLE_TICKER'
            ]
        }


def test_order_board():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {}
        response = client.get('/api/order_board')
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
            'orders': [
                {
                    'order_id': 1,
                    'timestamp': datetime_to_order_board_display_string(timestamp),
                    'ticker': 'EXAMPLE_TICKER',
                    'order_side': 'BUY',
                    'price': 1000,
                    'volume': 10,
                }
            ]
        }


def test_trades():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {}
        response = client.get('/api/trades')
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
            'trades': [
                {
                    'trade_id': 1,
                    'order_id_maker': 1,
                    'order_id_taker': 2,
                    'timestamp': datetime_to_string(timestamp),
                    'ticker': 'EXAMPLE_TICKER',
                    'price': 1000,
                    'volume': 10,
                }
            ]
        }


def test_ping():
    timestamp = datetime(
        year=2024, month=7, day=25,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    with TestClient(app) as client:
        json = {}
        response = client.get('/api/debug/ping')
        assert response.status_code == 200
        assert response.json() == {
            'status': 'success',
            'message': 'no message',
            'ping': 'pong'
        }

