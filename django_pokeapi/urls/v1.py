import typing

import orjson
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer, JSONRenderer

from django_pokeapi.apps.pokeapi.api.pokeapi import router


class ORJSONRenderer(BaseRenderer):
    """Custom JSON renderer using orjson for better performance."""

    media_type = "application/json"

    def __init__(self):
        self.backup_renderer = JSONRenderer()

    def render(
        self, request: HttpRequest, data: typing.Any, *, response_status: typing.Any
    ) -> bytes:
        """Render data to JSON using orjson with fallback to default renderer."""
        try:
            return orjson.dumps(data)
        except TypeError as error:
            # Handle large integer overflow by falling back to default renderer
            if "Integer exceeds 64-bit range" in str(error):
                return self.backup_renderer.render(
                    request, data, response_status=response_status
                )
            raise error


api = NinjaAPI(
    title="PokeAPI",
    version="1.0.0",
    description="API responsible for endpoints for PokeAPI.",
    renderer=ORJSONRenderer(),
)

api.add_router("", router)
