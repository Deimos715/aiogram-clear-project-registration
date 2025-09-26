import time
from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message

class ThrottlingMiddleware(BaseMiddleware):
    '''
    Простейший троттлинг по user_id (in-memory). На вырост можно заменить на Redis.
    '''
    def __init__(self, rate_limit: float = 0.5) -> None:
        super().__init__()
        self.rate_limit = rate_limit
        self.last_called: Dict[int, float] = {}

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        uid = event.from_user.id if event.from_user else 0
        now = time.monotonic()
        prev = self.last_called.get(uid, 0.0)
        if now - prev < self.rate_limit:
            return
        self.last_called[uid] = now
        return await handler(event, data)
