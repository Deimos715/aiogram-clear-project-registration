import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from settings.config import settings
from bot.routers import setup_routers
from bot.utils.logging import setup_logging
from bot.services.scheduler import setup_scheduler, shutdown_scheduler
from bot.services.db import create_pool, close_pool, init_db

async def main() -> None:
    if not settings.bot_token:
        raise RuntimeError('BOT_TOKEN is empty. Set it in settings/.env')

    setup_logging(settings.log_level)
    logging.getLogger(__name__).info('Starting bot...')

    # Init DB
    await create_pool()
    await init_db()

    bot = Bot(settings.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    setup_routers(dp)

    cmds = [
        BotCommand(command='start', description='Начать'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='profile', description='Мой профиль'),
        BotCommand(command='stats', description='Статистика (админ)'),
        BotCommand(command='users', description='Пользователи (админ)'),
    ]
    await bot.set_my_commands(cmds)

    scheduler = setup_scheduler()

    try:
        await dp.start_polling(bot)
    finally:
        await shutdown_scheduler(scheduler)
        await close_pool()
        logging.getLogger(__name__).info('Bot stopped.')

if __name__ == '__main__':
    asyncio.run(main())
