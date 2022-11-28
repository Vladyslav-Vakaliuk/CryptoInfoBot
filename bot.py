import logging
import threading
import time

import gas_price
import database

from config import BOT_TOKEN
from screenshots import make_screen_bubbles

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from pycoingecko import CoinGeckoAPI
from urllib.request import urlopen

logging.basicConfig(filename='logs.log', level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


# Connect to database
database.db_connect()

# Connect to Telegram API 
try:
    bot = Bot(token=BOT_TOKEN)
except:
    pass

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

cg = CoinGeckoAPI()

class  ProfileStatesGroup(StatesGroup):
    coin = State()


def bubbles_update():
    while True:
        make_screen_bubbles()
        time.sleep(1800)


@dp.message_handler(commands=['start', 'help'], state='*')
async def start(message: types.Message, state: FSMContext):
    mess = f'Привіт, <b>{message.from_user.first_name}</b>\n' \
           f'\n' \
           f'Я - <b>CryptoInfoBot</b>, ось, що я вмію: \n' \
           f'\n' \
           f'Дізнатися ціну бітка або будь якої іншої монети:\n' \
           f'\n' \
           f'Просто напиши мені "BTC" або будь яку іншу криптовалюту і ти отримаєш ціну 💥\n' \
           f'\n' \
           f'Також я маю ще кілька команд:\n' \
           f'\n' \
           f'/start aбо /help - Отримати це повідомлення \n' \
           f'/gas - Отримати актуальну ціну на газ в мережі ETH \n' \
           f'/index - Дізнатися індекс страху та жадібності \n' \
           f'/bubbles - Зміна цін топ 100 криптовалют за 24 години \n'\
           f'\n' \
           f'\n' \
           f'Адмін - @vakal33 \n' \
           f'\n' \
           f'Підтримати донатом: \n' \
           f'\n' \
           f'ETH | BSC - <code>0xE9239d18E4211f97113AD3aCB8979979Cf0549Ef</code> \n' \
           f'\n' \
           f'TRC20 - <code>TQHZqsDZVyj4KRpZf7789ckBNuN6vABeAu</code>' 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'DOT', 'APT', 'NEAR', 'AVAX', 'TRX')   

    try:
        database.db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, username=message.from_user.username) 
    except:
        pass     
                    
    if state is None:
        return

    await bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    await ProfileStatesGroup.coin.set()


@dp.message_handler(commands=['gas'], state='*')
async def gas(message: types.Message, state: FSMContext):
    gas_price.gas_func()
    link = 'https://etherscan.io/gastracker'
    mess = f'<b>Актуальна ціна газу ⛽:</b> \n' \
          f'\n' \
          f'🔥 Low ~ {gas_price.low} GWEI\n' \
          f'--------------------------------------\n' \
          f'💥 Avarege ~ {gas_price.avarege} GWEI\n' \
          f'---------------------------------------\n' \
          f'🧨 Hight ~ {gas_price.hight} GWEI\n' \
          f'\n' \
          f'<b>Інформація з:</b> {link}'
    await bot.send_message(message.chat.id, mess, disable_web_page_preview = True, parse_mode='html')

    if state is None:
        return

    await ProfileStatesGroup.coin.set()

@dp.message_handler(commands=['index'], state='*')
async def index(message: types.Message, state: FSMContext):
    url = 'https://alternative.me/crypto/fear-and-greed-index.png'
    image = (urlopen(url))
    
    mess = f'<b>Інформація з:</b> {url}' 

    await bot.send_photo(message.chat.id, photo=image, parse_mode='html')
    await bot.send_message(message.chat.id, mess, disable_web_page_preview = True, parse_mode='html')

    if state is None:
        return

    await ProfileStatesGroup.coin.set()

@dp.message_handler(commands=['bubbles'], state='*')
async def bubbles(message: types.Message, state: FSMContext):  
    with open('source/bubbles.png', 'rb') as img:
        await bot.send_photo(message.chat.id, img)

    url = 'https://cryptobubbles.net/'
    mess = f'<b>Інформація з:</b> {url}' 
    await bot.send_message(message.chat.id, mess, disable_web_page_preview = True, parse_mode='html')

    if state is None:
        return

    await ProfileStatesGroup.coin.set()

@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.coin)
async def price(message: types.Message, state: FSMContext):
    crypto_id = message.text.lower()
    database.find_id(symbol=crypto_id)
    database.find_name(symbol=crypto_id)
    coin = database.coin
    name = database.name

    price_response = cg.get_price(ids=coin, vs_currencies='usd', include_24hr_change='true')
    usd_24h_change = round(price_response[coin]['usd_24h_change'], 2) 
    link = cg.get_coin_by_id(id=coin)

    price = price_response[coin]['usd']
    link = link['links']['homepage'][0]

    if usd_24h_change < 0:
        mess = f'💰 <b>{name} ({crypto_id})</b> 🔥\n' \
               f'---------------------------------- \n' \
               f'📍 <b>Ціна</b> ~ {price} 💲\n' \
               f'---------------------------------- \n' \
               f'📌 <b>24 H:</b> {usd_24h_change} % 📊\n' \
               f'---------------------------------- \n' \
               f'🔗 <a href="{link}">Офіційний сайт</a> ℹ️'

        await bot.send_message(message.chat.id, mess, disable_web_page_preview = True, parse_mode='html')
    else: 
        mess = f'💰 <b>{name} ({crypto_id})</b> 🔥\n' \
               f'---------------------------------- \n' \
               f'📍 <b>Ціна</b> ~ {price} 💲\n' \
               f'---------------------------------- \n' \
               f'📌 <b>24 H:</b> +{usd_24h_change} % 📊\n' \
               f'---------------------------------- \n' \
               f'🔗 <a href="{link}">Офіційний сайт</a> ℹ️' 

        await bot.send_message(message.chat.id, mess, disable_web_page_preview = True, parse_mode='html')


if __name__ == '__main__':
    threading.Thread(target = bubbles_update).start()
    executor.start_polling(dp, skip_updates=True)   
