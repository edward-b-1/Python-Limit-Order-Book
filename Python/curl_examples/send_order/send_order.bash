#!/usr/bin/bash

IP_ADDRESS=176.58.122.148
PORT=80

ENDPOINT='api/send_order'

curl -X POST "http://$IP_ADDRESS:$PORT/$ENDPOINT" \
    -H 'Content-Type: application/json' \
    --data @body.json
