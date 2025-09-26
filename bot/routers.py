from aiogram import Dispatcher
from .handlers.start import router as start_router
from .handlers.help import router as help_router
from .handlers.echo import router as echo_router
from .handlers.profile import router as profile_router
from .handlers.admin import router as admin_router

def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)
    dp.include_router(echo_router)
