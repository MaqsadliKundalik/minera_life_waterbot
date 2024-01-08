from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_command_keyboards = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
start_command_keyboards.insert(KeyboardButton(text="zakaz qo'shish"))
start_command_keyboards.insert(KeyboardButton(text="zakaz o'chirish"))
start_command_keyboards.insert(KeyboardButton(text="chiqish"))

cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.insert(KeyboardButton(text="🚫 Bekor qilish"))

confirmation_keyboards = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
confirmation_keyboards.insert(KeyboardButton(text="Ha"))
confirmation_keyboards.insert(KeyboardButton(text="Yo'q"))