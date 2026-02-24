#!/bin/bash
ROOT="$HOME/senior-automation-suite/projects/sas_monitor_bot/src"

# Обновляем конфиг (добавляем URL твоего n8n)
echo 'N8N_WEBHOOK_URL="http://твой-ip:5678/webhook/sas-report"' >> $ROOT/config.py

# Обновляем основной файл (добавляем aiohttp для отправки вебхуков)
cat << 'EOT' > $ROOT/n8n_exporter.py
import aiohttp
import json
import logging
from config import N8N_WEBHOOK_URL

logger = logging.getLogger("SAS_MONITOR")

async def send_to_n8n(user_id, action, timestamp):
    if "твой-ip" in N8N_WEBHOOK_URL: return # Заглушка, пока не впишешь реальный URL
    
    payload = {
        "user_id": user_id,
        "action": action,
        "timestamp": timestamp,
        "source": "SAS_Enterprise_Bot"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_WEBHOOK_URL, json=payload) as resp:
                if resp.status == 200:
                    logger.info("Data successfully exported to n8n")
    except Exception as e:
        logger.error(f"n8n Export Error: {e}")
EOT

pip install aiohttp --quiet
echo "[-] Модуль экспорта в n8n готов. Отредактируй config.py, вставив реальный Webhook URL."
