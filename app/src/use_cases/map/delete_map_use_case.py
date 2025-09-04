from app.src.domain.interface_repositories.map_repository import MapRepository


class DeleteMapUseCase:
    def __init__(self, map_repository: MapRepository):
        self.map_repository = map_repository

    def execute(self, map_id: int) -> bool:
        return self.map_repository.delete_map(map_id)
