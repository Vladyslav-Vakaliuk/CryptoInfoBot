from aiogram import types, Dispatcher
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

async def get_price(msg: types.Message):
    crypto_id = msg.text
    price = cg.get_price(ids=crypto_id, vs_currencies='usd')

    if price:
        price = price[crypto_id.lower()]['usd']
    else:
        await msg.answer("Crypto was not found")
        return

    await msg.answer(f"Price of {crypto_id}={price}")

def register_get_price(dp: Dispatcher):
    dp.register_message_handler(get_price)