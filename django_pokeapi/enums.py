from django.db import models


class Environment(models.TextChoices):
    LOCAL = "local"
    DEV = "dev"
