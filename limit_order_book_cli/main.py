# import os
# print(os.environ['PYTHONPATH'])

from limit_order_book.types import OrderId
from limit_order_book.types import Ticker
from limit_order_book.types import OrderSide
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.types import Order
from limit_order_book.types import OrderWithoutOrderId

import typer
import requests
import json

app = typer.Typer()

#base_url = f'http://127.0.0.1:5000'
#base_url = f'http://127.0.0.1:80'
#base_url = f'http://172.17.0.1:80'
#base_url = f'http://176.58.122.148:80'
base_url = f'http://python-limit-order-book.co.uk:5555'
# 172.17.0.1

def get_url(endpoint):
    return f'{base_url}{endpoint}'


@app.command()
def send_order(ticker: str, order_side: str, price: int, volume: int):
    order = OrderWithoutOrderId(
        ticker=Ticker(ticker),
        order_side=OrderSide(order_side),
        int_price=IntPrice(price),
        volume=Volume(volume),
    )
    print(f'/api/send_order')
    print(order)

    url = get_url('/api/send_order')
    headers = {
        'accept': 'application/json',
    }
    data = {
        'ticker': ticker,
        'order_side': order_side,
        'price': price,
        'volume': volume,
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.request.method)
    print(response.request.headers)
    print(response.request.body)
    print(f'Status: {response.status_code}')
    response_dict = response.json()
    response_dict_json = json.dumps(response_dict, indent=4)
    print(f'{response_dict_json}')


# @app.command()
# def send_order_fixed_order_id(order_id: int, ticker: str, order_side: str, price: int, volume: int):
#     order = Order(
#         order_id=OrderId(order_id),
#         ticker=Ticker(ticker),
#         order_side=OrderSide(order_side),
#         int_price=IntPrice(price),
#         volume=Volume(volume),
#     )
#     print(f'/api/send_order')
#     print(order)

#     url = get_url('/api/send_order')
#     headers = {
#         'accept': 'application/json',
#     }
#     data = {
#         'order_id': order_id,
#         'ticker': ticker,
#         'order_side': order_side,
#         'price': price,
#         'volume': volume,
#     }
#     response = requests.post(url, headers=headers, json=data)
#     print(response.request.method)
#     print(response.request.headers)
#     print(response.request.body)
#     print(f'Status: {response.status_code}')
#     response_dict = response.json()
#     response_dict_json = json.dumps(response_dict, indent=4)
#     print(f'{response_dict_json}')


@app.command()
def modify_order(order_id: int, price: int, volume: int):
    print(f'/api/modify_order')
    print(f'{order_id}, {price}, {volume}')

    url = get_url('/api/modify_order')
    headers = {
        'accept': 'application/json',
    }
    data = {
        'order_id': order_id,
        'price': price,
        'volume': volume,
    }
    response = requests.post(url, headers=headers, json=data)
    print(f'Status: {response.status_code}')
    response_dict = response.json()
    response_dict_json = json.dumps(response_dict, indent=4)
    print(f'{response_dict_json}')


@app.command()
def cancel_order(order_id: int):
    order_id_order_id = OrderId(order_id)
    print(f'/api/cancel_order')
    print(order_id_order_id)

    url = get_url('/api/cancel_order')
    headers = {
        'accept': 'application/json',
    }
    data = {
        'order_id': order_id,
    }
    response = requests.post(url, headers=headers, json=data)
    print(f'Status: {response.status_code}')
    response_dict = response.json()
    response_dict_json = json.dumps(response_dict, indent=4)
    print(f'{response_dict_json}')


@app.command()
def top_of_book(ticker: str):
    ticker_ticker = Ticker(ticker)
    print(f'/api/top_of_book')
    print(ticker_ticker)

    url = get_url('/api/top_of_book')
    headers = {
        'accept': 'application/json',
    }
    data = {
        'ticker': ticker,
    }
    response = requests.post(url, headers=headers, json=data)
    print(f'Status: {response.status_code}')
    response_dict = response.json()
    response_dict_json = json.dumps(response_dict, indent=4)
    print(f'{response_dict_json}')


@app.command()
def ping():
    print(f'/api/debug/ping')
    url = get_url('/api/debug/ping')
    headers = {
        'accept': 'application/json',
    }
    response = requests.get(url, headers=headers)
    print(f'Status: {response.status_code}')
    response_dict = response.json()
    response_dict_json = json.dumps(response_dict, indent=4)
    print(f'{response_dict_json}')


@app.command()
def debug_log_top_of_book(ticker: str):
    print(f'/api/debug/debug_log_top_of_book')
    print(ticker)
    url = get_url('/api/debug/debug_log_top_of_book')
    headers = {
        'accept': 'application/json',
    }
    data = {
        'ticker': ticker,
    }
    response = requests.post(url, headers=headers, json=data)
    print(f'Status: {response.status_code}')
    response_dict = response.json()
    response_dict_json = json.dumps(response_dict, indent=4)
    print(f'{response_dict_json}')


@app.command()
def debug_log_current_order_id():
    print(f'/api/debug/debug_log_current_order_id')
    url = get_url('/api/debug/debug_log_current_order_id')
    headers = {
        'accept': 'application/json',
    }
    response = requests.post(url, headers=headers)
    print(f'Status: {response.status_code}')
    response_dict = response.json()
    response_dict_json = json.dumps(response_dict, indent=4)
    print(f'{response_dict_json}')


@app.command()
def debug_log_all_tickers():
    print(f'/api/debug/debug_log_all_tickers')
    url = get_url('/api/debug/debug_log_all_tickers')
    headers = {
        'accept': 'application/json',
    }
    response = requests.post(url, headers=headers)
    print(f'Status: {response.status_code}')
    response_dict = response.json()
    response_dict_json = json.dumps(response_dict, indent=4)
    print(f'{response_dict_json}')

