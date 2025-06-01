from django.db.models import QuerySet

from django_pokeapi.apps.pokeapi import models

from .dto.api_dto import (
    AbilityDTO,
    PokemonComparisonDTO,
    PokemonComparisonSummaryDTO,
    PokemonListDTO,
    PokemonRequestDTO,
    TypeDTO,
)
from .ipc.dto.pokemon import PokemonDTO


def get_pokemon_list(
    offset: int,
    limit: int,
) -> list[PokemonListDTO]:
    """Get optimized Pokemon list with related data and pagination.

    Args:
        offset: Starting position (which Pokemon ID to start from)
        limit: Maximum number of Pokemon to return (when set to 0, all Pokemon are returned)

    Returns:
        list[PokemonListDTO] with prefetched relations and applied pagination
    """
    # Optimize database queries using select_related and prefetch_related
    pokemon_query = (
        models.Pokemon.objects.select_related()
        .prefetch_related(
            "type_relations__pokemon_type",
            "ability_relations__ability",
        )
        .order_by("id")  # Ensure consistent ordering for offset/limit
    )

    # Apply pagination - if limit is 0, return all Pokemon from offset
    if not limit:
        pokemon_models = pokemon_query[offset:]
    else:
        pokemon_models = pokemon_query[offset : offset + limit]

    return [PokemonListDTO.from_model(pokemon) for pokemon in pokemon_models]


def get_pokemon(pokemon_request: PokemonRequestDTO) -> PokemonDTO:
    """Get Pokemon by id or name with optimized queries.

    Args:
        pokemon_request: Request DTO containing id or name filter

    Returns:
        PokemonDTO instance
    """
    if not pokemon_request.id and not pokemon_request.name:
        raise ValueError("Either id or name must be provided")

    query = models.Pokemon.objects.select_related().prefetch_related(
        "type_relations__pokemon_type",
        "ability_relations__ability",
    )

    if pokemon_request.id:
        pokemon = query.get(id=pokemon_request.id)
    else:
        pokemon = query.get(name__iexact=pokemon_request.name)

    return PokemonDTO.from_model(pokemon)


def search_pokemon_by_type(type_name: str) -> QuerySet[PokemonDTO]:
    """Search Pokemon by type name.

    Args:
        type_name: Type name to search for

    Returns:
        QuerySet of Pokemon with the specified type
    """
    return (
        models.Pokemon.objects.select_related()
        .prefetch_related("types", "pokemon_abilities")
        .filter(types__name__iexact=type_name)
        .distinct()
        .order_by("id")
    )


def search_pokemon_by_ability(ability_name: str) -> QuerySet[PokemonDTO]:
    """Search Pokemon by ability name.

    Args:
        ability_name: Ability name to search for

    Returns:
        QuerySet of Pokemon with the specified ability
    """
    return (
        models.Pokemon.objects.select_related()
        .prefetch_related("types", "pokemon_abilities")
        .filter(pokemon_abilities__name__iexact=ability_name)
        .distinct()
        .order_by("id")
    )


def compare_pokemon_stats(
    pokemon1_name: str, pokemon2_name: str
) -> PokemonComparisonDTO:
    """Compare stats between two Pokemon.

    Args:
        pokemon1_name: First Pokemon request DTO
        pokemon2_name: Second Pokemon request DTO

    Returns:
        Comparison data with stats, types, and differences
    """
    pokemon1 = get_pokemon(PokemonRequestDTO(name=pokemon1_name))
    pokemon2 = get_pokemon(PokemonRequestDTO(name=pokemon2_name))

    # Extract stats for comparison from DTO
    stats1 = {stat.stat.name: stat.base_stat for stat in pokemon1.stats}
    stats2 = {stat.stat.name: stat.base_stat for stat in pokemon2.stats}

    # Extract types from DTO
    types1 = [pokemon_type.type.name for pokemon_type in pokemon1.types]
    types2 = [pokemon_type.type.name for pokemon_type in pokemon2.types]

    comparison = PokemonComparisonDTO(
        pokemon1=PokemonComparisonSummaryDTO(
            id=pokemon1.id,
            name=pokemon1.name,
            height=pokemon1.height,
            weight=pokemon1.weight,
            base_experience=pokemon1.base_experience,
            stats=stats1,
            types=types1,
        ),
        pokemon2=PokemonComparisonSummaryDTO(
            id=pokemon2.id,
            name=pokemon2.name,
            height=pokemon2.height,
            weight=pokemon2.weight,
            base_experience=pokemon2.base_experience,
            stats=stats2,
            types=types2,
        ),
        stat_differences={},
    )

    # Calculate stat differences
    for stat_name in stats1.keys():
        if stat_name in stats2:
            comparison.stat_differences[stat_name] = (
                stats1[stat_name] - stats2[stat_name]
            )

    return comparison


## TYPES


def get_all_types() -> list[TypeDTO]:
    """Get all Pokemon types as simple list of names.

    Returns:
        List of type names sorted by id
    """
    pokemon_types = models.PokemonType.objects.all().order_by("id")
    return [TypeDTO.from_model(pokemon_type) for pokemon_type in pokemon_types]


def get_type_details(type_name: str) -> TypeDTO:
    """Get detailed type information.

    Args:
        type_name: Type name

    Returns:
        Type details
    """
    pokemon_type = models.PokemonType.objects.get(name=type_name)
    return TypeDTO.from_model(pokemon_type)


## ABILITIES


def get_all_abilities(offset: int, limit: int) -> list[AbilityDTO]:
    """Get all Pokemon abilities with pagination.

    Args:
        offset: Starting position (which Ability ID to start from)
        limit: Maximum number of Abilities to return (when set to 0, all Abilities are returned)

    Returns:
        list[AbilityDTO] with applied pagination
    """
    # Optimize database queries and ensure consistent ordering
    abilities_query = models.PokemonAbility.objects.all().order_by("id")

    # Apply pagination - if limit is 0, return all abilities from offset
    if not limit:
        abilities_models = abilities_query[offset:]
    else:
        abilities_models = abilities_query[offset : offset + limit]

    return [AbilityDTO.from_model(ability) for ability in abilities_models]


def get_ability_details(ability_name: str) -> AbilityDTO:
    """Get detailed ability information.

    Args:
        ability_name: Ability name

    Returns:
        Ability details
    """
    ability = models.PokemonAbility.objects.get(name__iexact=ability_name)
    return AbilityDTO.from_model(ability)
