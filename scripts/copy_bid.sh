#!/bin/bash
# Автоматизация копирования офферов в буфер Android

TEMPLATE_FILE="$HOME/senior-automation-suite/ai_strategy/bidding_templates.txt"
INDEX=$1

if [ -z "$INDEX" ]; then
    echo "Usage: bid [1|2|3]"
    exit 1
fi

# Извлекаем текст шаблона по номеру (между маркерами ТЕМПЛЕЙТ)
TEXT=$(awk -v n="$INDEX" '/# ТЕМПЛЕЙТ/ {count++} count==n && !/# ТЕМПЛЕЙТ/ {print}' "$TEMPLATE_FILE" | sed '/^$/d' | tr -d '"')

if [ -n "$TEXT" ]; then
    echo "$TEXT" | termux-clipboard-set
    echo "[-] Шаблон #$INDEX скопирован в буфер."
else
    echo "[!] Шаблон не найден."
fi
