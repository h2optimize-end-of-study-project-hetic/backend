import logging
import math
from dataclasses import dataclass

from app.src.domain.entities.map import Map
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.map_repository import MapRepository

logger = logging.getLogger(__name__)

@dataclass
class PaginatedMap:
    maps: list[Map]
    total: int| None
    chunk_size: int| None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetMapListUseCase:
    def __init__(self, map_repository: MapRepository):
        self.map_repository = map_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedMap:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "Map pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        maps, total, first_map, last_map = self.map_repository.paginate_maps(decoded_cursor, (limit + 1))

        next_map = None
        if len(maps) == (limit + 1):
            next_map = maps.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_map.id} if first_map else None
        last_cursor = {"id": last_map.id} if last_map else None
        next_cursor = {"id": next_map.id} if next_map else None

        return PaginatedMap(
            maps=maps,
            total=total,
            chunk_size=len(maps),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
