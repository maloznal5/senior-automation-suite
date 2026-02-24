import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from config import BOT_TOKEN, ADMIN_ID
from utils.logger import setup_logger

logger = setup_logger()
bot = AsyncTeleBot(BOT_TOKEN)

# Интерфейс уровня Senior (Инлайновые кнопки)
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 Запустить мониторинг", callback_data="start_mon"),
        types.InlineKeyboardButton("📊 Статистика API", callback_data="stats"),
        types.InlineKeyboardButton("🛠 Настройки", callback_data="settings"),
        types.InlineKeyboardButton("📄 Логи системы", callback_data="get_logs")
    )
    return markup

@bot.message_handler(commands=['start'])
async def welcome(message):
    if message.from_user.id != ADMIN_ID:
        logger.warning(f"Unauthorized access attempt: {message.from_user.id}")
        return
    
    await bot.send_message(
        message.chat.id, 
        "🛠 **SAS ENTERPRISE MONITOR**\nСистема готова к работе. Выберите действие:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
async def handle_query(call):
    logger.info(f"Action: {call.data} by user {call.from_user.id}")
    if call.data == "start_mon":
        await bot.answer_callback_query(call.id, "Мониторинг запущен")
        await bot.edit_message_text("🚀 **Статус:** Мониторинг активен (1.0s interval)", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "get_logs":
        await bot.answer_callback_query(call.id, "Выгрузка логов...")
        # Логика отправки файла логов
    else:
        await bot.answer_callback_query(call.id, "Функция в разработке")

async def main():
    logger.info("SAS Monitor Bot Started")
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())
