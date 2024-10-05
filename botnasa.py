import asyncio
import random
import requests
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery
from config import TOKEN, NASA_API_KEY
import keybord_bt as kb
from datetime import datetime, timedelta
from googletrans import Translator


TELEGRAM_BOT_TOKEN = TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

translator = Translator()


@dp.message(Command('photo_earth'))
async def photo_earth(message: Message):

    url_earth = ('https://epic.gsfc.nasa.gov/archive/natural/2024/10/03/jpg/epic_1b_20241003015633.jpg')
    await message.answer_photo(photo=url_earth)



def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date+(end_date - start_date)*random.random()
    date_str = random_date.strftime("%Y-%m-%d")
    url = (f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}')
    response = requests.get(url)
    return response.json()


@dp.message(Command('space_photo'))
async def space_photo(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']
    translated = translator.translate(title, src='en', dest='ru')
    await message.answer_photo(photo=photo_url, caption=f"{translated}\n")




@dp.message(F.text == 'Привет.')
async def privet(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}')
    await message.answer('Основные команды: \n /space_photo \n /photo_earth')

@dp.message(F.text == 'Пока.')
async def privet(message: Message):
        await message.answer(f'Досвидания, {message.from_user.first_name}')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет,{message.from_user.first_name} я бот', reply_markup=kb.main)




async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())