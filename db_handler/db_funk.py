from typing import Any, Dict, List, Optional
from create_bot import db_manager
from sqlalchemy import BigInteger, String, TIMESTAMP, text

USERS_TABLE = 'users_reg'


# Создаём таблицу users_reg, если её ещё нет
async def init_db() -> None:
    sql = f"""
    CREATE TABLE IF NOT EXISTS {USERS_TABLE} (
        user_id   BIGINT PRIMARY KEY,
        full_name VARCHAR(255),
        user_login VARCHAR(255),
        date_reg  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    async with db_manager as client:
        # Открываем ассинхронную сессию
        async with client.session() as session:
            await session.execute(text(sql))
            await session.commit()


# Обёртка для вызова init_db — создаём таблицу пользователей
async def create_table_users(table_name: str = USERS_TABLE) -> None:
    await init_db()


# Получаем данные конкретного пользователя по user_id
async def get_user_data(user_id: int, table_name: str = USERS_TABLE) -> Optional[Dict[str, Any]]:
    async with db_manager as client:
        return await client.select_data(
            table_name=table_name,
            where_dict={'user_id': user_id},
            one_dict=True
        )


# Возвращаем список всех пользователей или только их количество
async def get_all_users(table_name: str = USERS_TABLE, count: bool = False):
    async with db_manager as client:
        all_users: List[Dict[str, Any]] = await client.select_data(table_name=table_name)
        if count:
            return len(all_users)
        return all_users

# Добавляем пользователя в таблицу или обновляем данные, если такой user_id уже есть
async def insert_user(user_data: Dict[str, Any], table_name: str = USERS_TABLE) -> None:
    async with db_manager as client:
        await client.insert_data_with_update(
            table_name=table_name,
            records_data=user_data,
            conflict_column='user_id',
            update_on_conflict=True
        )
