from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from settings.config import settings
from bot.filters.is_admin import IsAdmin
from bot.services.user_service import count_users, list_users

router = Router(name='admin')
router.message.filter(IsAdmin(settings.admin_ids))

@router.message(Command('stats'))
async def cmd_stats(message: Message) -> None:
    total = await count_users()
    await message.answer(f'Пользователей: {total}')

@router.message(Command('users'))
async def cmd_users(message: Message) -> None:
    rows = await list_users(limit=20, offset=0)
    if not rows:
        await message.answer('Пока нет пользователей.')
        return
    lines = []
    for r in rows:
        u = f'@{r["username"]}' if r['username'] else '-'
        lines.append(f'{r["tg_id"]}  {u}  {r["full_name"] or "-"}')
    await message.answer('Первые пользователи:\n' + '\n'.join(lines))
