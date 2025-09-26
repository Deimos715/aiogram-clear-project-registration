import asyncpg
from typing import Optional
from settings.config import settings

_pool: Optional[asyncpg.Pool] = None

INIT_SQL = '''
CREATE TABLE IF NOT EXISTS users (
    id bigserial PRIMARY KEY,
    tg_id bigint UNIQUE NOT NULL,
    username text,
    full_name text,
    joined_at timestamptz NOT NULL DEFAULT now()
);
'''

async def create_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        if not settings.database_url:
            raise RuntimeError('DATABASE_URL is empty; set it in settings/.env to use DB')
        _pool = await asyncpg.create_pool(dsn=settings.database_url, min_size=1, max_size=5)
    return _pool

async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

async def init_db() -> None:
    pool = await create_pool()
    async with pool.acquire() as conn:
        await conn.execute(INIT_SQL)
