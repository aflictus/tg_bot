from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.admin_inl import stop_inl
from aiogram import types, Dispatcher
from data_base.sql_db import admin_id, add_admin_id, admin_all, sql_delete_command
from keyboards.admin_inl import stop_inl
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bot



class AddAdmin(StatesGroup):
    name = State()
    id = State()


#### Работа с модерацией ####


async def id(message: types.Message):
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        if len(list_id) == 1:
            await message.answer(f"На данный момент кроме вас никто не имеет доступ.\nВаш id: {message.from_user.id}")
        else:
            await message.answer(f"Список присутсвующих id: {list_id}\nВаш id: {message.from_user.id}")
    else:
        await message.answer(f"{message.from_user.id}")


async def admin_add(message: types.Message):
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        await AddAdmin.name.set()
        await message.answer("Введите имя пользователя.")


async def stop_handler(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Ок")


async def add_name(message: types.Message, state=FSMContext):
    if message.text != "Добавить пользователя":
        async with state.proxy() as data:
            data["name"] = message.text
        await AddAdmin.next()
        await message.answer("Введите id пользователя.")
    else:
        await message.answer("Вводи имя уже 😂")


async def add_id(message: types.Message, state=FSMContext):
    list_id = admin_id()
    if str(message.from_user.id) in list_id and message.text.isdigit():
        if message.text not in list_id:
            async with state.proxy() as data:
                data["id"] = message.text
            await message.answer(f"Добавление {data['name']} прошло успешно!")
            await add_admin_id(state)
            await state.finish()

            await message.answer(f"На данный момент имеют доступ: {len(list_id)} аккаунта.")
        else:
            await message.answer("Данный пользователь есть в списке")
            await message.answer(f"На данный момент имеют доступ: {len(list_id)} аккаунта.")
    else:
        await message.answer("id состоит только из цифр!")


async def del_callback(callback_query: types.CallbackQuery):
    list_id = admin_id()
    if str(callback_query.from_user.id) in list_id:
        if "del " in callback_query.data:
            await sql_delete_command(callback_query.data.replace("del ", ""))
            await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} удалён.", show_alert=True)


async def delete_admin(message: types.Message):
    list_id = admin_id()
    if str(message.from_user.id) in list_id:
        users = admin_all()
        for user in users:
            await bot.send_message(message.from_user.id, f"{user[0]} - {user[1]}", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f"Удалить {user[0]}", callback_data=f"del {user[0]}")))


def handlers_bot(dp: Dispatcher):
    dp.register_message_handler(admin_add, lambda message: "Добавить пользователя" == message.text)
    dp.register_message_handler(id, lambda message: "Список id" == message.text)
    dp.register_message_handler(add_name, state=AddAdmin.name)
    dp.register_message_handler(add_id, state=AddAdmin.id)
    dp.register_message_handler(stop_handler, state="*", commands="stop")
    dp.register_message_handler(stop_handler, Text(equals="stop", ignore_case=True), state="*")
    dp.register_callback_query_handler(del_callback, lambda x: x.data and x.data.startswith("del "))
    dp.register_message_handler(delete_admin, lambda message: "Удалить пользователя" == message.text)
