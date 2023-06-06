from aiogram import types, Dispatcher

async def start_cmd(msg: types.Message):
    await msg.reply(f"Привіт, <b>{msg.from_user.first_name}</b>\n"
           f"\n"
           f"Я - <b>CryptoKitty</b>, ось, що я вмію: \n"
           f"\n"
           f"Дізнатися ціну бітка або будь якої іншої монети")

def register_start(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])