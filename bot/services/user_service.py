from aiogram.types import Message
from bot.services.db import create_pool

async def upsert_user_from_message(message: Message):
    uid = message.from_user.id if message.from_user else 0
    username = message.from_user.username if message.from_user else None
    full_name = message.from_user.full_name if message.from_user else None
    pool = await create_pool()
    sql = '''
    INSERT INTO users (tg_id, username, full_name)
    VALUES ($1, $2, $3)
    ON CONFLICT (tg_id) DO UPDATE SET
        username = EXCLUDED.username,
        full_name = EXCLUDED.full_name
    RETURNING id, tg_id, username, full_name, joined_at;
    '''
    async with pool.acquire() as conn:
        return await conn.fetchrow(sql, uid, username, full_name)

async def get_user_by_tg_id(tg_id: int):
    pool = await create_pool()
    sql = 'SELECT id, tg_id, username, full_name, joined_at FROM users WHERE tg_id = $1;'
    async with pool.acquire() as conn:
        return await conn.fetchrow(sql, tg_id)

async def count_users() -> int:
    pool = await create_pool()
    sql = 'SELECT COUNT(*) FROM users;'
    async with pool.acquire() as conn:
        val = await conn.fetchval(sql)
        return int(val or 0)

async def list_users(limit: int = 20, offset: int = 0):
    pool = await create_pool()
    sql = '''
    SELECT tg_id, username, full_name, joined_at
    FROM users
    ORDER BY joined_at DESC
    LIMIT $1 OFFSET $2;
    '''
    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, limit, offset)
        return rows
