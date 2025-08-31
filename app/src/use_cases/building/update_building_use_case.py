from app.src.domain.entities.building import Building
from app.src.domain.interface_repositories.building_repository import BuildingRepository


class UpdateBuildingUseCase:
    def __init__(self, building_repository: BuildingRepository):
        self.building_repository = building_repository

    def execute(self, building_id: int, building_data: dict) -> Building:
        return self.building_repository.update_building(building_id, building_data)

    def get(self, building_id: int) -> Building:
        building = self.building_repository.select_building_by_id(building_id)

        return building
