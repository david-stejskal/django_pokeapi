from django.http import Http404, HttpRequest
from ninja import Query, Router

from django_pokeapi.apps.pokeapi import operations
from django_pokeapi.apps.pokeapi.dto.api_dto import (
    AbilityDTO,
    PokemonComparisonDTO,
    PokemonListDTO,
    PokemonRequestDTO,
    TypeDTO,
)
from django_pokeapi.apps.pokeapi.ipc.dto.pokemon import PokemonDTO

router = Router(tags=["pokemon"])


# Pokemon endpoints
@router.get("/pokemon/all", response=list[PokemonListDTO])
def get_pokemon_list(
    request: HttpRequest, offset: int = 0, limit: int = 100
) -> list[PokemonListDTO]:
    """Get list of all Pokemon with pagination.

    Args:
        request (HttpRequest): Request object (not used)
        offset (int): Starting position (which Pokemon ID to start from)
        limit (int): Maximum number of Pokemon to return (when set to 0, all Pokemon are returned)

    Returns:
        list[PokemonListDTO]: List with prefetched relations and applied pagination
    """
    return operations.get_pokemon_list(offset, limit)


@router.get("/pokemon", response=PokemonDTO)
def get_pokemon_detail(request, pokemonrouter: Query[PokemonRequestDTO]) -> PokemonDTO:
    """Get detailed information about a specific Pokemon by ID or name.
    Either name or id must be provided.
    """
    return operations.get_pokemon(pokemonrouter)


@router.get(
    "/pokemon/compare",
    response=PokemonComparisonDTO,
)
def compare_pokemon(
    request: HttpRequest, pokemon1_name: str, pokemon2_name: str
) -> PokemonComparisonDTO:
    """Compare Pokemon 1 stats with Pokemon 2 stats."""
    comparison = operations.compare_pokemon_stats(pokemon1_name, pokemon2_name)
    if not comparison:
        raise Http404("One or both Pokemon not found")

    return comparison


# Type endpoints
@router.get("/types", response=list[TypeDTO])
def list_types(request: HttpRequest):
    """Get list of all Pokemon types."""
    types = operations.get_all_types()
    return types


@router.get("/types/{type_name}", response=TypeDTO)
def get_type_details(request: HttpRequest, type_name: str) -> TypeDTO:
    """Get detailed type information."""
    type_data = operations.get_type_details(type_name)
    if not type_data:
        raise Http404("Type not found")

    return type_data


# Ability endpoints
@router.get("/abilities", response=list[AbilityDTO])
def list_abilities(request: HttpRequest, offset: int = 0, limit: int = 20):
    """Get list of all Pokemon abilities with pagination.

    Args:
        request (HttpRequest): Request object (not used)
        offset (int): Starting position (which Ability ID to start from)
        limit (int): Maximum number of Abilities to return
            (when set to 0, all Abilities are returned)

    Returns:
        list[AbilityDTO]: List with applied pagination
    """
    abilities = operations.get_all_abilities(offset, limit)

    return abilities


@router.get("/abilities/{ability_name}", response=AbilityDTO)
def get_ability_details(request: HttpRequest, ability_name: str) -> AbilityDTO:
    """Get detailed ability information."""
    ability_data = operations.get_ability_details(ability_name)
    if not ability_data:
        raise Http404("Ability not found")

    return ability_data
