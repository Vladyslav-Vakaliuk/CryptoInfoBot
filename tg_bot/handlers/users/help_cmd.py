from aiogram import types, Dispatcher

async def help_cmd(msg: types.Message):
    await msg.reply("How i can help you?")

def register_help(dp: Dispatcher):
    dp.register_message_handler(help_cmd, commands=['help'])