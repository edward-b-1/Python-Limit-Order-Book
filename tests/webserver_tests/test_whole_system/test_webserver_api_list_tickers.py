
from fastapi import FastAPI
from fastapi import status
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.exceptions import DuplicateOrderIdError

from lib_webserver.webserver import Webserver

from tests.webserver_tests.test_whole_system.helper import helper_generate_order_without_order_id
from tests.webserver_tests.test_whole_system.helper import helper_generate_order_id
from tests.webserver_tests.test_whole_system.helper import helper_generate_ticker
from tests.webserver_tests.test_whole_system.helper import helper_generate_top_of_book

from limit_order_book_webserver.get_webserver_instance import get_webserver_instance

# client = TestClient(app)

webserver_without_event_log = Webserver(use_fake_webserver=False, event_log_disabled=True)

def override_get_webserver_instance():
    return webserver_without_event_log

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

