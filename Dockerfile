# syntax=docker/dockerfile:1

from python:3.12-bookworm
workdir /python-limit-order-book
copy ./lib_datetime ./lib_datetime
copy ./lib_financial_exchange ./lib_financial_exchange
copy ./lib_webserver ./lib_webserver
copy ./limit_order_book ./limit_order_book
copy ./limit_order_book_webserver ./limit_order_book_webserver
copy ./requirements.txt .
run pip3 install --no-cache-dir --upgrade -r requirements.txt
env FASTAPI_PORT=5555
#entrypoint python3 -m limit_order_book_webserver
cmd ["python3", "-m", "limit_order_book_webserver"]
#cmd ["python3", "-m", "limit_order_book_webserver", "--proxy-headers", "--forwarded-allow-ips='*'"]
expose 5555
