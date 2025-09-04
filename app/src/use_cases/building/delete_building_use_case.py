from app.src.domain.interface_repositories.building_repository import BuildingRepository


class DeleteBuildingUseCase:
    def __init__(self, building_repository: BuildingRepository):
        self.building_repository = building_repository

    def execute(self, building_id: int) -> bool:
        return self.building_repository.delete_building(building_id)
