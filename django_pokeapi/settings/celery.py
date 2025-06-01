# from celery.schedules import crontab

from .common import env

REDIS_URL = env.str("REDIS_URL")

# Celery Configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Task routing and queue configuration
CELERY_TASK_DEFAULT_QUEUE = "django_pokeapi"
CELERY_TASK_ROUTES = {
    "django_pokeapi.*": {"queue": "django_pokeapi"},
}

# TODO: add once a week task to update all Pokemon data
CELERY_BEAT_SCHEDULE = {}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}
