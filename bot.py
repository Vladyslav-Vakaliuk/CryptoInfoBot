import coin_dict
import gas_price
import sqlite3
import time
import threading

from bubbles import make_screen

from sqlite3 import Error

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext

from pycoingecko import CoinGeckoAPI
from config import BOT_TOKEN

from urllib.request import urlopen

# Connect to database
try:
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    print("Database connected successfully")
except Error as e:
        print(f"The error '{e}' occurred")

conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                user_id INTEGER UNIQUE NOT NULL,
                user_name TEXT INTEGER NOT NULL,
                user_surname TEXT,
                username STRING TEXT,
                alert TEXT DEFAULT "none"
            );  """)
            

async def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
	cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
	conn.commit()

# Connect to Telegram API 
try:
    bot = Bot(token=BOT_TOKEN)
    print("Bot connected successfully")
except:
    print("Error to cennect API telegram")

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

cg = CoinGeckoAPI()

class  ProfileStatesGroup(StatesGroup):
    gas = State()


def bubbles_update():
    while True:
        make_screen()
        time.sleep(3600)


@dp.message_handler(commands=['start', 'help'], state='*')
async def start(message: types.Message, state: FSMContext):
    mess = f'Привіт, <b>{message.from_user.first_name}</b>\n' \
           f'\n' \
           f'Я - <b>CryptoInfoBot</b>, ось, що я вмію: \n' \
           f'\n' \
           f'Основна функція, це курс криптовалюти:\n' \
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
           f'Якщо ви не знайшли якийсь токен, просто напишіть мені і я одразу його додам 👌\n' \
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
        await db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, username=message.from_user.username) 
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
    await bot.send_message(message.chat.id, mess, parse_mode='html')

    if state is None:
        return

    await ProfileStatesGroup.coin.set()

@dp.message_handler(commands=['index'], state='*')
async def index(message: types.Message, state: FSMContext):
    url = 'https://alternative.me/crypto/fear-and-greed-index.png'
    image = (urlopen(url))
    
    await bot.send_photo(message.chat.id, photo=image, parse_mode='html')

    if state is None:
        return

    await ProfileStatesGroup.coin.set()

@dp.message_handler(commands=['bubbles'], state='*')
async def bubbles(message: types.Message, state: FSMContext):  
    with open('bubbles.png', 'rb') as img:
        await bot.send_photo(message.chat.id, img)

    if state is None:
        return

    await ProfileStatesGroup.coin.set()

@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.coin)
async def price(message: types.Message, state: FSMContext):
    crypto_id = message.text.lower()
    key = crypto_id
    if key in coin_dict.coin_list:
        crypto_name = coin_dict.coin_list.get(key)
        price_response = cg.get_price(ids=crypto_name, vs_currencies='usd', include_24hr_change='true')
        main_currency = 'usd'
        price = price_response[crypto_name][main_currency]
        usd_24h_change = price_response[crypto_name]['usd_24h_change']
        usd_24h_change = round(usd_24h_change, 2)
        mess = f'💰 <b>{crypto_id.upper()}</b> 🔥\n' \
            f'---------------------------------- \n' \
            f'📍 <b>Ціна</b> ~ {price} 💲\n' \
            f'---------------------------------- \n' \
            f'📌 <b>24 H:</b> {usd_24h_change} % 📊'  
        await bot.send_message(message.chat.id, mess, parse_mode='html')




if __name__ == '__main__':
    threading.Thread(target = bubbles_update).start()
    executor.start_polling(dp, skip_updates=True)   
