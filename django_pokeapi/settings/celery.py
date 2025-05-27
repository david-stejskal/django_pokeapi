from celery.schedules import crontab

from .common import env

REDIS_URL = env.str("REDIS_URL")


CELERY_BEAT_SCHEDULE = {}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}
