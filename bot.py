import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import BOT_TOKEN
from get_weather import get_weather, get_weather_now, get_weather_tomorrow
from data_base import write_to_table, read_to_table


kb = [
    [types.KeyboardButton(text='Узнать погоду⛅')],
    [types.KeyboardButton(text="Справочник по боту🗒")]
      ]

kb_interval = [
        [types.KeyboardButton(text='Сегодня'),
         types.KeyboardButton(text='Завтра')],
        [types.KeyboardButton(text='10 дней')]
        ]


dp = Dispatcher()


@dp.message(CommandStart())
@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer('Что будем делать❓',reply_markup=keyboard)


@dp.message(Command('help'))
@dp.message(F.text == 'Справочник по боту🗒')
async def help_bot(message: Message):
    await message.answer(f'Бот создан для получения данных\n'
                          'о погоде в вашем регионе 🗺️\n'
                          'Для начала работы с ботом\n'
                          'вызовите команду /start\n'
                          'Для получения точных данных\n'
                          'укажите свое местоположение📍 /location\n\n'
                          'Все данные взяты с сайта яндекс погода\n'
                          'https://yandex.ru/pogoda/', reply_markup=types.ReplyKeyboardRemove())


@dp.message(Command("weather"))
@dp.message(F.text == 'Узнать погоду⛅')
async def weather_in_city(message: Message):
    keybord = types.ReplyKeyboardMarkup(keyboard=kb_interval, resize_keyboard=True)
    await message.answer('Промежуток времени🕑', reply_markup=keybord)


@dp.message(F.text == 'Сегодня')
async def time_interval(message: Message):
    text = get_weather_now(message.from_user.id)
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text == 'Завтра')
async def time_interval(message: Message):
    text = get_weather_tomorrow(message.from_user.id)
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text == '10 дней')
async def time_interval(message: Message):
    text = get_weather(message.from_user.id)
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())


@dp.message(Command('location'))
async def location_users(message: Message):
    kb_location = [[types.KeyboardButton(text="Запросить геолокацию📍", request_location=True)]]
    keybord = types.ReplyKeyboardMarkup(keyboard=kb_location, resize_keyboard=True)
    # read_to_table(message.from_user.id)
    await message.answer('Поделиться местоположением❓', reply_markup=keybord)


@dp.message()
async def handler_location(message: Message):
    lat = message.location.latitude     # широта
    lon = message.location.longitude    # долгота
    id = message.from_user.id
    name = message.from_user.full_name
    # name = 1
    write_to_table(id, lat, lon, name)
    await message.answer('Местоположение успешно получено!', reply_markup=types.ReplyKeyboardRemove())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=BOT_TOKEN)
    
    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
