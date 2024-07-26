
from fastapi.testclient import TestClient

from limit_order_book_webserver.fastapi_webserver import app

from tests.webserver_tests.test_whole_system.helper import helper_generate_order_without_order_id
from tests.webserver_tests.test_whole_system.helper import helper_generate_order_id

from lib_webserver.webserver import Webserver
from lib_webserver.webserver import WebserverImplementationMode

from lib_datetime import DatetimeStrategy
from lib_datetime import datetime_to_order_board_display_string

from limit_order_book_webserver.get_webserver_instance import get_webserver_instance
from lib_datetime.get_datetime_strategy import get_datetime_strategy

from datetime import datetime
from datetime import timezone


client = TestClient(app)

current_datetime = datetime(
    year=2024, month=1, day=1,
    hour=9, minute=30, second=0,
    tzinfo=timezone.utc,
)
# datetime_strategy = DatetimeStrategy(test_mode=True, current_datetime=current_datetime)

# def override_get_datetime_strategy():
#     print(f'get_datetime_strategy(): (override_get_datetime_strategy()) returning the FAKE datetime strategy')
#     return datetime_strategy

# app.dependency_overrides[get_datetime_strategy] = override_get_datetime_strategy

webserver = Webserver(
    webserver_implementation_mode=WebserverImplementationMode.WITH_FAKE_DATETIME_PROXY,
    event_log_disabled=True,
)
webserver._webserver.set_datetime(timestamp=current_datetime) # TODO cleanup

def override_get_webserver_instance():
    return webserver

app.dependency_overrides[get_webserver_instance] = override_get_webserver_instance


# TODO: this test is trying to test the internal logic via the FastAPI webserver interface
# it is a legitimate test, but not really testing the FastAPI webserver paths by themselves
def test_order_trade():

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
    print(response.json()['trades'][0])
    assert response.json() == {
        'status': 'success',
        'message': None,
        'order_id': 2,
        'trades': [
            {
                'trade_id': 1,
                'timestamp': datetime_to_order_board_display_string(current_datetime),
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
    print(response.json())
    print(response.json()['order'])
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
            'volume': 5,
        }
    }
