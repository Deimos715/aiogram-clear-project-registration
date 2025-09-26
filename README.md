# Aiogram 3.x Starter (Registration, no referral)

Чистая заготовка бота на Aiogram 3.x.  
Реализованы:
- регистрация пользователя в PostgreSQL при первом `/start`;
- команда `/profile` для просмотра профиля;
- простая админ-статистика: `/stats` и `/users` (для ADMIN_IDS).

Конфиги и `.env` лежат в `settings/`.

## Быстрый старт

Создать виртуальное окружение и установить зависимости:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Переименовать в папке `settings` файл `.env.example` в `.env` и указать токен и настройки базы:

```bash
cp settings/.env.example settings/.env
```

Запустить бота командой:

```bash
python main.py
```

## Команды

- `/start` — регистрация/приветствие  
- `/help` — помощь  
- `/profile` — профиль пользователя  
- `/stats` — количество пользователей (только для ADMIN_IDS)  
- `/users` — список пользователей (только для ADMIN_IDS)

---

## Структура проекта

### settings/
Хранит конфигурацию проекта и `.env` с секретными данными.

- `config.py` — загрузка переменных окружения и объект `settings`.  
- `.env` — рабочие настройки (токен, база, админы и т.д.).  
- `.env.example` — пример файла `.env`.

### bot/
Основной код бота.

- `routers.py` — собирает все роутеры из пакета `handlers` и подключает их к `Dispatcher`.

#### bot/handlers/
Здесь лежат обработчики сообщений.

- `start.py` — команда `/start` (регистрация пользователя).  
- `help.py` — команда `/help`.  
- `profile.py` — команда `/profile` (показ профиля).  
- `admin.py` — команды `/stats` и `/users` (админ-функции).  
- `echo.py` — базовый echo-хэндлер (для теста).

#### bot/keyboards/
Заготовки клавиатур (reply/inline).

- `common.py` — пример клавиатуры «Да/Нет».

#### bot/middlewares/
Мидлвары (промежуточная логика).

- `throttling.py` — простейший антиспам (ограничение частоты сообщений).

#### bot/filters/
Кастомные фильтры для сообщений и апдейтов.

- `is_admin.py` — фильтр, проверяющий, что сообщение пришло от администратора.

#### bot/services/
Сервисы, не завязанные на Telegram напрямую.

- `db.py` — подключение к PostgreSQL через `asyncpg` (инициализация таблицы `users`).  
- `user_service.py` — функции для работы с пользователями (регистрация, выборка, статистика).  
- `scheduler.py` — планировщик задач (APScheduler).

#### bot/utils/
Вспомогательные утилиты.

- `logging.py` — настройка логирования.
