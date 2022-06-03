#!/bin/bash

rm -f /tmp/ep2/online/*

python3 server/main.py 3000 &
echo "in vini 123"| python3 client/main.py localhost 3000 udp &
echo "in francisco 123\ncall vini" | python3 client/main.py localhost 3000 tcp &
