import asyncio
import logging
from typing import Awaitable, Callable, TypeVar, Union

import httpx

from .dto.abilities import Ability, AbilityListResponse
from .dto.pokemon import PokemonDTO, PokemonListResponseDTO
from .dto.types import PokemonType, TypeListResponse

LIMIT = 100000
OFFSET = 0

_log = logging.getLogger(__name__)

T = TypeVar("T")


class AsyncPokeAPIClient:
    """Asynchronous HTTP client for PokeAPI with typed responses."""

    def __init__(
        self,
        async_client: httpx.AsyncClient,
        base_url: str = "https://pokeapi.co/api/v2/",
    ) -> None:
        """Initialize asynchronous PokeAPI client.

        Args:
            async_client: Pre-configured httpx.AsyncClient instance
            base_url: Base URL for PokeAPI endpoints
        """
        self.base_url = base_url
        self.client = async_client

    async def _make_request(self, endpoint: str) -> dict:
        """Make asynchronous HTTP request to PokeAPI endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            JSON response data

        Raises:
            httpx.HTTPError: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def _make_batch_requests(
        self,
        ids: list[int],
        request_func: Callable[[int], Awaitable[T]],
        chunk_size: int = 30,
        chunk_delay: float = 0.1,
    ) -> list[T]:
        """Make batch requests with chunking to avoid overwhelming the server.

        Args:
            ids: List of IDs to fetch
            request_func: Async function that takes ID and returns the resource
            chunk_size: Number of requests per chunk
            chunk_delay: Delay between chunks in seconds

        Returns:
            List of fetched resources
        """
        all_results = []

        for i in range(0, len(ids), chunk_size):
            chunk = ids[i : i + chunk_size]
            chunk_num = i // chunk_size + 1
            total_chunks = (len(ids) - 1) // chunk_size + 1

            _log.info("Fetching chunk %d/%d", chunk_num, total_chunks)

            tasks = [request_func(item_id) for item_id in chunk]
            chunk_results = await asyncio.gather(*tasks, return_exceptions=False)
            all_results.extend(chunk_results)

            if i + chunk_size < len(ids):
                await asyncio.sleep(chunk_delay)

        return all_results

    # Pokemon endpoints
    async def get_pokemon(self, pokemon_id: Union[int, str]) -> PokemonDTO:
        """Get Pokemon by ID or name asynchronously.

        Args:
            pokemon_id: Pokemon ID or name

        Returns:
            Pokemon data
        """
        data = await self._make_request(f"pokemon/{pokemon_id}/")
        return PokemonDTO(**data)

    async def get_all_pokemon(
        self, limit: int = LIMIT, offset: int = OFFSET
    ) -> PokemonListResponseDTO:
        """Get all Pokemon (up to limit) asynchronously.

        Args:
            limit: Maximum number of Pokemon to fetch
            offset: Starting index

        Returns:
            Complete Pokemon list
        """
        data = await self._make_request(f"pokemon/?limit={limit}&offset={offset}")
        return PokemonListResponseDTO(**data)

    async def get_multiple_pokemon(self, pokemon_ids: list[int]) -> list[PokemonDTO]:
        """Get multiple Pokemon concurrently by their IDs.

        Args:
            pokemon_ids: List of Pokemon IDs to fetch

        Returns:
            List of Pokemon data
        """
        return await self._make_batch_requests(
            pokemon_ids,
            self.get_pokemon,
        )

    # Type endpoints
    async def get_type_by_id(self, type_id: Union[int, str]) -> PokemonType:
        """Get Type by ID or name asynchronously.

        Args:
            type_id: Type ID or name

        Returns:
            Type data
        """
        data = await self._make_request(f"type/{type_id}/")
        return PokemonType(**data)

    async def get_all_types(
        self, limit: int = LIMIT, offset: int = OFFSET
    ) -> TypeListResponse:
        """Get all Types asynchronously.

        Args:
            limit: Maximum number of Types to fetch
            offset: Starting index

        Returns:
            Complete Type list
        """
        data = await self._make_request(f"type/?limit={limit}&offset={offset}")
        return TypeListResponse(**data)

    async def get_multiple_types(self, type_ids: list[int]) -> list[PokemonType]:
        """Get multiple Types concurrently by their IDs.

        Args:
            type_ids: List of Type IDs to fetch

        Returns:
            List of Type data
        """
        return await self._make_batch_requests(type_ids, self.get_type_by_id)

    # Ability endpoints
    async def get_ability(self, ability_id: Union[int, str]) -> Ability:
        """Get Ability by ID or name asynchronously.

        Args:
            ability_id: Ability ID or name

        Returns:
            Ability data
        """
        data = await self._make_request(f"ability/{ability_id}/")
        return Ability(**data)

    async def get_all_abilities(
        self, limit: int = LIMIT, offset: int = OFFSET
    ) -> AbilityListResponse:
        """Get all Abilities asynchronously.

        Args:
            limit: Maximum number of Abilities to fetch
            offset: Starting index

        Returns:
            Complete Ability list
        """
        data = await self._make_request(f"ability/?limit={limit}&offset={offset}")
        return AbilityListResponse(**data)

    async def get_multiple_abilities(self, ability_ids: list[int]) -> list[Ability]:
        """Get multiple Abilities concurrently by their IDs.

        Args:
            ability_ids: List of Ability IDs to fetch

        Returns:
            List of Ability data
        """
        return await self._make_batch_requests(ability_ids, self.get_ability)
