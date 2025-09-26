from aiogram import Router, F
from aiogram.types import Message

router = Router(name='echo')

@router.message(F.text)
async def echo_text(message: Message) -> None:
    await message.answer(message.text)
