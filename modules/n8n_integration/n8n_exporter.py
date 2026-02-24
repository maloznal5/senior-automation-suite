import aiohttp
import os
import logging
from datetime import datetime

# Логирование для защиты в арбитраже
logging.basicConfig(level=logging.INFO, filename='../../logs/app.log', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("N8N_BRIDGE")

# Webhook твоего n8n (можно заменить на продакшн-сервер)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://127.0.0.1:5678/webhook/sas-analytics")

async def export_to_crm(user_id, action_type):
    payload = {
        "user_id": user_id,
        "action": action_type,
        "timestamp": datetime.now().isoformat(),
        "source": "SAS_Enterprise_Monitor"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(N8N_WEBHOOK_URL, json=payload) as resp:
                if resp.status in [200, 201]:
                    logger.info(f"Успешный экспорт в n8n: {action_type}")
                else:
                    logger.error(f"Сбой API n8n: HTTP {resp.status}")
    except Exception as e:
        logger.error(f"Критическая ошибка сети при доступе к n8n: {e}")
