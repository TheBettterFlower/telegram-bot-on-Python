import datetime

import requests
from config import pogoda_token
from pprint import pprint


def get_w(city, pogoda_token):
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
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={pogoda_token}&units=metric'
        )
        data = r.json()
        #pprint(data)

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            print(' ')

        humidity = data['main']['humidity']
        presure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}'
              f'Погода: {city}\nТемпература: {int(cur_weather)}C° {wd}\n'
              f'Влажность: {humidity}%\nДавление: {presure} мм.рт.ст\nВетер: {wind} м/c\n'
              f'Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n'
              f'Продолжительность дня: {length_of_the_day}\nТемпаратура ожидается от {temp_min} до {temp_max}\n'
              f'Хорошего дня!')
    except Exception as ex:
        print(ex)
        print('Попробуйте снова')


def main():
    city = input('Введите название: ')
    get_w(city, pogoda_token)


if __name__ == '__main__':
    main()