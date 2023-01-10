from aiogram import Dispatcher
from data_base.sql_db import all_telegram_id, admin_id
from aiogram_broadcaster import TextBroadcaster #pip install aiogram_broadcaster
from keyboards.client_kb import kb_transaction0
import asyncio
import aioschedule
from datetime import date


async def user_notify(telegram_id, name):
    await TextBroadcaster(telegram_id, f"Hey, {name.title()}").run()
    await TextBroadcaster(telegram_id, f"It's time to pay taxes and file returns. This will take three minutes.").run()
    await TextBroadcaster(telegram_id, 'Fill in the information on the income of the reporting (previous) month, from the 1st day including the last.').run()
    await TextBroadcaster(telegram_id, 'Please select a button:', reply_markup=kb_transaction0).run()



async def notify():
    if date.today().strftime("%d") == "01":
        users = all_telegram_id()
        for id in users:
            name, telegram_id = id
            await user_notify(telegram_id, name)
            await asyncio.sleep(.05)
    else:
        pass


async def scheduler():
    aioschedule.every().day.at("10:00").do(notify)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def user_notify_payment(id, payment):
    await TextBroadcaster(id, 'Hey, your report is ready!').run()
    await TextBroadcaster(id, f"Please, pay tax in the amount of {payment} Gel to account 101001000.").run()


async def users_notify_payment(id_user, payment):
    await user_notify_payment(id_user, payment)
    await asyncio.sleep(.05)








