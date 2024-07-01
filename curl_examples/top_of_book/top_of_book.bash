#!/usr/bin/bash

IP_ADDRESS=176.58.122.148
PORT=80

ENDPOINT='top_of_book'

curl -X GET "http://$IP_ADDRESS:$PORT/$ENDPOINT" \
    -H 'Content-Type: application/json' \
    --data @body.json
