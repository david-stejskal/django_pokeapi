import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_pokeapi.settings")

app = Celery("django_pokeapi.apps.common")
app.config_from_object("django.conf:settings", namespace="CELERY", force=True)
app.autodiscover_tasks()
