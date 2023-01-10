from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


stop_inl = InlineKeyboardMarkup(row_width=1)
stop = InlineKeyboardButton(text="Отмена", callback_data="stop", one_time_keyboard=True)

stop_inl.add(stop)


id_inl = InlineKeyboardMarkup(row_width=1)
id = InlineKeyboardButton(text="Проверить", callback_data="check_id", one_time_keyboard=True)

id_inl.add(id)