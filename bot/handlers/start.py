from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.services.user_service import upsert_user_from_message

router = Router(name='start')

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await upsert_user_from_message(message)
    await message.answer('Привет! Ты зарегистрирован.\nКоманды: /help, /profile')
