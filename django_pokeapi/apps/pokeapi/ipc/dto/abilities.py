from typing import Optional

from pydantic import BaseModel

from .pokemon import NamedAPIResource


class AbilityEffectEntry(BaseModel):
    """Ability effect description."""

    effect: str
    short_effect: str
    language: NamedAPIResource


class AbilityFlavorTextEntry(BaseModel):
    """Ability flavor text."""

    flavor_text: str
    language: NamedAPIResource
    version_group: NamedAPIResource


class AbilityPokemon(BaseModel):
    """Pokemon with this ability."""

    is_hidden: bool
    slot: int
    pokemon: NamedAPIResource


class Ability(BaseModel):
    """Complete Ability data from PokeAPI."""

    id: int
    name: str
    is_main_series: bool
    generation: NamedAPIResource
    effect_entries: list[AbilityEffectEntry]
    effect_changes: list[dict]  # Complex nested structure
    flavor_text_entries: list[AbilityFlavorTextEntry]
    pokemon: list[AbilityPokemon]


class AbilityListResponse(BaseModel):
    """Paginated list of Abilities."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[NamedAPIResource]
