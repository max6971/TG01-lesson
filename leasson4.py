import asyncio
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery

import keybord_bt as kb



TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()




@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer("загрузка")
    await callback.message.answer(
    "News [перейти по ссылке](https://radiopotok.ru/radio/644)")


@dp.callback_query(F.data == 'audio')
async def audio(callback: CallbackQuery):
    await callback.answer("загрузка")
    await callback.message.answer(
        "Аудио [перейти по ссылке](https://zaycev.net/pages/247665/24766594.shtml")

    @dp.callback_query(F.data == 'video')
    async def video(callback: CallbackQuery):
        await callback.answer("загрузка")
        await callback.message.answer(
            "видео [перейти по ссылке](https://rutube.ru/feeds/top/?utm_source=insightpeople&utm_medium=cpa&utm_term=5493983196&utm_content=16507883648_mk_top&utm_campaign=perf_insight_mk_top_idk40&yclid=1433738268242083839")
@dp.message(Command('links'))
async def links(message: Message):
    await message.answer('Мои возможности', reply_markup=kb.inline_keyboard_test)

'''@dp.message(F.data == 'показать больше')
async def bolshe(message: Message):
    await message.answer('И еще', reply_markup=await kb.test_keyboard())

@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer('И еще немножко', reply_markup=kb.inline_keyboard_dynamic)
'''
@dp.message(Command('links'))
async def send_welcome(message: Message):
    keyboard = InlineKeyboardMarkup.add(
        InlineKeyboardButton(text="Показать больше", callback_data='show_more')
    )
    await message.reply("Выберите опцию:", reply_markup=keyboard)

@dp.callback_query(F.data == 'show_more')
async def process_show_more(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup.add(
        InlineKeyboardButton(text="Опция 1", callback_data='option_1'),
        InlineKeyboardButton(text="Опция 2", callback_data='option_2')
    )
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query(F.data == 'option_1')
async def process_options(callback_query: CallbackQuery):
    option_text = "Вы выбрали " + ("Опцию 1" if callback_query.data == 'option_1' else "Опцию 2")
    await bot.send_message(callback_query.from_user.id, option_text)
    await bot.answer_callback_query(callback_query.id)



@dp.message(F.text == 'Привет.')
async def privet(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}')
    await message.answer('Основные команды: \n /links \n /dynamic ')

@dp.message(F.text == 'Пока.')
async def privet(message: Message):
        await message.answer(f'Досвидания, {message.from_user.first_name}')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет, я бот', reply_markup=kb.main)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
