from ninja import Router

from .pokeapi import router

api_pokeapi_router = Router()
api_pokeapi_router.add_router("", router)
