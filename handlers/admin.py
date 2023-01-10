from aiogram import types, Dispatcher
from data_base.sql_db import telegram_id, tax_data, admin_id, tg_id_declaration
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from keyboards.admin_inl import stop_inl, id_inl
from keyboards.admin_kb import kb_menu, kb_admin, kb_users
from sending_machine.client_sending import users_notify_payment
from create_bot import bot
import openpyxl


class LoadPayment(StatesGroup):
    id = State()
    payment = State()


""" Админ меню """


async def admin_handler(message: types.Message):
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        await message.answer("Модераторское право подтверждено!", reply_markup=kb_menu)


async def admin_admin(message: types.Message):
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        await message.answer("Добавить админа:", reply_markup=kb_admin)


async def admin_users(message: types.Message):
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        await message.answer("Работа с пользователями:", reply_markup=kb_users)


async def admin_back(message: types.Message):
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        await message.answer("Меню:", reply_markup=kb_menu)


#### Выгрузка клиентов ####

async def load_tax_data(message: types.Message):
    await message.answer("Загружаю...")
    data = [["ID", "Name", "Surname", "Email", "Phone number", "Payment type", "Tax ID", "Address", "RS username",
             "RS password", "Business activity", "Month Transaction", "Date Transaction", "All Transaction"]]
    data.append(*tax_data())
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        book = openpyxl.Workbook()
        sheet = book.active
        index = 0
        i = 1
        for user in data:
            for j in range(1, 15):
                sheet.cell(row=i, column=j).value = user[index]
                index += 1
            i += 1
            index = 0
        book.save("data.xlsx")
        book.close()
        await message.answer_document(open('data.xlsx', 'rb'))


#### Присваивание платежа ####

async def start_load_payment(message: types.Message):
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        await message.answer("Введи персональное id человека")
        await LoadPayment.id.set()


async def stop_handler(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Ок")


async def load_id(message: types.Message, state=FSMContext):
    await message.answer("Хорошо, если ты правильно ввёл id, напиши сумму платежа в лари.")
    async with state.proxy() as data:
        data["id"] = int(message.text)
    await LoadPayment.next()


async def load_payment(message: types.Message, state=FSMContext):
    await message.answer("Пользователь получил платёж!")
    async with state.proxy() as data:
        data["payment"] = message.text
    tg_id = tg_id_declaration(data["id"])
    await users_notify_payment(tg_id, message.text)

    await state.finish()


def handlers_bot(dp: Dispatcher):
    dp.register_message_handler(admin_handler, commands=["admin"])
    dp.register_message_handler(admin_admin, lambda message: "Добавить админа" == message.text)
    dp.register_message_handler(admin_users, lambda message: "Работа с пользователями" == message.text)
    dp.register_message_handler(admin_back, lambda message: "Вернуться" == message.text)
    dp.register_message_handler(load_tax_data, lambda message: "Все клиенты" == message.text)
    dp.register_message_handler(start_load_payment, lambda message: "Добавить платёж" == message.text)
    dp.register_message_handler(stop_handler, state="*", commands="stop")
    dp.register_message_handler(stop_handler, Text(equals="stop", ignore_case=True), state="*")
    dp.register_message_handler(load_id, state=LoadPayment.id)
    dp.register_message_handler(load_payment, state=LoadPayment.payment)
