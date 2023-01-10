from aiogram.utils import executor
from handlers import client_start, client_register, other, client_transaction, admin, admin_admin, client_login
from create_bot import dp
from data_base import sql_db
from sending_machine.client_sending import scheduler
import asyncio


async def on_startup(_):
    print("The bot has been enabled")
    sql_db.sql_start()
    await other.set_default_commands(_)
    asyncio.create_task(scheduler())


client_start.handlers_bot(dp)
client_register.handlers_bot(dp)
admin.handlers_bot(dp)
admin_admin.handlers_bot(dp)
client_transaction.handlers_bot(dp)
client_login.handlers_bot(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
