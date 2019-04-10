import math
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from bs4 import BeautifulSoup
import re
from user_agent import generate_user_agent, generate_navigator


TOKEN = '889443907:AAHUP8IQRoNQ4fWXuIpd5mML-fBwbRaANuM'

prices = {}
brands = {}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_top_items(brand=None, price=None):
    url = "https://www.mvideo.ru/noutbuki-planshety-komputery/noutbuki-118/f/"

    if brand:
        brands = str(brand[0])
        for b in brand[1:]:
            brands = brands + ',' + str(b)
        url = url + 'brand=' + brands + '/'

    if price:
        url = url + 'price=from-' + price[0] + '-to-' + price[1]

    r = requests.get(
    url, headers=generate_navigator())

    soup = BeautifulSoup(r.text, "html.parser")
    
    try:
	    img = soup.find(
	        'div', class_="c-product-tile").find('img')['data-original'][2:]
	    item_price = soup.find('div',
	    class_="c-product-tile").find('div',
	    class_='c-pdp-price__current').text.replace('\xa0',
	    '').replace('\t',
	    '').replace('\n',
	    '').replace(' ',
	     '')
	    href = soup.find('div', class_="c-product-tile").find('a')['href']
	    href = "https://www.mvideo.ru" + href
	    return img, href, item_price
    except BaseException:
	    return str(url + '\n' + soup)


@dp.message_handler(commands=['start'], commands_prefix='!/')
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nДавай выберем тебе ноутбук!")

@dp.message_handler(commands=['help'], commands_prefix='!/')
async def process_help_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Давай выберем тебе ноутбук \n \
    	/price -- напиши минимальную и максимальную цены через пробел \n \
    	/brand -- напиши через пробел производителей из данного списка: Apple, Acer, Asus, HP, Lenovo \n \
    	/items -- по данной команде бот выдаст тебе товары")

@dp.message_handler(commands=['price'], commands_prefix='!/')
async def process_price_command(message: types.Message):
	global prices
	prices[message.chat.id] = message.text.split()

@dp.message_handler(commands=['brand'], commands_prefix='!/')
async def process_brand_command(message: types.Message):
	global brands
	brands[message.chat.id] = message.text.split()

@dp.message_handler(commands=['items'], commands_prefix='!/')
async def process_items_command(message: types.Message):
	global brands
	global prices
	
	chat_brands = 'b'
	chat_prices = 'p'
	
	try:
		chat_brands = brands[message.chat.id]
	except BaseException:
		pass
	
	try:
		chat_prices = prices[message.chat.id]
	except BaseException:
		pass
	
	img_url, href, item_price = get_top_items(chat_brands[1:], chat_prices[1:])

	tell_price = 'Цена на данный ноутбук составляет ' + item_price[:-1] + 'рублей'
	await bot.send_photo(message.chat.id, types.InputFile.from_url(img_url))
	await bot.send_message(message.from_user.id, tell_price)
	await bot.send_message(message.from_user.id, href)



@dp.message_handler()
async def message_handler(message: types.Message):
	info = 'Я не чат-бот, извини. Задай, пожалуйста, параметры ноутбука.'
	await bot.send_message(message.from_user.id, info)

if __name__ == '__main__':
    executor.start_polling(dp)
