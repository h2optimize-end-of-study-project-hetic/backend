from app.src.domain.entities.map import Map
from app.src.domain.interface_repositories.map_repository import MapRepository


class UpdateMapUseCase:
    def __init__(self, map_repository: MapRepository):
        self.map_repository = map_repository

    def execute(self, map_id: int, map_data: dict) -> Map:
        return self.map_repository.update_map(map_id, map_data)

    def get(self, map_id: int) -> Map:
        map = self.map_repository.select_map_by_id(map_id)

        return map
