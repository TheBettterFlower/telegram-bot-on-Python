import requests
import datetime

from aiogram.client.session.aiohttp import AiohttpSession

from config import bot_token, pogoda_token
from aiogram import Bot, types, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import asyncio
import logging
from aiogram import F


logging.basicConfig(level=logging.INFO)
# Объект бота
session = AiohttpSession(proxy="http://proxy.server:3128/")
bot = Bot(token=bot_token, session=session)
# Диспетчер
dp = Dispatcher()

kb = [
        [
            types.KeyboardButton(text="ГЕОЛОКАЦИЯ"),
        ]
    ]
keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# Хэндлер на команду /start
@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.delete()
    await message.answer(f'Привет, {message.from_user.first_name}! '
                                               'Я помогу вам узнать подробную информацию '
                                               'о погодных условиях в вашем или '
                        'любом другом населенном пункте \U00002600')


@dp.message()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождливо \U00002614',
        'Drizzle': 'Дождливо \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={pogoda_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = ' '

        humidity = data['main']['humidity']
        presure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        await message.reply(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}'
              f'Погода: {city}\nТемпература: {int(cur_weather)}C° {wd}\n'
              f'Влажность: {humidity}%\nДавление: {presure} мм.рт.ст\nВетер: {wind} м/c\n'
              f'Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n'
              f'Продолжительность дня: {length_of_the_day}\n'
              f'Температура ожидается от {int(temp_min)}C° до {int(temp_max)}C°\n'
              f'Хорошего дня!')
    except:
        await message.reply('\U00002620 Попробуйте снова \U00002620')

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



