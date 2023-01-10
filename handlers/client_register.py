from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.client_kb import kb_client, kb_menu
from data_base.sql_db import sql_add_command_tax, load_tax_data
from google_sheets.ioli_data import tax_data
from sending_machine.admin_sending import admins_notify
from aiogram.dispatcher.filters import Text
import re
import datetime
from csv import writer


class TaxData(StatesGroup):
    name = State()
    surname = State()
    email = State()
    ph_number = State()
    telegram_id = State()
    payment_type = State()
    tax_id = State()
    address = State()
    rs_username = State()
    rs_password = State()
    bus_activ = State()
    end_datetime_reg = State()



#############     CLIENT CONTACTS      #############


async def start(message: types.Message):
    await message.answer("Please introduce yourself", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Write the name in English as indicated in the international passport.")
    await TaxData.name.set()


async def stop_handler(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("The process has been stopped!")


async def load_name(message: types.Message, state=FSMContext):
    if bool(re.fullmatch('[A-Za-z]{2,25}', message.text.strip())):
        await TaxData.name.set()
        async with state.proxy() as data:
            data["name"] = message.text.strip()
        await TaxData.next()
        await message.answer("Super!")
        await message.answer(f"{data['name']}, write the surname in English as indicated in the international passport.")
    else:
        await message.answer("Name must be in English and must not contain spaces!")


async def load_surname(message: types.Message, state=FSMContext):
    if bool(re.fullmatch('[A-Za-z]{2,25}', message.text.strip())):
        async with state.proxy() as data:
            data["surname"] = message.text.strip()
        await TaxData.next()
        await message.answer("Wonderful!")
        await message.answer("Please enter your valid email. It will be needed by the tax service to send informational messages.")
    else:
        await message.answer("Surname must be in English and must not contain spaces!")



async def load_email(message: types.Message, state=FSMContext):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, message.text):
        async with state.proxy() as data:
            data["email"] = message.text
        await TaxData.next()
        await message.answer("Wonderful!")
        await message.answer("Write your Georgian phone number. The format should be: +995987654321")
    else:
        await message.answer("Invalid Email")


async def load_ph_number(message: types.Message, state=FSMContext):

    if message.text[:4] == "+995" and len(message.text) == 13 and message.text[1:].isdigit():
        async with state.proxy() as data:
            data["ph_number"] = message.text
        await message.answer("Great!")
        await message.answer(f"{data['name']}, choose iolipay service package", reply_markup=kb_client)
        await TaxData.telegram_id.set()
        async with state.proxy() as data:
            data["telegram_id"] = message.from_user.id

        await TaxData.payment_type.set()

    else:
        await message.answer("The format should be: +995#########.")


#############     CLIENT TAX ID      #############


async def payment(message : types.Message , state=FSMContext):
    buttons = ["$25/Monthly", "$240/Annual", "I’m corporative client"]
    if message.text[2:] in buttons:
        async with state.proxy() as data:
            data["payment_type"] = message.text[2:]
        await TaxData.next()

        await message.answer("Cool!", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Now I will register you in the system of the tax service of Georgia. I will need information about your registration as an individual entrepreneur.")
        await message.answer("Enter the Georgian Tax Identification Number of Individual Entrepreneur. This is a 9-digit code indicated in the IP registration certificate")
    else:
        await message.answer("Click the button!😂", reply_markup=kb_client)


async def tax_id(message : types.Message , state=FSMContext):
    if message.text.isdigit() and len(message.text) == 9:
        async with state.proxy() as data:
            data["tax_id"] = message.text
        await TaxData.next()

        await message.answer("Good!")
        await message.answer("Now enter the address that was used to register the status of an individual entrepreneur in Georgia.")
        await message.answer("For example: 0105, Georgia, Tbilisi, Freedom square, 2-58")
    else:
        await message.answer("The format should be: 987654321")


async def address(message : types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
    await TaxData.next()

    await message.answer("Wonderful. There is very little left.")
    await message.answer("Now you need to find the following information in the received sms from rs.ge and enter rs username")


async def rs_username(message : types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["rs_username"] = message.text
    await TaxData.next()

    await message.answer("And also write rs.ge password")


async def rs_password(message : types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["rs_password"] = message.text
    await TaxData.next()

    await message.answer("Super! And the final question")
    await message.answer("Write the type of your business activity.")


async def bus_activ(message : types.Message, state=FSMContext):
    now = datetime.datetime.now()
    async with state.proxy() as data:
        data["bus_activ"] = message.text
    await TaxData.end_datetime_reg.set()
    async with state.proxy() as data:
        data["end_datetime_reg"] = now.strftime("%d-%m-%Y %H:%M")

    await sql_add_command_tax(state)


    await message.answer("Great!")
    await message.answer("Your registration has been successfully completed.")
    await message.answer("When the time comes for filing the declaration and tax, I will write to you in this chat. Paying the tax and filing the declaration will take no more than 3 minutes. See you later 🤗")

    await admins_notify(message)

    data = load_tax_data(message.from_user.id)
    tax_data(data)

    await state.finish()




def handlers_bot(dp: Dispatcher):
    dp.register_message_handler(start, lambda message: "❌ No" in message.text)
    dp.register_message_handler(stop_handler, state="*", commands="stop")
    dp.register_message_handler(stop_handler, Text(equals="stop", ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=TaxData.name)
    dp.register_message_handler(load_surname, state=TaxData.surname)
    dp.register_message_handler(load_email, state=TaxData.email)
    dp.register_message_handler(load_ph_number, state=TaxData.ph_number)
    dp.register_message_handler(payment, state=TaxData.payment_type)
    dp.register_message_handler(tax_id, state=TaxData.tax_id)
    dp.register_message_handler(address, state=TaxData.address)
    dp.register_message_handler(rs_username, state=TaxData.rs_username)
    dp.register_message_handler(rs_password, state=TaxData.rs_password)
    dp.register_message_handler(bus_activ, state=TaxData.bus_activ)


