from django.urls import path
from django.views.generic import RedirectView

from .v1 import api

urlpatterns = [
    path("", RedirectView.as_view(url="api/v1/docs")),
    path("api/v1/", api.urls, name="ninja-v1"),  # type: ignore
]
