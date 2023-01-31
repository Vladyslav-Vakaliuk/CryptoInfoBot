import logging

from aiogram import Dispatcher
from config import ADMINS

async def get_admins_id():
    admins_list = []
    admins_list.append(ADMINS)
    return admins_list
    
# Notify all admins when bot started
async def on_startup_notify(dp: Dispatcher):
    for admin in await get_admins_id():
        try:
            await dp.bot.send_message(chat_id=admin, text="Bot, Started")
        except Exception as err:
            logging.error(err)