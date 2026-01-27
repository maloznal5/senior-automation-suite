# -*- coding: utf-8 -*-
import asyncio, logging, os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)

load_dotenv()
API = os.getenv("BOT_TOKEN")
ADM = 470455594

bot = Bot(token=API)
dp = Dispatcher()

class Form(StatesGroup):
    n, s, p, t = State(), State(), State(), State()
    chat = State()
    reply_state = State()

def main_kb(uid):
    btns = [
        [KeyboardButton(text="Записатися 📅"), KeyboardButton(text="Ціни 💳")],
        [KeyboardButton(text="Рекомендації догляду 🧴"), KeyboardButton(text="Догляд після ✨")],
        [KeyboardButton(text="Написати майстру 💬"), KeyboardButton(text="Контакти 📞")],
        [KeyboardButton(text="Приклади робіт ✨")]
    ]
    if uid == ADM: btns.append([KeyboardButton(text="Заявки (Адмін) 🛠")])
    return ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)

def cancel_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Головне меню 🏠")]], resize_keyboard=True)

@dp.message(F.text.in_({"/start", "Головне меню 🏠"}))
async def cmd_start(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("✨ **LeraKeratin Assistant**", reply_markup=main_kb(m.from_user.id))

@dp.message(F.text == "Написати майстру 💬")
async def start_chat_with_admin(m: Message, state: FSMContext):
    await m.answer("📝 **Напишіть ваше запитання майстру:**", reply_markup=cancel_kb())
    await state.set_state(Form.chat)

@dp.message(Form.chat)
async def forward_to_admin(m: Message, state: FSMContext):
    if m.text == "Головне меню 🏠": return await cmd_start(m, state)
    admin_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Відповісти ✍️", callback_data=f"ans_{m.from_user.id}")]])
    await bot.send_message(ADM, f"📩 **НОВЕ ПОВІДОМЛЕННЯ**\n\n👤 Від: {m.from_user.full_name}\n🆔 ID: `{m.from_user.id}`\n💬: {m.text}", reply_markup=admin_kb)
    await m.answer("✅ **Повідомлення надіслано!**", reply_markup=main_kb(m.from_user.id))
    await state.clear()

@dp.callback_query(F.data.startswith("ans_"))
async def start_reply(clb: CallbackQuery, state: FSMContext):
    target_id = clb.data.split("_")[1]
    await state.update_data(reply_to=target_id)
    await clb.message.answer(f"✍️ **Відповідь для ID {target_id}:**", reply_markup=cancel_kb())
    await state.set_state(Form.reply_state)
    await clb.answer()

@dp.message(Form.reply_state)
async def send_reply_to_user(m: Message, state: FSMContext):
    if m.text == "Головне меню 🏠": return await cmd_start(m, state)
    data = await state.get_data()
    try:
        await bot.send_message(data.get("reply_to"), f"💌 **Відповідь від майстра:**\n\n{m.text}")
        await m.answer("✅ Відправлено!", reply_markup=main_kb(m.from_user.id))
    except Exception as e: await m.answer(f"❌ Помилка: {e}")
    await state.clear()

@dp.message(F.text == "Ціни 💳")
async def send_prices(m: Message):
    await m.answer("✨ **𝐏𝐑𝐈𝐂𝐄 𝐋𝐈𝐒𝐓** ✨\n(Кератин, Ботокс, Відновлення)\nПовний прайс у майстра.")

@dp.message(F.text == "Контакти 📞")
async def send_contacts(m: Message):
    ikb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Instagram 📸", url="https://www.instagram.com/leraa.keratin")]])
    await m.answer("📍 **КОНТАКТИ**\n\n👤 Майстер: Лера\n✈️ @leriiiiiiiik", reply_markup=ikb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
