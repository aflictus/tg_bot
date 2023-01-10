from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.client_kb import kb_menu
from aiogram.dispatcher.filters import Text
import re


class Login(StatesGroup):
    email = State()
    phone_number = State()

async def start(message: types.Message):
    await message.answer("We are glad to see you again!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Enter the email address you used during your registration with Iolipay.")
    await Login.email.set()


async def stop_handler(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("The process has been stopped!")


async def load_email(message: types.Message, state=FSMContext):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, message.text):
        async with state.proxy() as data:
            data["email"] = message.text
        await Login.next()
        await message.answer("Wonderful!")
        await message.answer("Write your Georgian phone number. The format should be: +995987654321")
    else:
        await message.answer("Invalid Email")


async def load_ph_number(message: types.Message, state=FSMContext):
    name = "?"
    if message.text[:4] == "+995" and len(message.text) == 13 and message.text[1:].isdigit():
        async with state.proxy() as data:
            data["phone_number"] = message.text
        await message.answer("Great!")
        await message.answer(f"{name}, we're glad to help you.", reply_markup=kb_menu)
        await state.finish()

    else:
        await message.answer("The format should be: +995#########.")


def handlers_bot(dp: Dispatcher):
    dp.register_message_handler(start, lambda message: "✅ Yes" in message.text)
    dp.register_message_handler(load_email, state=Login.email)
    dp.register_message_handler(load_ph_number, state=Login.phone_number)
    dp.register_message_handler(stop_handler, state="*", commands="stop")
    dp.register_message_handler(stop_handler, Text(equals="stop", ignore_case=True), state="*")