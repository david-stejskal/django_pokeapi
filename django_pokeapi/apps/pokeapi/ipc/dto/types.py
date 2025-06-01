from typing import Optional

from pydantic import BaseModel

from .pokemon import NamedAPIResource


class TypeRelations(BaseModel):
    """Type effectiveness relations."""

    no_damage_to: list[NamedAPIResource]
    half_damage_to: list[NamedAPIResource]
    double_damage_to: list[NamedAPIResource]
    no_damage_from: list[NamedAPIResource]
    half_damage_from: list[NamedAPIResource]
    double_damage_from: list[NamedAPIResource]


class TypePokemon(BaseModel):
    """Pokemon with this type."""

    slot: int
    pokemon: NamedAPIResource


class PokemonType(BaseModel):
    """Complete Type data from PokeAPI."""

    id: int
    name: str
    damage_relations: TypeRelations
    pokemon: list[TypePokemon]
    moves: list[NamedAPIResource]
    generation: NamedAPIResource
    move_damage_class: Optional[NamedAPIResource] = None


class TypeListResponse(BaseModel):
    """Paginated list of Types."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[NamedAPIResource]
