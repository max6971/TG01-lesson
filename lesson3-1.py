import asyncio
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
import sqlite3




TELEGRAM_BOT_TOKEN = '7352103454:AAESnRPqmUN7jgghs9Llt07fahbnAJgdHEk'
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()
def init_db():
    conn =sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISIS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL)''')
    conn.commit()
    conn.close()

#init_db()
@dp.message(CommandStart())
async def start(messege: Message, state: FSMContext):
    await messege.answer(" Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(messege: Message, state: FSMContext):
    await state.update_data(name=messege.text)
    await messege.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(messege: Message, state: FSMContext):
    await state.update_data(age=messege.text)
    await messege.answer("В каком ты классе?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(messege: Message, state: FSMContext):
    await state.update_data(grade=messege.text)
    user_data = await state.get_data()
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INFO(name, age, grade) VALUES(?, ?, ?)''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()


    await state.clear()
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
