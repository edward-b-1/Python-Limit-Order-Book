
from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.exceptions import DuplicateOrderIdError

from lib_webserver.webserver import Webserver
from lib_datetime.fake_datetime import now as now_fake
from lib_datetime.fake_datetime import set_current_datetime

from tests.webserver_tests.test_whole_system.helper import helper_generate_order_without_order_id
from tests.webserver_tests.test_whole_system.helper import helper_generate_order_id
from tests.webserver_tests.test_whole_system.helper import helper_generate_ticker
from tests.webserver_tests.test_whole_system.helper import helper_generate_top_of_book

from limit_order_book_webserver.get_webserver_instance import get_webserver_instance
from lib_datetime.get_now_function import get_now_function

from datetime import datetime
from datetime import timezone

# client = TestClient(app)

current_datetime = datetime(
    year=2024, month=1, day=1,
    hour=9, minute=30, second=0,
    tzinfo=timezone.utc,
)
set_current_datetime(current_datetime_value=current_datetime)
now = now_fake

webserver_without_event_log = Webserver(
    use_fake_webserver=False,
    event_log_disabled=True,
)

def override_get_now_function():
    print(f'override_get_now_function(): returning the FAKE now function')
    print(f'now=')
    print(now)
    print(now())
    return now

def override_get_webserver_instance():
    return webserver_without_event_log

app.dependency_overrides[get_now_function] = override_get_now_function
app.dependency_overrides[get_webserver_instance] = override_get_webserver_instance


def test_list_all_tickers():

    with TestClient(app) as client:
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

