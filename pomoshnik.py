import asyncio
import random
import sqlite3
from aiogram. fsm. context import FSMContext
from aiogram.fsm import state
from aiogram.fsm.state import State, StatesGroup
import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F

from aiogram import Bot, Dispatcher

from config import TOKEN
import aiohttp
import logging

TELEGRAM_BOT_TOKEN = TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
button_registr = KeyboardButton(text="Регистрация")
button_exchange_rates = KeyboardButton(text="Курс валют")
button_tips = KeyboardButton(text="Советы по Экономии")
button_finaces = KeyboardButton(text="Финансы")

keyboards = ReplyKeyboardMarkup(keyboard=[
    [button_registr, button_exchange_rates],
    [button_tips, button_finaces]
    ], resize_keyboard=True)
conn = sqlite3.connect('user.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL
    )
    ''')
conn.commit()

class FinacesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()

@dp.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/3bc6898375376e0042843423/latest/USD" # 3bc6898375376e0042843423
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("упс, нет данных")
            return
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']

        eur_to_rub = usd_to_rub/eur_to_usd

        await message.answer(f" USD - {usd_to_rub:.2f} руб\n"
                             f" EUR - {eur_to_rub:.2f} руб")



    except:
        await message.answer("упс, ошибка соединения")

@dp.message(F.text == 'Регистрация')
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cursor.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
    user = cursor.fetchone()
    if user:
        await message.answer(" ВЫ уже зарегестрировались")
    else:
        cursor.execute('''INSERT INTO users (telegram_id, name) VALUES(?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer(" Вы успешно зарегестрировались.")

@dp.message(F.text == "Советы по Экономии")
async def send_tips(message: Message):
    tips = [
        "Хорошо подумай, перед покупкой.",
        "В магазин за продуктами не ходи голодным. ",
        "Это точно тебе нужно?",
        "Ты уже отложил часть денег на черный день?",
        "Сегодня есть скидки на нужные товары? Есть - идем за покупками. Нет - подождем."
    ]
    tip = random.choice(tips)
    await message.answer(tip)


@dp.message(F.text == "Финансы")
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinacesForm.category1)
    await message.reply("Введите первую категорию расходов.")
@dp.message(FinacesForm.category1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category1 = message.text)
    await state.set_state(FinacesForm.expenses1)
    await message.reply(f"Введите расходы для категории {message.text}.")

@dp.message(FinacesForm.expenses1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses1 = float(message.text))
    await state.set_state(FinacesForm.category2)
    await message.reply("Введите Вторую категорию расходов")


@dp.message(FinacesForm.category2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category2 = message.text)
    await state.set_state(FinacesForm.expenses2)
    await message.reply(f"Введите расходы для категории {message.text}.")


@dp.message(FinacesForm.expenses2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses2 = float(message.text))
    await state.set_state(FinacesForm.category3)
    await message.reply("Введите третью категорию расходов")

@dp.message(FinacesForm.category3)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category3 = message.text)
    await state.set_state(FinacesForm.expenses3)
    await message.reply(f"Введите расходы для категории {message.text}.")


@dp.message(FinacesForm.expenses3)
async def finances(message: Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = message.from_user.id
    cursor.execute('''
    UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?,  expenses2 = ?, category3 = ?, expenses3 = ? WHERE telegram_id =?''',
                   (data['category1'], data['expenses1'], data['category2'], data['expenses2'], data['category3'], float(message.text), telegram_id))
    conn.commit()
    await state.clear()

    await message.answer("Данные сохранены")


@dp.message(Command('start'))
async def send_start(message: Message):
    await  message.answer("Hello", reply_markup=keyboards)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())