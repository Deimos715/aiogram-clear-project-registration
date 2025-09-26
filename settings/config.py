import os
from dataclasses import dataclass
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
load_dotenv(os.path.join(BASE_DIR, '.env'))

def _parse_admin_ids(s: str) -> list[int]:
    ids: list[int] = []
    for part in s.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            pass
    return ids

@dataclass
class Settings:
    bot_token: str = os.getenv('BOT_TOKEN', '')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    database_url: str = os.getenv('DATABASE_URL', '')
    tz: str = os.getenv('TZ', 'Europe/Moscow')
    admin_ids_raw: str = os.getenv('ADMIN_IDS', '')

    @property
    def admin_ids(self) -> list[int]:
        return _parse_admin_ids(self.admin_ids_raw)

settings = Settings()
