import asyncio
import logging
import requests
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, F, types


TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'
OPENWEATHERMAP_API_KEY = 'OPENWEATHERMAP_API_KEY'


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


def get_weather(city_name):
    base_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey={OPENWEATHERMAP_API_KEY}"
    params = {
        'q': city_name,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


# Обработчик для команды /start
@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который сообщает погоду. Введите название города, чтобы узнать погоду.")



# Обработчик текстовых сообщений
@dp.message()
async def send_weather(message: types.Message):
    city_name = message.text
    weather_data = get_weather(city_name)

    if weather_data:
        city = weather_data['name']
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']

        await message.reply(f"Погода в {city}: {temp}°C, {description.capitalize()}.")
    else:
        await message.reply(
            "Не удалось получить данные о погоде. Пожалуйста, убедитесь, что вы ввели правильное название города.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
















