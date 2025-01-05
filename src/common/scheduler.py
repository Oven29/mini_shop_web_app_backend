from core.config import settings

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.redis import RedisJobStore


redis_jobstore = RedisJobStore(
    db=settings.redis.db,
    host=settings.redis.host,
    port=settings.redis.port,
)

scheduler = AsyncIOScheduler(
    jobstores={'default': redis_jobstore},
    job_defaults={'coalesce': False, 'max_instances': 100},
)
