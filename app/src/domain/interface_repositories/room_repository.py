from abc import ABC, abstractmethod

from app.src.domain.entities.room import Room


class RoomRepository(ABC):
    @abstractmethod
    def create_room(self, room: Room) -> Room:
        pass

    @abstractmethod
    def select_rooms(self, offset: int | None = None, limit: int | None = None) -> list[Room | None]:
        pass

    @abstractmethod
    def count_all_rooms(self) -> int:
        pass

    @abstractmethod
    def select_room_by_id(self, room_id: int) -> Room:
        pass

    @abstractmethod
    def update_room(self, room_id: int, room_data: dict) -> Room:
        pass

    @abstractmethod
    def delete_room(self, room_id: int) -> bool:
        pass
