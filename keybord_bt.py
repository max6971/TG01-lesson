from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет.")],
    [KeyboardButton(text="Пока.")]
],resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="новости", callback_data='news' )],
    [InlineKeyboardButton(text="аудео",  callback_data='audio')],
    [InlineKeyboardButton(text="видео",  callback_data='video')]
])

inline_keyboard_dynamic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="показать больше", callback_data='news' )]
    ])




test = ["Опция 1", "Опция 2"]
async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   for key in test:
       keyboard.add(InlineKeyboardButton(text=key))
   return keyboard.adjust(2).as_markup()