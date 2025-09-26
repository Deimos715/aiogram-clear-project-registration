from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name='help')

@router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await message.answer('Доступные команды:\n/start - регистрация/приветствие\n/help - помощь\n/profile - мой профиль\n/stats - статистика (админ)\n/users - пользователи (админ)')
