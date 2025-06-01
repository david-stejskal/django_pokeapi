from typing import Optional

from ninja import Schema

from django_pokeapi.apps.pokeapi import models


# Request schemas
class PokemonRequestDTO(Schema):
    name: str | None = None
    id: int | None = None


class PokemonComparisonRequestDTO(Schema):
    pokemon1: PokemonRequestDTO
    pokemon2: PokemonRequestDTO


# Response schemas
class PokemonListDTO(Schema):
    """Pokemon list item schema."""

    id: int
    name: str
    height: int
    weight: int
    base_experience: Optional[int] = None
    sprites: dict
    types: list[str]

    @classmethod
    def from_model(cls, pokemon: models.Pokemon) -> "PokemonListDTO":
        """Create PokemonListDTO from Django model instance.

        Args:
            pokemon: Pokemon model instance with prefetched relations

        Returns:
            PokemonListDTO instance
        """
        # Extract types from type_relations
        types = [
            relation.pokemon_type.name for relation in pokemon.type_relations.all()
        ]

        return cls(
            id=pokemon.id,
            name=pokemon.name,
            height=pokemon.height,
            weight=pokemon.weight,
            base_experience=pokemon.base_experience,
            sprites=pokemon.sprites,
            types=types,
        )


class PokemonComparisonSummaryDTO(Schema):
    """Simplified Pokemon data for comparison."""

    id: int
    name: str
    height: int
    weight: int
    base_experience: Optional[int] = None
    stats: dict
    types: list[str]


class TypeDTO(Schema):
    """Pokemon type schema."""

    id: int
    name: str
    damage_relations: dict
    generation_id: Optional[int] = None
    move_damage_class: Optional[str] = None

    @classmethod
    def from_model(cls, pokemon_type: models.PokemonType) -> "TypeDTO":
        return cls(
            id=pokemon_type.id,
            name=pokemon_type.name,
            damage_relations=pokemon_type.damage_relations,
            generation_id=pokemon_type.generation_id,
            move_damage_class=pokemon_type.move_damage_class,
        )


class AbilityDTO(Schema):
    """Pokemon ability schema."""

    id: int
    name: str
    is_main_series: bool
    generation_id: Optional[int] = None
    effect_entries: list[dict]
    flavor_text_entries: list[dict]

    @classmethod
    def from_model(cls, ability: models.PokemonAbility) -> "AbilityDTO":
        return cls(
            id=ability.id,
            name=ability.name,
            is_main_series=ability.is_main_series,
            generation_id=ability.generation_id,
            effect_entries=ability.effect_entries,
            flavor_text_entries=ability.flavor_text_entries,
        )


class PokemonComparisonDTO(Schema):
    """Pokemon comparison schema."""

    pokemon1: PokemonComparisonSummaryDTO
    pokemon2: PokemonComparisonSummaryDTO
    stat_differences: dict
