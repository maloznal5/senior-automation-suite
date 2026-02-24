#!/bin/bash
ROOT="$HOME/senior-automation-suite"
BOT_PATH="$ROOT/projects/sas_monitor_bot"

# 1. Перезапись основного файла без psutil
cat << 'EOT' > $BOT_PATH/src/main.py
import asyncio
import subprocess
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from config import BOT_TOKEN, ADMIN_ID
from utils.logger import setup_logger

logger = setup_logger()
bot = AsyncTeleBot(BOT_TOKEN)

def get_sys_info():
    # Нативный мониторинг Linux (без внешних библиотек)
    try:
        storage = subprocess.getoutput("df -h . | awk 'NR==2 {print $4}'")
        processes = subprocess.getoutput("ps -e | wc -l").strip()
        return f"💾 Свободно в Termux: {storage} | ⚙️ Процессов: {processes}"
    except Exception as e:
        logger.error(f"System info error: {e}")
        return "💻 Мониторинг ресурсов ограничен"

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
        await bot.edit_message_text(
            f"📊 **Системные показатели:**\n{get_sys_info()}", 
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=main_menu(), 
            parse_mode="Markdown"
        )
    elif call.data == "mon":
        await bot.answer_callback_query(call.id, "Мониторинг запущен")
        await bot.edit_message_text(
            "🚀 **Статус:** Мониторинг сети и парсеров активен.", 
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=main_menu(), 
            parse_mode="Markdown"
        )
    else:
        await bot.answer_callback_query(call.id, "Действие принято")

async def main():
    logger.info("SAS Bot is starting without psutil...")
    print("[-] Система в сети. Жду команд в Telegram.")
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())
EOT

# 2. Фиксация в GitHub
cd $ROOT
git add .
git commit -m "fix: replace psutil with native subprocess for Termux compatibility"
git push origin main

# 3. Мгновенный запуск
cd $BOT_PATH/src
python main.py
