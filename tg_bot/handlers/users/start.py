from config import ADMINS

from aiogram import types, Dispatcher
from tg_bot.handlers.admin.start import admin_start

async def cmd_start(msg: types.Message):
    if msg.from_user.id == int(ADMINS):
        await admin_start(msg)
    else:
        text = "Hello, User"  
                           
        await msg.answer(text, parse_mode="HTML")

def register_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])