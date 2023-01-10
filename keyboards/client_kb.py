from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types

item0 = KeyboardButton("✅ Yes")
item8 = KeyboardButton("❌ No")

kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_start.row(item0, item8)


item1 = KeyboardButton("⏳ $25/Monthly")
item2 = KeyboardButton("🌐 $240/Annual")
item3 = KeyboardButton("🌐 I’m corporative client")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.row(item1, item2).add(item3)


item4 = KeyboardButton("✅ Add another transaction")
item5 = KeyboardButton("➡ No more transactions")

kb_transaction = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_transaction.row(item4, item5)


item04 = KeyboardButton("✅ Add transaction")
item05 = KeyboardButton("➡ No transactions")

kb_transaction0 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_transaction0.row(item04, item05)


item7 = KeyboardButton("🗂 Send report")
item6 = KeyboardButton("↩ Back")

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_menu.add(item7).add(item6)


item07 = KeyboardButton("❌ I don`t have any transaction")
item06 = KeyboardButton("↩ Back")

kb_menu0 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_menu0.add(item7).add(item6)



