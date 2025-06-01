import logging

from django.db import transaction

from django_pokeapi.apps.pokeapi import models
from django_pokeapi.apps.pokeapi.ipc.dto.abilities import Ability
from django_pokeapi.apps.pokeapi.ipc.dto.pokemon import PokemonDTO
from django_pokeapi.apps.pokeapi.ipc.dto.types import PokemonType

_log = logging.getLogger(__name__)


def bulk_save_all_data(
    types_data: list[PokemonType],
    abilities_data: list[Ability],
    pokemon_data: list[PokemonDTO],
) -> None:
    """Bulk save all fetched data to database using optimized operations.

    Args:
        types_data: List of PokemonType data to save
        abilities_data: List of Ability data to save
        pokemon_data: List of Pokemon data to save
    """
    # Bulk save types
    if types_data:
        _log.info("Bulk saving %d types...", len(types_data))
        bulk_save_types(types_data)
        _log.info("Successfully bulk saved %d types", len(types_data))

    # Bulk save abilities
    if abilities_data:
        _log.info("Bulk saving %d abilities...", len(abilities_data))
        bulk_save_abilities(abilities_data)
        _log.info("Successfully bulk saved %d abilities", len(abilities_data))

    # Bulk save Pokemon
    if pokemon_data:
        _log.info("Bulk saving %d Pokemon...", len(pokemon_data))
        bulk_save_pokemon_with_relations(pokemon_data)
        _log.info("Successfully bulk saved %d Pokemon", len(pokemon_data))


@transaction.atomic
def bulk_save_types(types_data: list[PokemonType]) -> None:
    """Bulk save Pokemon types to database.

    Args:
        types_data: List of PokemonType data to save
    """
    type_objects = []
    for type_data in types_data:
        type_obj = models.PokemonType(
            id=type_data.id,
            name=type_data.name,
            damage_relations=type_data.damage_relations.model_dump(),
            generation_id=(
                int(type_data.generation.url.split("/")[-2])
                if type_data.generation
                else None
            ),
            move_damage_class=(
                type_data.move_damage_class.name
                if type_data.move_damage_class
                else None
            ),
        )
        type_objects.append(type_obj)

    models.PokemonType.objects.bulk_create(
        type_objects,
        update_conflicts=True,
        update_fields=["damage_relations", "generation_id", "move_damage_class"],
        unique_fields=["id"],
    )


@transaction.atomic
def bulk_save_abilities(abilities_data: list[Ability]) -> None:
    """Bulk save Pokemon abilities to database.

    Args:
        abilities_data: List of Ability data to save
    """
    ability_objects = []
    for ability_data in abilities_data:
        ability_obj = models.PokemonAbility(
            id=ability_data.id,
            name=ability_data.name,
            is_main_series=ability_data.is_main_series,
            generation_id=(
                int(ability_data.generation.url.split("/")[-2])
                if ability_data.generation
                else None
            ),
            effect_entries=[
                entry.model_dump() for entry in ability_data.effect_entries
            ],
            effect_changes=ability_data.effect_changes,
            flavor_text_entries=[
                entry.model_dump() for entry in ability_data.flavor_text_entries
            ],
        )
        ability_objects.append(ability_obj)

    models.PokemonAbility.objects.bulk_create(
        ability_objects,
        update_conflicts=True,
        update_fields=[
            "is_main_series",
            "generation_id",
            "effect_entries",
            "effect_changes",
            "flavor_text_entries",
        ],
        unique_fields=["id"],
    )


@transaction.atomic
def bulk_save_pokemon_with_relations(pokemon_data: list[PokemonDTO]) -> None:
    """Bulk save Pokemon with their type and ability relations.

    Args:
        pokemon_data: List of Pokemon data to save
    """
    # Step 1: Bulk create/update Pokemon objects
    pokemon_objects = []
    for pokemon in pokemon_data:
        pokemon_obj = models.Pokemon(
            id=pokemon.id,
            name=pokemon.name,
            base_experience=pokemon.base_experience,
            height=pokemon.height,
            is_default=pokemon.is_default,
            order=pokemon.order,
            weight=pokemon.weight,
            forms=[form.model_dump() for form in pokemon.forms],
            held_items=[hi.model_dump() for hi in pokemon.held_items],
            location_area_encounters=pokemon.location_area_encounters,
            moves=[move.model_dump() for move in pokemon.moves],
            species_data=pokemon.species.model_dump(),
            sprites=pokemon.sprites.model_dump(),
            stats=[stat.model_dump() for stat in pokemon.stats],
        )
        pokemon_objects.append(pokemon_obj)

    models.Pokemon.objects.bulk_create(
        pokemon_objects,
        update_conflicts=True,
        update_fields=[
            "base_experience",
            "height",
            "is_default",
            "order",
            "weight",
            "forms",
            "held_items",
            "location_area_encounters",
            "moves",
            "species_data",
            "sprites",
            "stats",
        ],
        unique_fields=["id"],
    )

    # Step 2: Clear existing relations and bulk create new ones
    pokemon_ids = [p.id for p in pokemon_data]

    # Clear existing type relations
    models.PokemonTypeRelation.objects.filter(pokemon_id__in=pokemon_ids).delete()

    # Bulk create type relations
    type_relations = []
    for pokemon in pokemon_data:
        for type_data in pokemon.types:
            # Ensure the type exists (get_or_create the referenced types)
            pokemon_type, _ = models.PokemonType.objects.get_or_create(
                name=type_data.type.name,
                defaults={"id": int(type_data.type.url.split("/")[-2])},
            )

            type_relations.append(
                models.PokemonTypeRelation(
                    pokemon_id=pokemon.id,
                    pokemon_type=pokemon_type,
                    slot=type_data.slot,
                )
            )

    if type_relations:
        models.PokemonTypeRelation.objects.bulk_create(type_relations)

    # Clear existing ability relations
    models.PokemonAbilityRelation.objects.filter(pokemon_id__in=pokemon_ids).delete()

    # Bulk create ability relations
    ability_relations = []
    for pokemon in pokemon_data:
        for ability_data in pokemon.abilities:
            # Ensure the ability exists
            ability, _ = models.PokemonAbility.objects.get_or_create(
                name=ability_data.ability.name,
                defaults={"id": int(ability_data.ability.url.split("/")[-2])},
            )

            ability_relations.append(
                models.PokemonAbilityRelation(
                    pokemon_id=pokemon.id,
                    ability=ability,
                    slot=ability_data.slot,
                    is_hidden=ability_data.is_hidden,
                )
            )

    if ability_relations:
        models.PokemonAbilityRelation.objects.bulk_create(ability_relations)
