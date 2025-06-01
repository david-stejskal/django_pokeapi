import typing

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class TrackingleModel(BaseModel):
    modified = models.DateTimeField(null=True, blank=True, default=None)

    class Meta(BaseModel.Meta):
        abstract = True

    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.modified = timezone.now()
        super().save(*args, **kwargs)

    def update(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.modified = timezone.now()
        super().update(*args, **kwargs)  # type: ignore
