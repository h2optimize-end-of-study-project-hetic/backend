from abc import ABC, abstractmethod

from app.src.domain.entities.event_room import EventRoom


class EventRoomRepository(ABC):
    @abstractmethod
    def create_event_room(self, event_room: EventRoom) -> EventRoom:
        pass

    @abstractmethod
    def paginate_event_rooms(self, cursor: int | None, limit: int) -> tuple[list[EventRoom], int, EventRoom | None, EventRoom | None]:
        pass

    @abstractmethod
    def select_event_rooms(self, offset: int | None = None, limit: int | None = None) -> list[EventRoom | None]:
        pass

    @abstractmethod
    def count_all_event_rooms(self) -> int:
        pass

    @abstractmethod
    def select_event_room_by_id(self, event_room_id: int) -> EventRoom:
        pass

    @abstractmethod
    def update_event_room(self, event_room_id: int, event_room_data: dict) -> EventRoom:
        pass

    @abstractmethod
    def delete_event_room(self, event_room_id: int) -> bool:
        pass

    @abstractmethod
    def get_event_room_by_position(self, position: int) -> EventRoom:
        pass

    @abstractmethod
    def get_event_room(self, position: int) -> EventRoom:
        pass
