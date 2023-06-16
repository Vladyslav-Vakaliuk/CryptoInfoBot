from aiogram import types, Dispatcher
from pycoingecko import CoinGeckoAPI
import json

cg = CoinGeckoAPI()

with open('coins_list.json') as json_file:
    coins_list = json.load(json_file)


def get_coin_id(coin_symbol):
    for coin in coins_list:
        if coin['symbol'] == coin_symbol.lower():
            return coin['id']
    return None


async def get_price(msg: types.Message):
    crypto_space = msg.text.split()
    if len(crypto_space) >= 2: 
        crypto_name = crypto_space[1]
        multiply = float(crypto_space[0])
        coin_id = get_coin_id(crypto_name.lower())
        price = cg.get_price(ids=coin_id, vs_currencies='usd', include_24hr_change="true")
        usd_24h_change = round(price[coin_id]["usd_24h_change"], 2)

        if price:
            price = price[coin_id.lower()]['usd']
            total_price = int(price) * multiply
        else:
            await msg.answer("Crypto was not found")
            return
        
        text = f"💰 <b>{crypto_name.upper()} ({coin_id})</b> 🔥\n" \
               f"\n" \
               f"📈 <b>Ціна за 1 {crypto_name.upper()}:</b>~{price}💲\n"\
               f"\n" \
               f"📈 <b>Ціна за {multiply} {crypto_name.upper()}:</b>~{total_price}💲\n"\
               f"\n" \
               f"📌 <b>24 H:</b> {usd_24h_change} % 📊"

        await msg.answer(text=text, parse_mode="html")

    else:
        crypto_name = crypto_space[0]
        coin_id = get_coin_id(crypto_name.lower())
        price = cg.get_price(ids=coin_id, vs_currencies='usd', include_24hr_change="true")
        usd_24h_change = round(price[coin_id]["usd_24h_change"], 2)

        if price:
                price = price[coin_id.lower()]['usd']
        else:
            await msg.answer("Crypto was not found")
            return


        await msg.answer(
            f'💰 <b>{crypto_name} ({coin_id})</b> 🔥\n📈 <b>Ціна</b>~{price}💲\n📌 <b>24 H:</b> {usd_24h_change} % 📊')


def register_get_price(dp: Dispatcher):
    dp.register_message_handler(get_price)
