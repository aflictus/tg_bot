from aiogram import Dispatcher
from data_base.sql_db import admin_id
from aiogram_broadcaster import TextBroadcaster
import asyncio




async def admin_notify(id):
    await TextBroadcaster(id, 'Был зарегистрирован новый пользователь!').run()


async def admins_notify(message):
    users = admin_id()
    for id in users:
        await admin_notify(id)
        await asyncio.sleep(.05)


async def admin_notify_payment(id, id_user):
    await TextBroadcaster(id, f'Пользователю нужен платёж!\nID пользователя: {id_user}').run()


async def admins_notify_payment(id_user):
    users = admin_id()
    for id in users:
        await admin_notify_payment(id, id_user)
        await asyncio.sleep(.05)
