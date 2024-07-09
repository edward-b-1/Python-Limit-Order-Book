#!/usr/bin/bash

PROTOCOL=http
#HOST=176.58.122.148
HOST=python-limit-order-book.co.uk
PORT=5555

ENDPOINT='api/modify_order'

curl -X POST "${PROTOCOL}://$HOST:$PORT/$ENDPOINT" \
    -H 'Content-Type: application/json' \
    --data @body.json