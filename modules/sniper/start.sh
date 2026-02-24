#!/bin/bash
cd "$(dirname "$0")"
while true; do
    python main.py
    echo "[] Снайпер упал. Рестарт через 5 сек..." >> ../../logs/app.log
    sleep 5
done
