from abc import ABC, abstractmethod

from app.src.domain.entities.building import Building


class BuildingRepository(ABC):
    @abstractmethod
    def create_building(self, building: Building) -> Building:
        pass

    @abstractmethod
    def paginate_buildings(self, cursor: int | None, limit: int) -> tuple[list[Building], int, Building | None, Building | None]:
        pass

    @abstractmethod
    def select_buildings(self, offset: int | None = None, limit: int | None = None) -> list[Building | None]:
        pass

    @abstractmethod
    def count_all_buildings(self) -> int:
        pass

    @abstractmethod
    def select_building_by_id(self, building_id: int) -> Building:
        pass

    @abstractmethod
    def update_building(self, building_id: int, building_data: dict) -> Building:
        pass

    @abstractmethod
    def delete_building(self, building_id: int) -> bool:
        pass

    @abstractmethod
    def get_building_by_position(self, position: int) -> Building:
        pass

    @abstractmethod
    def get_building(self, position: int) -> Building:
        pass
