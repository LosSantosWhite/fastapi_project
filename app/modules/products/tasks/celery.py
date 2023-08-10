from celery import Celery

from app.config import config

celery = Celery(
    "tasks", broker=str(config.redis.dsn), include=["app.modules.products.tasks"]
)
