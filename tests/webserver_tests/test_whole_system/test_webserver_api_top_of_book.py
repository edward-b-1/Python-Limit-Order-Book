
from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.exceptions import DuplicateOrderIdError

from tests.webserver_tests.test_whole_system.helper import helper_generate_order_without_order_id
from tests.webserver_tests.test_whole_system.helper import helper_generate_order_id
from tests.webserver_tests.test_whole_system.helper import helper_generate_ticker
from tests.webserver_tests.test_whole_system.helper import helper_generate_top_of_book

from lib_webserver.webserver import Webserver
from lib_datetime import datetime_to_order_board_display_string
from lib_datetime import set_use_fake_now_implementation
from lib_datetime.fake_datetime import set_current_datetime

from limit_order_book_webserver.get_webserver_instance import get_webserver_instance

from datetime import datetime
from datetime import timezone


client = TestClient(app)

current_datetime = datetime(
    year=2024, month=1, day=1,
    hour=9, minute=30, second=0,
    tzinfo=timezone.utc,
)
set_current_datetime(current_datetime_value=current_datetime)
set_use_fake_now_implementation(True)

webserver = Webserver(
    use_fake_webserver=False,
    event_log_disabled=True,
)

def override_get_webserver_instance():
    return webserver

app.dependency_overrides[get_webserver_instance] = override_get_webserver_instance


def test_top_of_book():

    json = helper_generate_ticker('PYTH')
    response = client.post('/api/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', None, None, None, None)

    json = helper_generate_order_without_order_id('PYTH', 'BUY', 1000, 10)
    response = client.post('/api/send_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 1,
        'trades': [],
    }

    json = helper_generate_ticker('PYTH')
    response = client.post('/api/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 10, None, None)

    json = helper_generate_order_without_order_id('PYTH', 'SELL', 1025, 15)
    response = client.post('/api/send_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 2,
        'trades': [],
    }

    json = helper_generate_ticker('PYTH')
    response = client.post('/api/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', 1000, 10, 1025, 15)

    json = helper_generate_order_id(1)
    response = client.post('/api/cancel_order', json=json)
    assert response.status_code == 200
    assert response.json() == {
        'status': 'success',
        'message': 'order id 1 cancelled',
        'order': {
            'order_id': 1,
            # TODO: wrong datetime format?
            'timestamp': datetime_to_order_board_display_string(current_datetime),
            'ticker': 'PYTH',
            'order_side': 'BUY',
            'price': 1000,
            'volume': 10,
        }
    }

    json = helper_generate_ticker('PYTH')
    response = client.post('/api/top_of_book', json=json)
    assert response.status_code == 200
    assert response.json() == helper_generate_top_of_book('PYTH', None, None, 1025, 15)