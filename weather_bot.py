from config import TOKEN, OPEN_WHEATHER_TOKEN
import datetime
import requests
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.reply('Привет! Пришли мне название города, где хочешь узнать погоду')


@dp.message_handler(commands=['weather'])
async def get_weather(message: Message):
    try:
        city = 'saint petersburg'
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WHEATHER_TOKEN}&units=metric')
        data = r.json()
        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        day_length = sunset - sunrise
        await message.reply(f'****{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}****\n'
                            f'Погода в городе {city}:\n'
                            f'Температура: {cur_weather}°C\n' 
                            f'Влажность: {humidity}%\n'
                            f'Давление: {pressure} мм.рт.ст.\n'
                            f'Скорость ветра: {wind_speed} м/с\n'
                            f'Время восхода: {sunrise}\n'
                            f'Время заката: {sunset}\n'
                            f'Продолжительность дня: {day_length}')
    except:
        await message.reply('Проверьте название города')


if __name__ == '__main__':
    executor.start_polling(dp)
