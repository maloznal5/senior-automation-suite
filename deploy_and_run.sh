#!/bin/bash
# SAS Enterprise Deployer: Полная перезапись и запуск

ROOT="$HOME/senior-automation-suite"
BOT_PATH="$ROOT/projects/sas_monitor_bot"

# 1. Исправление и создание структуры
mkdir -p $BOT_PATH/src/utils
mkdir -p $ROOT/logs

# 2. Обновление .env (Центральный конфиг)
cat << 'EOT' > $ROOT/.env
BOT_TOKEN="8780387143:AAEovV_r-tD8oggABGgUo-f93jduMz0r78g"
ADMIN_ID="8335925220"
EOT
cp $ROOT/.env $BOT_PATH/.env

# 3. Файл логгера (Enterprise logging)
cat << 'EOT' > $BOT_PATH/src/utils/logger.py
import logging
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("SAS_MONITOR")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler("logs/bot_core.log")
        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | [%(levelname)s] | %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger
EOT

# 4. Файл конфигурации
cat << 'EOT' > $BOT_PATH/src/config.py
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else 0
EOT

# 5. Основной файл бота (Premium UI)
cat << 'EOT' > $BOT_PATH/src/main.py
import asyncio
import os
import psutil
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from config import BOT_TOKEN, ADMIN_ID
from utils.logger import setup_logger

logger = setup_logger()
bot = AsyncTeleBot(BOT_TOKEN)

def get_sys_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"💻 CPU: {cpu}% | RAM: {ram}%"

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 Мониторинг", callback_data="mon"),
        types.InlineKeyboardButton("📈 Статус системы", callback_data="sys"),
        types.InlineKeyboardButton("📂 Логи", callback_data="logs"),
        types.InlineKeyboardButton("❌ Стоп", callback_data="stop")
    )
    return markup

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    if message.from_user.id != ADMIN_ID: return
    await bot.send_message(
        message.chat.id, 
        f"🛡 **SAS ENTERPRISE SYSTEM**\n{get_sys_info()}\n\nВыберите модуль управления:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
async def handle_query(call):
    if call.data == "sys":
        await bot.answer_callback_query(call.id, "Обновление данных...")
        await bot.edit_message_text(f"📊 **Системные показатели:**\n{get_sys_info()}", call.message.chat.id, call.message.message_id, reply_markup=main_menu(), parse_mode="Markdown")
    else:
        await bot.answer_callback_query(call.id, "Команда принята")

async def main():
    logger.info("SAS Bot is starting...")
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())
EOT

# 6. Установка зависимостей и пуш в GitHub
pip install pyTelegramBotAPI python-dotenv psutil --quiet
cd $ROOT
git add .
git commit -m "feat: finalize enterprise bot architecture and auto-run"
git push origin main

# 7. ЗАПУСК
echo "[-] Деплой завершен. ЗАПУСК БОТА..."
cd $BOT_PATH/src
python main.py
