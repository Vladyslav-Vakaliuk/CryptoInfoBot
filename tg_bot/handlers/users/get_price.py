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
    command_args = msg.text.split()
    crypto_name = command_args[1]
    amount = float(command_args[0])
    coin_id = get_coin_id(crypto_name.lower())
    price = cg.get_price(ids=coin_id, vs_currencies='usd')

    if price:
        price = price[coin_id.lower()]['usd']
        total_price = int(price) * amount
    else:
        await msg.answer("Crypto was not found")
        return

    await msg.answer(f"💰 <b>{crypto_name} ({coin_id})</b> 🔥\n📈 <b>Ціна</b>~{total_price}💲")


def register_get_price(dp: Dispatcher):
    dp.register_message_handler(get_price)
