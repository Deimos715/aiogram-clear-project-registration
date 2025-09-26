from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from create_bot import bot, admins
from db_handler.db_funk import get_user_data, insert_user
from keyboards.kbs import main_kb, home_page_kb

user_router = Router()

universe_text = ('Чтобы получить информацию о своём профиле, воспользуйтесь кнопкой «Мой профиль» '
                 'или командой /profile из меню.')


# Проверяем регистрацию пользователя и добавляем в базу при первом запуске
@user_router.message(CommandStart())
async def cmd_start(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_info = await get_user_data(user_id=message.from_user.id)

    if user_info:
        response_text = f'{message.from_user.full_name}, вижу, что вы уже в базе. {universe_text}'
    else:
        await insert_user(user_data={
            'user_id': message.from_user.id,
            'full_name': message.from_user.full_name,
            'user_login': message.from_user.username,
        })
        response_text = (f'{message.from_user.full_name}, вы зарегистрированы в боте. '
                         f'{universe_text}')

    await message.answer(text=response_text, reply_markup=main_kb(message.from_user.id))



# Получаем и показываем профиль пользователя
@user_router.message(Command('profile'))
@user_router.message(F.text.contains('Мой профиль'))
async def get_profile(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_info = await get_user_data(user_id=message.from_user.id)
        if not user_info:
            await message.answer('Похоже, вы ещё не зарегистрированы. Нажмите /start.')
            return

        text = (f'👉 Телеграм ID: <code><b>{user_info.get("user_id")}</b></code>\n'
                f'📝 Полное имя: {user_info.get("full_name") or "-"}\n'
                f'🔑 Логин: {("@" + user_info.get("user_login")) if user_info.get("user_login") else "-"}\n'
                f'📅 Зарегистрирован: {user_info.get("date_reg")}')

    await message.answer(text, reply_markup=home_page_kb(message.from_user.id))



# Возвращаем пользователя на главную страницу
@user_router.message(F.text.contains('Назад'))
async def go_home(message: Message):
    await message.answer(f'{message.from_user.first_name}, {universe_text}', reply_markup=main_kb(message.from_user.id))


# Показываем справку с командами (и админскими командами, если пользователь админ)
@user_router.message(Command("help"))
async def cmd_help(message: Message):
    is_admin = message.from_user.id in admins

    text = (
        "🆘 Помощь\n\n"
        "Доступные команды:\n"
        "• /start — регистрация/приветствие\n"
        "• /profile — профиль пользователя\n"
        "• /help — эта помощь\n"
    )
    if is_admin:
        text += "\n\n⚙️ Админские команды:\n• /stats — статистика\n• /broadcast — рассылка"

    await message.answer(text, reply_markup=main_kb(message.from_user.id))
