from ninja import NinjaAPI

# from django_pokeapi.apps.pokeapi.api import api_pokeapi_router

api = NinjaAPI(
    title="PokeAPI",
    version="1.0.0",
    description="API responsible for endpoints for PokeAPI.",
)

# api.add_router("", api_pokeapi_router)
