from celery import Celery
from celery.schedules import crontab
from app.config import settings

celery_worker = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks",
             "app.tasks.scheduled",
             ],
)

celery_worker.conf.broker_connection_retry_on_startup = True

celery_worker.conf.beat_schedule = {
    "nazw": {
        "task" : "periodic_task",
        "schedule" : 10,
    }
}