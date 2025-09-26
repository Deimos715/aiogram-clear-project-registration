from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

_scheduler: Optional[AsyncIOScheduler] = None

def setup_scheduler() -> AsyncIOScheduler:
    '''
    Инициализация планировщика. По умолчанию - одна демонстрационная задача.
    '''
    global _scheduler
    if _scheduler is not None:
        return _scheduler
    _scheduler = AsyncIOScheduler(timezone='UTC')

    @_scheduler.scheduled_job(CronTrigger.from_crontab('*/5 * * * *'))
    def demo_job() -> None:
        print(f'[APScheduler] demo_job tick at {datetime.utcnow().isoformat()}Z')

    _scheduler.start()
    return _scheduler

async def shutdown_scheduler(scheduler: Optional[AsyncIOScheduler]) -> None:
    if scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
