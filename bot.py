# -*- coding: utf-8 -*-
import asyncio, logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)

API = "8261425012:AAGd3kctchDce-93DyrGLgpUHRqKx7wglWE"
ADM = 470455594

bot = Bot(token=API)
dp = Dispatcher()

class Form(StatesGroup):
    n, s, p, t = State(), State(), State(), State()
    chat = State()        # Клиент пишет мастеру
    reply_state = State() # Мастер отвечает клиенту

def log_order(data):
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(f"{data}\n")

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

# --- КЛИЕНТ ПИШЕТ МАСТЕРУ ---
@dp.message(F.text == "Написати майстру 💬")
async def start_chat_with_admin(m: Message, state: FSMContext):
    await m.answer("📝 **Напишіть ваше запитання майстру:**", reply_markup=cancel_kb())
    await state.set_state(Form.chat)

@dp.message(Form.chat)
async def forward_to_admin(m: Message, state: FSMContext):
    if m.text == "Головне меню 🏠": return await cmd_start(m, state)
    
    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Відповісти ✍️", callback_data=f"ans_{m.from_user.id}")]
    ])
    await bot.send_message(ADM, f"📩 **НОВЕ ПОВІДОМЛЕННЯ**\n\n👤 Від: {m.from_user.full_name}\n🆔 ID: `{m.from_user.id}`\n💬: {m.text}", reply_markup=admin_kb)
    await m.answer("✅ **Повідомлення надіслано!** Майстер скоро відповість.", reply_markup=main_kb(m.from_user.id))
    await state.clear()

# --- МАСТЕР ОТВЕЧАЕТ КЛИЕНТУ ---
@dp.callback_query(F.data.startswith("ans_"))
async def start_reply(clb: CallbackQuery, state: FSMContext):
    target_id = clb.data.split("_")[1]
    await state.update_data(reply_to=target_id)
    await clb.message.answer(f"✍️ **Введіть відповідь для клієнта (ID: {target_id}):**", reply_markup=cancel_kb())
    await state.set_state(Form.reply_state)
    await clb.answer()

@dp.message(Form.reply_state)
async def send_reply_to_user(m: Message, state: FSMContext):
    if m.text == "Головне меню 🏠": return await cmd_start(m, state)
    
    data = await state.get_data()
    target_id = data.get("reply_to")
    
    try:
        await bot.send_message(target_id, f"💌 **Відповідь від майстра:**\n\n{m.text}")
        await m.answer("✅ Відповідь надіслана клієнту!", reply_markup=main_kb(m.from_user.id))
    except Exception as e:
        await m.answer(f"❌ Помилка при надсиланні: {e}")
    
    await state.clear()

# --- ОСТАЛЬНЫЕ ФУНКЦИИ БЕЗ ИЗМЕНЕНИЙ ---
@dp.message(F.text == "Ціни 💳")
async def send_prices(m: Message):
    text = (
        "✨ **𝐏𝐑𝐈𝐂𝐄 𝐋𝐈𝐒𝐓** ✨\n"
        "──────────────────\n"
        "❄️ **ХОЛОДНЕ ВІДНОВЛЕННЯ**\n"
        "▫️ 20-30 см — 1150 ₴ | 31-40 см — 1300 ₴\n"
        "▫️ 41-50 см — 1450 ₴ | 51-60 см — 1600 ₴\n"
        "▫️ 61-70 см — 1750 ₴ | 71-80 см — 1900 ₴\n\n"
        "🔥 **КЕРАТИН | БОТОКС**\n"
        "▫️ 30-40 см — 1350 ₴ | 41-50 см — 1600 ₴\n"
        "▫️ 51-60 см — 1900 ₴ | 61-70 см — 2500 ₴\n"
        "▫️ 71-80 см — 3000 ₴\n\n"
        "💎 **ТОТАЛЬНА РЕКОНСТРУКЦІЯ**\n"
        "▫️ 30-40 см — 2100 ₴ | 41-50 см — 2600 ₴\n"
        "▫️ 51-60 см — 3000 ₴ | 61-70 см — 3700 ₴\n"
        "▫️ 71-80 см — 4200 ₴\n\n"
        "➕ **ДОДАТКОВО:**\n"
        "▫️ Густота: 9см (400₴), 10-11см (600₴), 12см+ (700-900₴)\n"
        "▫️ Пористе волосся: 300-600 ₴\n"
        "▫️ Нарощене: 1200 ₴ | Пілінг: 600 ₴\n"
        "▫️ Доплата за складність (плутання): 300 ₴\n"
        "──────────────────\n"
        "🎁 **Стрижка кінців у ПОДАРУНОК!**"
    )
    await m.answer(text, parse_mode="Markdown")

@dp.message(F.text == "Контакти 📞")
async def send_contacts(m: Message):
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Instagram 📸", url="https://www.instagram.com/leraa.keratin")],
        [InlineKeyboardButton(text="Telegram Майстра 💌", url="https://t.me/leriiiiiiiik")]
    ])
    text = "📍 **КОНТАКТИ**\n\n👤 Майстер: Лера\n📞 Тел: +380 (93) 232 59 91\n✈️ Telegram: @leriiiiiiiik"
    await m.answer(text, reply_markup=ikb, parse_mode="Markdown")

@dp.message(F.text == "Заявки (Адмін) 🛠")
async def view_orders(m: Message):
    if m.from_user.id != ADM: return
    try:
        with open("orders.txt", "r", encoding="utf-8") as f:
            data = f.read()
        await m.answer(f"📋 **ВСІ ЗАЯВКИ:**\n\n{data if data else 'Порожньо'}")
    except: await m.answer("📁 Файл не знайдено.")

@dp.message(F.text == "Записатися 📅")
async def ask_name(m: Message, state: FSMContext):
    await m.answer("👤 **Ваше ім'я?**", reply_markup=cancel_kb())
    await state.set_state(Form.n)

@dp.message(Form.n)
async def ask_service(m: Message, state: FSMContext):
    if m.text == "Головне меню 🏠": return await cmd_start(m, state)
    await state.update_data(n=m.text)
    await m.answer("💇 **Яка процедура та довжина?**", reply_markup=cancel_kb())
    await state.set_state(Form.s)

@dp.message(Form.s)
async def ask_photo(m: Message, state: FSMContext):
    if m.text == "Головне меню 🏠": return await cmd_start(m, state)
    await state.update_data(s=m.text)
    await m.answer("📸 **Надішліть фото волосся (ззаду)**", reply_markup=cancel_kb())
    await state.set_state(Form.p)

@dp.message(Form.p, F.photo)
async def ask_time(m: Message, state: FSMContext):
    await state.update_data(p=m.photo[-1].file_id)
    await m.answer("🕒 **Бажана дата і час?**", reply_markup=cancel_kb())
    await state.set_state(Form.t)

@dp.message(Form.t)
async def finish_order(m: Message, state: FSMContext):
    if m.text == "Головне меню 🏠": return await cmd_start(m, state)
    d = await state.get_data()
    uid = m.from_user.id
    log_order(f"Клієнт: {d['n']} | Послуга: {d['s']} | Час: {m.text}")
    
    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Підтвердити", callback_data=f"conf_{uid}"),
         InlineKeyboardButton(text="❌ Відхилити", callback_data=f"reje_{uid}")]
    ])
    caption = f"🆕 **НОВА ЗАЯВКА**\n👤 Клієнт: {d['n']}\n💇 Послуга: {d['s']}\n🕒 Час: {m.text}\n🆔 ID: {uid}"
    await bot.send_photo(ADM, d['p'], caption=caption, reply_markup=admin_kb)
    await m.answer("✅ **Надіслано!** Майстер відповість вам.", reply_markup=main_kb(uid))
    await state.clear()

@dp.callback_query(F.data.startswith("conf_"))
async def conf(clb: CallbackQuery):
    await bot.send_message(clb.data.split("_")[1], "🎉 **Запис підтверджено!**")
    await clb.message.edit_caption(caption=clb.message.caption + "\n✅ ПІДТВЕРДЖЕНО")

@dp.callback_query(F.data.startswith("reje_"))
async def reje(clb: CallbackQuery):
    await bot.send_message(clb.data.split("_")[1], "❌ **Час зайнятий.** Майстер зв'яжеться з вами.")
    await clb.message.edit_caption(caption=clb.message.caption + "\n❌ ВІДХИЛЕНО")

@dp.message(F.text == "Рекомендації догляду 🧴")
async def care_rec(m: Message):
    text = "🧴 **Рекомендації:** Deeply, Moroccan Argan Oil. Скраб 1/міс, маска 1/тижд. Детальніше у майстра."
    await m.answer(text)

@dp.message(F.text == "Догляд після ✨")
async def care_after(m: Message):
    await m.answer("🧼 **ПРАВИЛА:** Безсульфатний шампунь, сушка феном на 100%, кондиціонер.")

@dp.message(F.text == "Приклади робіт ✨")
async def works(m: Message):
    await m.answer("📸 Instagram: https://www.instagram.com/leraa.keratin")

async def main(): await dp.start_polling(bot)
if __name__ == "__main__": asyncio.run(main())
