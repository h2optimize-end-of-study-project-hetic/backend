from app.src.domain.entities.map import Map
from app.src.domain.interface_repositories.map_repository import MapRepository


class CreateMapUseCase:
    def __init__(self, map_repository: MapRepository):
        self.map_repository = map_repository

    def execute(self, map: Map) -> Map:
        return self.map_repository.create_map(map)
