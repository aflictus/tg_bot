from aiogram import types, Dispatcher
from keyboards.client_kb import kb_start
from data_base.sql_db import telegram_id, tax_data


async def start(message: types.Message):
    user = list(telegram_id())
    if (str(message.from_user.id), ) in user:
        await message.answer("Hello!", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("We are glad to see you again!")
        await message.answer("Every first day of the month, I notify you about the payment of tax.")

    else:
        await message.answer("Hello!")
        await message.answer("I am a bot that will help you register in the Iolipay system.")
        await message.answer("Have you sign up to Ioliply?", reply_markup=kb_start)


async def help(message: types.Message):
    await message.answer("That's bot...\nSupport: @BotFather")


def handlers_bot(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help, commands=["help"])

