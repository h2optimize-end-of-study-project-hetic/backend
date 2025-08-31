from app.src.domain.entities.building import Building
from app.src.domain.interface_repositories.building_repository import BuildingRepository


class CreateBuildingUseCase:
    def __init__(self, building_repository: BuildingRepository):
        self.building_repository = building_repository

    def execute(self, building: Building) -> Building:
        return self.building_repository.create_building(building)
