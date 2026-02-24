#!/bin/bash
# Интеграция aiosqlite и модуля аналитики

ROOT="$HOME/senior-automation-suite"
BOT_PATH="$ROOT/projects/sas_monitor_bot"
SRC_PATH="$BOT_PATH/src"

mkdir -p $SRC_PATH/database

# 1. Ядро Базы Данных (database/db_core.py)
cat << 'EOT' > $SRC_PATH/database/db_core.py
import aiosqlite
import os
import csv
from utils.logger import setup_logger

logger = setup_logger()
DB_PATH = "database/analytics.db"

async def init_db():
    os.makedirs("database", exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()
    logger.info("Database initialized.")

async def log_action(user_id: int, action: str):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('INSERT INTO user_actions (user_id, action) VALUES (?, ?)', (user_id, action))
            await db.commit()
    except Exception as e:
        logger.error(f"DB Log Error: {e}")

async def export_csv(filepath: str = "database/report.csv"):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute('SELECT * FROM user_actions ORDER BY timestamp DESC') as cursor:
                rows = await cursor.fetchall()
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Log_ID", "User_ID", "Action", "Timestamp"])
                    writer.writerows(rows)
        return filepath
    except Exception as e:
        logger.error(f"CSV Export Error: {e}")
        return None
EOT

# 2. Обновление основного файла (src/main.py)
cat << 'EOT' > $SRC_PATH/main.py
import asyncio
import subprocess
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from config import BOT_TOKEN, ADMIN_ID
from utils.logger import setup_logger
from database.db_core import init_db, log_action, export_csv

logger = setup_logger()
bot = AsyncTeleBot(BOT_TOKEN)

def get_sys_info():
    try:
        storage = subprocess.getoutput("df -h . | awk 'NR==2 {print $4}'")
        processes = subprocess.getoutput("ps -e | wc -l").strip()
        return f"💾 Свободно: {storage} | ⚙️ Процессов: {processes}"
    except:
        return "💻 Мониторинг ограничен"

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 Мониторинг", callback_data="mon_start"),
        types.InlineKeyboardButton("📈 Статус", callback_data="sys_status"),
        types.InlineKeyboardButton("❌ Стоп", callback_data="mon_stop")
    )
    return markup

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    if message.from_user.id != ADMIN_ID: return
    await log_action(message.from_user.id, "cmd_start")
    await bot.send_message(
        message.chat.id, 
        f"🛡 **SAS ENTERPRISE**\n{get_sys_info()}",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['report'])
async def send_report(message):
    if message.from_user.id != ADMIN_ID: return
    await log_action(message.from_user.id, "cmd_report")
    
    msg = await bot.send_message(message.chat.id, "⏳ Формирование CSV отчета...")
    filepath = await export_csv()
    
    if filepath:
        with open(filepath, 'rb') as doc:
            await bot.send_document(message.chat.id, doc, caption="📊 Аналитика использования системы")
        await bot.delete_message(message.chat.id, msg.message_id)
    else:
        await bot.edit_message_text("❌ Ошибка выгрузки БД", message.chat.id, msg.message_id)

@bot.callback_query_handler(func=lambda call: True)
async def handle_query(call):
    await log_action(call.from_user.id, f"btn_{call.data}")
    
    if call.data == "sys_status":
        await bot.answer_callback_query(call.id)
        await bot.edit_message_text(f"📊 **Системные показатели:**\n{get_sys_info()}", call.message.chat.id, call.message.message_id, reply_markup=main_menu(), parse_mode="Markdown")
    elif call.data == "mon_start":
        await bot.answer_callback_query(call.id, "Мониторинг запущен")
        await bot.edit_message_text("🚀 **Статус:** Активен", call.message.chat.id, call.message.message_id, reply_markup=main_menu(), parse_mode="Markdown")

async def main():
    await init_db()
    logger.info("SAS Bot + Analytics Started")
    print("[-] База данных подключена. Бот в сети.")
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())
EOT

# 3. Установка зависимости и рестарт сессии
pip install aiosqlite --quiet
cd $ROOT
git add .
git commit -m "feat: integrate aiosqlite analytics and csv reporting"
git push origin main

echo "[-] Интеграция завершена. Перезапускаю фоновый процесс tmux..."
tmux kill-session -t sas_bot 2>/dev/null
tmux new-session -d -s sas_bot "cd $SRC_PATH && python main.py"
echo "[-] Готово. Зайди в бота, понажимай кнопки и введи /report"
