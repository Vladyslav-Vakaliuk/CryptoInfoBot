import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

from tg_bot.models.notify_admins import on_startup_notify
from tg_bot.models.set_bot_commands import set_default_commands

from tg_bot.handlers.users.start import register_start

logger = logging.getLogger(__name__)

storage = MemoryStorage()

def register_all_handlers(dp):
    register_start(dp)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        filename="logger.log"
    )

    logger.info("Starting bot")
    print("[INFO] Starting Bot")

    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    register_all_handlers(dp)

    # start
    try:
        await set_default_commands(dp)
        await on_startup_notify(dp)
        await dp.start_polling()
    except:
        logger.error("Something get wrong!")
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error(f"Bot stopped! Error: {KeyboardInterrupt} {SystemExit}")
        print("[INFO] Bot stopped")