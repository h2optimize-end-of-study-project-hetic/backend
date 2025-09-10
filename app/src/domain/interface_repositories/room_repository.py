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


    @abstractmethod
    def get_room_by_position(self, position: int) -> Room | None:
        pass

    @abstractmethod
    def select_rooms_with_tags(self, cursor: int | None, limit: int) -> list[Room]:
        pass

    @abstractmethod
    def paginate_rooms_with_tags(self, cursor: int | None, limit: InterruptedError) -> tuple[list[Room], int, Room | None, Room | None]:       
        pass


