from app.src.domain.entities.map import Map
from app.src.domain.interface_repositories.map_repository import MapRepository


class GetMapByIdUseCase:
    def __init__(self, map_repository: MapRepository):
        self.map_repository = map_repository

    def execute(self, map_id: int) -> Map:
        map = self.map_repository.select_map_by_id(map_id)

        return map
