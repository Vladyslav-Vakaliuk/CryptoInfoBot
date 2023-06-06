from aiogram import types, Dispatcher

async def help_cmd(msg: types.Message):
    await msg.reply(f'Я - <b>CryptoKitty</b>, ось, що я вмію:\n'
                    f'\n'
                    f'Дізнатися ціну бітка або будь якої іншої монети\n'
                    f'\n'
                    f'Просто напиши мені яка в тебе крипта і скільки\n'
                    f'\n'
                    f'Наприклад: 1 BTC, 0.3 BTC, 3 BTC, 2ETH')


def register_help(dp: Dispatcher):
    dp.register_message_handler(help_cmd, commands=['help'])