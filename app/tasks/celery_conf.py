from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks", "app.tasks.scheduled"],
)


celery_app.conf.beat_schedule = {
    "check-in tomorrow": {
        "task": "email.booking_reminder_1day",
        # "schedule": 50,  # seconds
        "schedule": crontab(minute=30, hour=9),
    },
    "check-in 3 days": {
        "task": "email.booking_reminder_3day",
        #     'schedule' : 52, # seconds
        "schedule": crontab(minute=30, hour=15),
    },
}
