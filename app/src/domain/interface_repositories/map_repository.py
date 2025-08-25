from abc import ABC, abstractmethod

from app.src.domain.entities.map import Map


class MapRepository(ABC):
    @abstractmethod
    def create_map(self, map: Map) -> Map:
        pass

    @abstractmethod
    def paginate_maps(self, cursor: int | None, limit: int) -> tuple[list[Map], int, Map | None, Map | None]:
        pass

    @abstractmethod
    def select_maps(self, offset: int | None = None, limit: int | None = None) -> list[Map | None]:
        pass

    @abstractmethod
    def count_all_maps(self) -> int:
        pass

    @abstractmethod
    def select_map_by_id(self, map_id: int) -> Map:
        pass

    @abstractmethod
    def update_map(self, map_id: int, map_data: dict) -> Map:
        pass

    @abstractmethod
    def delete_map(self, map_id: int) -> bool:
        pass

    @abstractmethod
    def get_map_by_position(self, position: int) -> Map:
        pass

    @abstractmethod
    def get_map(self, position: int) -> Map:
        pass
