from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage


bot = Bot("5987117436:AAErC0g-AZ9RqpTA-w-NTrpGY7xOTNDXlIA")
dp = Dispatcher(bot, storage=MemoryStorage())


#Промежуточный файл