from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from create_bot import admins, bot
from db_handler.db_funk import get_all_users
from keyboards.kbs import home_page_kb

admin_router = Router()

# Получаем список всех пользователей и показываем их администратору
@admin_router.message((F.text.endswith('Админ панель')) & (F.from_user.id.in_(admins)))
async def show_admin_panel(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        all_users_data = await get_all_users()

        admin_text = f'👥 В базе данных <b>{len(all_users_data)}</b> человек. Вот короткая информация по каждому:\n\n'
        for user in all_users_data:
            admin_text += (
                f'👤 Телеграм ID: {user.get("user_id")}\n'
                f'📝 Полное имя: {user.get("full_name") or "-"}\n'
            )
            if user.get("user_login"):
                admin_text += f'🔑 Логин: @{user.get("user_login")}\n'

            admin_text += f'📅 Зарегистрирован: {user.get("date_reg")}\n\n〰️〰️〰️〰️〰️〰️〰️〰️\n\n'

    await message.answer(admin_text, reply_markup=home_page_kb(message.from_user.id))
