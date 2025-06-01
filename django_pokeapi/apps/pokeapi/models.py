from typing import TYPE_CHECKING

from django.db import models

from django_pokeapi.apps.common.common_models import TrackingleModel

if TYPE_CHECKING:
    from django.db.models import QuerySet


class PokemonType(TrackingleModel):
    name = models.TextField(unique=True)
    damage_relations = models.JSONField(default=dict)
    generation_id = models.IntegerField(null=True, blank=True)
    move_damage_class = models.TextField(null=True, blank=True)

    class Meta:
        db_table = '"pokeapi"."pokemon_types"'
        ordering = ["id"]


class PokemonAbility(TrackingleModel):
    name = models.TextField(unique=True)
    is_main_series = models.BooleanField(default=True)
    generation_id = models.IntegerField(null=True, blank=True)
    effect_entries = models.JSONField(default=list)
    effect_changes = models.JSONField(default=list)
    flavor_text_entries = models.JSONField(default=list)

    class Meta:
        db_table = '"pokeapi"."abilities"'
        ordering = ["id"]


class Pokemon(TrackingleModel):
    name = models.TextField(unique=True)
    base_experience = models.IntegerField(null=True, blank=True)
    height = models.IntegerField()
    is_default = models.BooleanField(default=True)
    order = models.IntegerField()
    weight = models.IntegerField()

    # JSON fields for complex nested data that doesn't need querying
    forms = models.JSONField(default=list)
    held_items = models.JSONField(default=list)
    location_area_encounters = models.URLField(max_length=500)
    moves = models.JSONField(default=list)
    species_data = models.JSONField(default=dict)
    sprites = models.JSONField(default=dict)
    stats = models.JSONField(default=list)

    # Many-to-many relationships
    types = models.ManyToManyField(PokemonType, through="PokemonTypeRelation")
    pokemon_abilities = models.ManyToManyField(
        PokemonAbility, through="PokemonAbilityRelation"
    )

    class Meta:
        db_table = '"pokeapi"."pokemon"'
        ordering = ["id"]


class PokemonTypeRelation(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name="type_relations"
    )
    pokemon_type = models.ForeignKey(
        PokemonType, on_delete=models.CASCADE, related_name="pokemon_relations"
    )
    slot = models.IntegerField()

    class Meta:
        db_table = '"pokeapi"."pokemon_type_relations"'
        unique_together = ["pokemon", "slot"]
        ordering = ["pokemon", "slot"]


class PokemonAbilityRelation(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name="ability_relations"
    )
    ability = models.ForeignKey(
        PokemonAbility, on_delete=models.CASCADE, related_name="pokemon_relations"
    )
    slot = models.IntegerField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        db_table = '"pokeapi"."pokemon_ability_relations"'
        unique_together = ["pokemon", "slot"]
        ordering = ["pokemon", "slot"]
