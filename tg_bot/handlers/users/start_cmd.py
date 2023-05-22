from aiogram import types, Dispatcher

async def start_cmd(msg: types.Message):
    await msg.reply("Hello, user!")

def register_start(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])