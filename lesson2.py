import asyncio
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, types, F
from googletrans import Translator

import random


TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

translator = Translator()

@dp.message()
async def translate_message(message: types.Message):
    original_text = message.text
    translated = translator.translate(original_text, src='ru', dest='en')
    await message.reply(translated.text)


@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://https://appleinsider.ru/wp-content/uploads/2023/03/spring_wallpapper_paris-750x1623.jpg', 'https://appleinsider.ru/wp-content/uploads/2023/03/spring_wallpapper_rose_tree-750x1333.jpg', 'https://appleinsider.ru/wp-content/uploads/2023/03/spring_wallpapper_tree_2-750x1623.jpg','https://appleinsider.ru/wp-content/uploads/2023/03/spring_wallpapper_ipad_macbook-750x422.jpg','https://appleinsider.ru/wp-content/uploads/2023/03/spring_wallpapper_tree_3-750x1623.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='фото для тебя')


@dp.message(F.photo)
async def react_foto(message: Message):
    list = ['Ничё себе!', 'Как это возможно!','Ух ты!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "Привет")
async def aitext(message: Message):
    await message.answer('Привет, пользователь телеграмма')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Основные команды: \n /start \n /help')


@dp.message(CommandStart)
async def start(message: Message):
        await message.answer('Привет, я бот.')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

