# syntax=docker/dockerfile:1

from python:3.12-bookworm
workdir /python-limit-order-book
copy . .
run pip3 install -r requirements.txt
env FASTAPI_PORT=80
entrypoint python3 -m limit_order_book_webserver
expose 80
