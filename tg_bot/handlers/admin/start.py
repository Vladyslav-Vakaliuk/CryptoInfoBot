from aiogram import types, Dispatcher

async def admin_start(msg: types.Message):
    text = "Hello, Admin!"

    await msg.reply(text)