from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.user_service import get_user_by_tg_id, upsert_user_from_message

router = Router(name='profile')

@router.message(Command('profile'))
async def cmd_profile(message: Message) -> None:
    tg_id = message.from_user.id if message.from_user else 0
    row = await get_user_by_tg_id(tg_id)
    if row is None:
        await upsert_user_from_message(message)
        row = await get_user_by_tg_id(tg_id)
    if row is None:
        await message.answer('Не удалось получить профиль. Попробуйте позднее.')
        return
    username_line = f'Username: @{row["username"]}' if row['username'] else 'Username: -'
    text = f'Ваш профиль:\nID: {row["tg_id"]}\nИмя: {row["full_name"] or "-"}\n{username_line}'
    await message.answer(text)
