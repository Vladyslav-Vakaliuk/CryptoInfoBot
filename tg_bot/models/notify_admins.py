from aiogram import Dispatcher
from config import ADMINS

async def get_admins_id():
    admins_list = [int(x) for x in ADMINS.split(',')]
    return admins_list
    
# Notify all admins when bot started
async def on_startup_notify(dp: Dispatcher):
    for admin in await get_admins_id():
        try:
            await dp.bot.send_message(chat_id=admin, text="Bot, Started")
        except Exception as err:
            pass