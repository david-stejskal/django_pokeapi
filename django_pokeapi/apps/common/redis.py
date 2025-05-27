from redis.client import Redis

from django_pokeapi import settings

redis: Redis = Redis(
    db=0,
    decode_responses=True,
).from_url(url=f"{settings.REDIS_URL}")
