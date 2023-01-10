from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.client_kb import  kb_menu, kb_transaction, kb_menu0
from data_base.sql_db import serial_number, all_transaction, sql_add_payment, sql_delete_payment
from sending_machine.admin_sending import admins_notify_payment
from aiogram.dispatcher.filters import Text
from google_sheets.ioli_data import tax_transaction
from create_bot import bot
import re


class Transaction(StatesGroup):
    last_transaction = State()
    date_transaction = State()


async def no_more(message: types.Message):
    await message.answer("Okay. If you didn't do anymore transactions, press the button and pay the tax.", reply_markup=kb_menu)



async def no_transaction(message: types.Message):
    await message.answer("Okay. If you didn't do any transactions, press the button.", reply_markup=kb_menu0)



async def any_transaction(message: types.Message):
    await message.answer("Okay. See you later.", reply_markup=types.ReplyKeyboardRemove())



async def back(message: types.Message):
    await message.answer("What do we do?", reply_markup=kb_transaction)

async def add_transaction(message: types.Message):
    await message.answer("So, write transaction and transaction date, be sure to specify the currency. \nFor example: 1675.88 USD")
    await Transaction.last_transaction.set()

async def transaction(message: types.Message):
    await message.answer("So, write transaction and transaction date, be sure to specify the currency. \nFor example: 1675.88 USD")
    await Transaction.last_transaction.set()


async def stop_handler(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("The process has been stopped!", reply_markup=types.ReplyKeyboardRemove())


async def last(message: types.Message, state=FSMContext):
    regex0 = r'\b[0-9]+\.[0-9]{,2}\s[A-Za-z]{3,3}\b'
    regex1 = r'\b[0-9]+\s[A-Za-z]{3,3}\b'
    if bool(re.fullmatch(regex0, message.text)) or bool(re.fullmatch(regex1, message.text)):
        async with state.proxy() as data:
            data["last_transaction"] = message.text
        await Transaction.next()
        await message.answer("🙈 When was the transaction made?\nFor example DD.MM.YYYY")
    else:
        await message.answer("Format must be: 5432.10 USD")


async def date(message: types.Message, state=FSMContext):
    if re.search(r'(.\d+.\d+.\d+)', message.text):
        async with state.proxy() as data:
            data["date_transaction"] = message.text
        await Transaction.next()
        await message.answer("Good!")
        await sql_add_payment(message.from_user.id, state)
        await message.answer("What we are going to do?", reply_markup=kb_transaction)

    else:
        await message.answer("Format must be: 09.09.2022")


async def report(message: types.Message):
    await message.answer("Okay!")
    await message.answer("Within 5 minutes I will send you a report.", reply_markup=types.ReplyKeyboardRemove())
    id = serial_number(message.from_user.id)
    await admins_notify_payment(*id)
    list0 = all_transaction(message.from_user.id)
    tax_transaction(*list0, *id)
    sql_delete_payment(message.from_user.id)





def handlers_bot(dp: Dispatcher):
    dp.register_message_handler(transaction, lambda message: "✅ Add another transaction" in message.text)
    dp.register_message_handler(no_more, lambda message: "➡ No more transactions" in message.text)
    dp.register_message_handler(no_transaction, lambda message: "➡ No transactions" in message.text)
    dp.register_message_handler(add_transaction, lambda message: "✅ Add transaction" in message.text)
    dp.register_message_handler(any_transaction, lambda message: "❌ I don`t have any transaction" in message.text)
    dp.register_message_handler(report, lambda message: "🗂 Send report" in message.text)
    dp.register_message_handler(back, lambda message: "↩ Back" in message.text)
    dp.register_message_handler(last, state=Transaction.last_transaction)
    dp.register_message_handler(date, state=Transaction.date_transaction)
    dp.register_message_handler(stop_handler, state="*", commands="stop")
    dp.register_message_handler(stop_handler, Text(equals="stop", ignore_case=True), state="*")


