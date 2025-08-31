import logging
import math
from dataclasses import dataclass

from app.src.domain.entities.building import Building
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.building_repository import BuildingRepository

logger = logging.getLogger(__name__)

@dataclass
class PaginatedBuilding:
    buildings: list[Building]
    total: int| None
    chunk_size: int| None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetBuildingListUseCase:
    def __init__(self, building_repository: BuildingRepository):
        self.building_repository = building_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedBuilding:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "Building pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        buildings, total, first_building, last_building = self.building_repository.paginate_buildings(decoded_cursor, (limit + 1))

        next_building = None
        if len(buildings) == (limit + 1):
            next_building = buildings.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_building.id} if first_building else None
        last_cursor = {"id": last_building.id} if last_building else None
        next_cursor = {"id": next_building.id} if next_building else None

        return PaginatedBuilding(
            buildings=buildings,
            total=total,
            chunk_size=len(buildings),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
