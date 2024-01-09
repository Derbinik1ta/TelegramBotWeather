import requests
import json
from googletrans import Translator
from datetime import datetime
from datetime import timedelta
from config import cookies, headers, params
from data_base import read_to_table


translator = Translator()

weather_dict = {
    'легкий дождь': '🌧',
    'дождь': '🌧',
    'пасмурная погода': '☁️',
    'пасмурно': '☁️',
    'снег': '❄',
    'ясно': '☀'
}


def write_to_json(information, filename):
    with open(f'weather data/{filename}.json', 'w') as file:
        json.dump(information, file, indent=4, ensure_ascii=False)


def read_to_json(filename):
    with open(f'weather data/{filename}.json', 'r') as file:
        json.loads(file)


# параметр запроса
# def params_config(lat, lon):
#     global params
#     params = {
#     'lat': '45.00975',
#     'lon': '39.099838',
#     'page': 'main',
#     'day': '',
#     'ta_features': 'favorites;sgn',
#     'turboapp': '1',
# }
    
    
# запрашиваем json файл 
def response_weather(id_users):
    global lat, lon
    lat, lon = read_to_table(id_users)
    
    response = requests.get('https://yandex.ru/pogoda/', params=params, cookies=cookies, headers=headers)
    print(f'Статус код запроса: {response.status_code}')
    global response_result_later, response_result_now
    if response.status_code == 200:
        response_json = response.json()
        response_result_now = response_json.get('data').get('fact')
        response_result_later = response_json.get('data').get('forecasts')
        write_to_json(response_result_now, '1_now_information')
        write_to_json(response_result_later, '2_later_information')
    else:
        print(f'Не могу получить информацию о погоде с сайта🤒')
        response_result_now = read_to_json('1_now_information')
        response_result_later = read_to_json('1_now_information')
        
        
# получаем эмодзи
def validator_emodji(condition):
    global emodji_weather
    try:
        emodji_weather = weather_dict[condition]
    except:
        emodji_weather = ''


# узнать погоду сегодня
def get_weather_now(id_users):
    # write_to_json(response_result, '1_all_information')
    # print(response_result.get('condition'))
    response_weather(id_users)

    condition = translator.translate(response_result_now.get('condition'), dest='ru').text
    if condition =='прозрачный':
        condition = 'ясно'
    validator_emodji(condition)
    return f'Сейчас🗓️: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\nТемпература воздуха🌡: {response_result_now.get('temp')}℃\nСостояние погоды: {condition} {emodji_weather}\nВлажность воздуха💧: {response_result_now.get('pressure_mm')} г/м³\nСкорость ветра💨: {response_result_now.get('wind_speed')} м/с'


# узнать погоду завтра
def get_weather_tomorrow(id_users):  
    response_result = response_weather(id_users)

    condition = translator.translate(response_result_later[1].get('parts').get('day').get('condition'), dest='ru').text
    if condition =='прозрачный':
        condition = 'ясно'
    validator_emodji(condition)

    date_now = datetime.now()
    date_tomorrow = date_now + timedelta(days=1)
    return f'Завтра🗓️: {date_tomorrow.strftime('%d.%m.%Y')}\n\nТемпература воздуха🌡: {response_result_later[1].get('parts').get('day').get('temp_avg')}℃\nСостояние погоды: {condition} {emodji_weather}\nВлажность воздуха💧: {response_result_later[1].get('parts').get('day').get('pressure_mm')} г/м³\nСкорость ветра💨: {response_result_later[1].get('parts').get('day').get('wind_speed')} м/с'


# узнать погоду на 10 дней
def get_weather(id_users):
    response_result = response_weather(id_users)

    condition = translator.translate(response_result_later[1].get('parts').get('day').get('condition'), dest='ru').text
    if condition =='прозрачный':
            condition = 'ясно'
    validator_emodji(condition)

    date_now = datetime.now()
    result_weather = f'Дата🗓️: {date_now.strftime('%d.%m.%Y')}\n\nТемпература воздуха🌡: {response_result_later[0].get('parts').get('day').get('temp_avg')}℃\nСостояние погоды: {condition} {emodji_weather}\nВлажность воздуха💧: {response_result_later[0].get('parts').get('day').get('pressure_mm')} г/м³\nСкорость ветра💨: {response_result_later[0].get('parts').get('day').get('wind_speed')} м/с\n\n\n'
    for i in range(1, 10):
        condition = translator.translate(response_result_later[i].get('parts').get('day').get('condition'), dest='ru').text
        if condition =='прозрачный':
            condition = 'ясно'
        validator_emodji(condition)

        
        date_of_the_week = date_now + timedelta(days=i)
        result_weather += f'Дата🗓️: {date_of_the_week.strftime('%d.%m.%Y')}\n\nТемпература воздуха🌡: {response_result_later[i].get('parts').get('day').get('temp_avg')}℃\nСостояние погоды: {condition} {emodji_weather}\nВлажность воздуха💧: {response_result_later[i].get('parts').get('day').get('pressure_mm')} г/м³\nСкорость ветра💨: {response_result_later[i].get('parts').get('day').get('wind_speed')} м/с\n\n\n'
    return result_weather


def main():
    get_weather_now(135246)
    # get_weather_tomorrow()
    # get_weather()

if __name__ == '__main__':
    main()
