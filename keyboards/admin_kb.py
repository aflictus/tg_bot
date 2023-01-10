from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types

item0 = KeyboardButton("Добавить админа")
item6 = KeyboardButton("Работа с пользователями")

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(item6).add(item0)


item1 = KeyboardButton("Список id")
item2 = KeyboardButton("Добавить пользователя")
item3 = KeyboardButton("Удалить пользователя")
item7 = KeyboardButton("Вернуться")


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(item1).add(item2).add(item3).add(item7)


item4 = KeyboardButton("Добавить платёж")
item5 = KeyboardButton("Все клиенты")


kb_users = ReplyKeyboardMarkup(resize_keyboard=True)
kb_users.add(item5).add(item4).add(item7)
