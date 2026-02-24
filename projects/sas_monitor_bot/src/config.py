import os
from dotenv import load_dotenv

load_dotenv(os.path.expanduser('~/senior-automation-suite/.env'))

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
LOG_FILE = "logs/bot_core.log"
