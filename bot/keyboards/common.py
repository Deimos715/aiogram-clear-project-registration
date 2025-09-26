from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def yes_no_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Да'), KeyboardButton(text='Нет')]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
