from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from create_bot import admins

# Создаем главное меню с кнопками
def main_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [[KeyboardButton(text='👤 Мой профиль')]]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text='⚙️ Админ панель')])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Воспользуйтесь меню:'
    )


# Создаем клавиатуру для возврата на главную страницу
def home_page_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [[KeyboardButton(text='🔙 Назад')]]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text='⚙️ Админ панель')])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Воспользуйтесь меню:'
    )
