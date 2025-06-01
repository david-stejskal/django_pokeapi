from typing import Any, Dict, Optional

from pydantic import BaseModel

from django_pokeapi.apps.pokeapi import models


class NamedAPIResource(BaseModel):
    """Basic named API resource reference."""

    name: str
    url: str


class APIResource(BaseModel):
    """Basic API resource reference."""

    url: str


class PokemonSpritesDTO(BaseModel):
    """Pokemon sprite URLs."""

    front_default: Optional[str] = None
    front_shiny: Optional[str] = None
    front_female: Optional[str] = None
    front_shiny_female: Optional[str] = None
    back_default: Optional[str] = None
    back_shiny: Optional[str] = None
    back_female: Optional[str] = None
    back_shiny_female: Optional[str] = None


class PokemonStatDTO(BaseModel):
    """Pokemon stat information."""

    base_stat: int
    effort: int
    stat: NamedAPIResource


class PokemonTypeDTO(BaseModel):
    """Pokemon type information."""

    slot: int
    type: NamedAPIResource


class PokemonAbilityDTO(BaseModel):
    """Pokemon ability information."""

    is_hidden: bool
    slot: int
    ability: NamedAPIResource


class PokemonMoveDTO(BaseModel):
    """Pokemon move information."""

    move: NamedAPIResource


class PokemonHeldItemDTO(BaseModel):
    """Pokemon held item information."""

    item: NamedAPIResource
    version_details: list[Dict[str, Any]]


class PokemonDTO(BaseModel):
    """Complete Pokemon data from PokeAPI."""

    id: int
    name: str
    base_experience: Optional[int] = None
    height: int
    is_default: bool
    order: int
    weight: int
    abilities: list[PokemonAbilityDTO]
    forms: list[NamedAPIResource]
    held_items: list[PokemonHeldItemDTO]
    location_area_encounters: str
    moves: list[PokemonMoveDTO]
    species: NamedAPIResource
    sprites: PokemonSpritesDTO
    stats: list[PokemonStatDTO]
    types: list[PokemonTypeDTO]

    @classmethod
    def from_model(cls, pokemon: "models.Pokemon") -> "PokemonDTO":
        """Create Pokemon DTO from Django model instance.

        Args:
            pokemon: Pokemon model instance with prefetched relations

        Returns:
            PokemonDTO instance
        """
        # Get abilities from PokemonAbilityRelation
        ability_relations = pokemon.ability_relations.all().order_by("slot")
        abilities = [
            PokemonAbilityDTO(
                is_hidden=relation.is_hidden,
                slot=relation.slot,
                ability=NamedAPIResource(
                    name=relation.ability.name,
                    url=f"/api/v2/ability/{relation.ability.id}/",
                ),
            )
            for relation in ability_relations
        ]

        # Convert forms from JSON to NamedAPIResource objects
        forms = [
            NamedAPIResource(name=form.get("name", ""), url=form.get("url", ""))
            for form in pokemon.forms
        ]

        # Convert held_items from JSON to PokemonHeldItem objects
        held_items = [
            PokemonHeldItemDTO(
                item=NamedAPIResource(
                    name=item.get("item", {}).get("name", ""),
                    url=item.get("item", {}).get("url", ""),
                ),
                version_details=item.get("version_details", []),
            )
            for item in pokemon.held_items
        ]

        # Convert moves from JSON to PokemonMove objects
        moves = [
            PokemonMoveDTO(
                move=NamedAPIResource(
                    name=move.get("move", {}).get("name", ""),
                    url=move.get("move", {}).get("url", ""),
                )
            )
            for move in pokemon.moves
        ]

        # Convert species_data from JSON to NamedAPIResource
        species = NamedAPIResource(
            name=pokemon.species_data.get("name", ""),
            url=pokemon.species_data.get("url", ""),
        )

        # Convert sprites from JSON to PokemonSprites object
        sprites_data = pokemon.sprites
        sprites = PokemonSpritesDTO(
            front_default=sprites_data.get("front_default"),
            front_shiny=sprites_data.get("front_shiny"),
            front_female=sprites_data.get("front_female"),
            front_shiny_female=sprites_data.get("front_shiny_female"),
            back_default=sprites_data.get("back_default"),
            back_shiny=sprites_data.get("back_shiny"),
            back_female=sprites_data.get("back_female"),
            back_shiny_female=sprites_data.get("back_shiny_female"),
        )

        # Convert stats from JSON to PokemonStat objects
        stats = [
            PokemonStatDTO(
                base_stat=stat.get("base_stat", 0),
                effort=stat.get("effort", 0),
                stat=NamedAPIResource(
                    name=stat.get("stat", {}).get("name", ""),
                    url=stat.get("stat", {}).get("url", ""),
                ),
            )
            for stat in pokemon.stats
        ]

        # Get types from PokemonTypeRelation
        type_relations = pokemon.type_relations.all().order_by("slot")
        types = [
            PokemonTypeDTO(
                slot=relation.slot,
                type=NamedAPIResource(
                    name=relation.pokemon_type.name,
                    url=f"/api/v2/type/{relation.pokemon_type.id}/",
                ),
            )
            for relation in type_relations
        ]

        return cls(
            id=pokemon.id,
            name=pokemon.name,
            base_experience=pokemon.base_experience,
            height=pokemon.height,
            is_default=pokemon.is_default,
            order=pokemon.order,
            weight=pokemon.weight,
            abilities=abilities,
            forms=forms,
            held_items=held_items,
            location_area_encounters=str(pokemon.location_area_encounters),
            moves=moves,
            species=species,
            sprites=sprites,
            stats=stats,
            types=types,
        )


class PokemonListResponseDTO(BaseModel):
    """List of Pokemon."""

    results: list[NamedAPIResource]
