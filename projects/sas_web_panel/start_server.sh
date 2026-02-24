#!/bin/bash
cd "$(dirname "$0")"
echo "[+] Стартуем SAS Web Panel на http://127.0.0.1:5000"
while true; do
    python main.py
    echo "[!] Сбой Flask сервера. Авто-рестарт через 2 секунды..."
    sleep 2
done
