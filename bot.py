import sys
import asyncio
import logging
import requests
from config import BOT_TOKEN

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tg_bot.models.set_bot_commands import set_default_commands
from tg_bot.models.notify_admins import on_startup_notify

from tg_bot.handlers.users.start_cmd import register_start
from tg_bot.handlers.users.help_cmd import register_help
from tg_bot.handlers.users.get_price import register_get_price


# Setup logger
logger = logging.getLogger('')
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
sh.setFormatter(formatter)
logger.addHandler(sh)

# def register_all_middlewares(dp):
#     pass 

# def register_all_filters(dp):
#     pass

def register_all_handlers(dp): 
    register_start(dp)
    register_help(dp)
    register_get_price(dp)


async def on_startup(dp):
    await on_startup_notify(dp)
    await set_default_commands(dp)

async def main():
    # storage = RedisStorage2()
    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    # register_all_middlewares(dp)
    # register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await on_startup(dp)
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.debug(KeyboardInterrupt, SystemExit)