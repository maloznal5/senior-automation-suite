import os
import telebot
from dotenv import load_dotenv

# Загружаем конфиг из корня сюиты
env_path = os.path.expanduser('~/senior-automation-suite/.env')
load_dotenv(env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

def run_test():
    if not BOT_TOKEN or not ADMIN_ID:
        print("[!] ОШИБКА: Переменные в .env не найдены.")
        return

    bot = telebot.TeleBot(BOT_TOKEN)
    try:
        msg = "✅ **SAS Heartbeat**\nСвязь установлена. Система видит владельца."
        bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
        print(f"[-] Сообщение отправлено на ID: {ADMIN_ID}")
    except Exception as e:
        print(f"[!] Ошибка Telegram API: {e}")

if __name__ == "__main__":
    run_test()
