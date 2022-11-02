import telebot
import config
import coin_dict
import gas_price
import sqlite3

from telebot import types
from pycoingecko import CoinGeckoAPI

# Connect to Telegram API
try:
    bot = telebot.TeleBot(config.BOT_TOKEN)
except:
    print('Error connect')

# Connect to Coingecko API
cg = CoinGeckoAPI()

# Connect to SQlite3
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# SQlite 
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
	cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
	conn.commit()


# Bot commands
@bot.message_handler(commands=['start', 'help'])
def start(message):
    mess = f'Привіт, <b>{message.from_user.first_name}</b>\n' \
           f'\n' \
           f'Я - <b>CryptoInfoBot</b>, ось команди для взаємодії зі мною: \n' \
           f'\n' \
           f'/start aбо /help - Отримати це повідомлення \n' \
           f'/price - Отримати ціну вибраної криптовалюти \n' \
           f'/gas - Отримати актуальну ціну на газ в мережі ETH \n' \
           f'/alert - Поставити оповіщення про зміну ціни криптовалюти \n'\
           f'/click - Не натискати!!! \n' \
           f'\n' \
           f'\n' \
           f'Адмін - @vakal33 \n' \
           f'\n' \
           f'Підтримати донатом: \n' \
           f'\n' \
           f'ETH | BSC - <code>0xE9239d18E4211f97113AD3aCB8979979Cf0549Ef</code> \n' \
           f'\n' \
           f'TRC20 - <code>TQHZqsDZVyj4KRpZf7789ckBNuN6vABeAu</code>'     
              
    try:
        db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name, user_surname=message.from_user.last_name, username=message.from_user.username) 
    except:
        pass       
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['price'])
def price_comand(message):    

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE')

    mess = bot.send_message(message.chat.id, f'<b>Введіть назву, наприклад "BTC":</b> ', parse_mode='html', reply_markup = markup)
    bot.register_next_step_handler(mess, price_function)

 

def price_function(message):
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
        bot.send_message(message.chat.id, mess, parse_mode='html')
        return price_comand(message)
    else:    
        bot.send_message(message.chat.id, f'Gavno xyle, try again xyle... 💩 ', parse_mode='html')
        return price_comand(message)

@bot.message_handler(commands=['gas'])
def gas(message):
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
                    
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['click'])
def enjoy(message):
    with open('source\gifka_rus.MP4', 'rb') as gif:
        bot.send_video(message.chat.id, gif)



@bot.message_handler(commands=['alert'])
def alert(message):
    bot.send_message(message.chat.id, 'Команда в розробці <3')



bot.polling(none_stop=True)