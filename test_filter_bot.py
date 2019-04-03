import math
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from bs4 import BeautifulSoup
import re


TOKEN = '889443907:AAHUP8IQRoNQ4fWXuIpd5mML-fBwbRaANuM'


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def message_handler(msg: types.Message):
	info = 'Съешь еще этих мягких французских булок, да выпей чаю'
	await bot.send_message(msg.from_user.id, info)

if __name__ == '__main__':
    executor.start_polling(dp)