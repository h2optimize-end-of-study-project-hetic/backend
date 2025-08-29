from abc import ABC, abstractmethod

from app.src.domain.entities.event import Event


class EventRepository(ABC):
    @abstractmethod
    def create_event(self, event: Event) -> Event:
        pass

    @abstractmethod
    def paginate_events(self, cursor: int | None, limit: int) -> tuple[list[Event], int, Event | None, Event | None]:
        pass

    @abstractmethod
    def select_events(self, offset: int | None = None, limit: int | None = None) -> list[Event | None]:
        pass

    @abstractmethod
    def count_all_events(self) -> int:
        pass

    @abstractmethod
    def select_event_by_id(self, event_id: int) -> Event:
        pass

    @abstractmethod
    def update_event(self, event_id: int, event_data: dict) -> Event:
        pass

    @abstractmethod
    def delete_event(self, event_id: int) -> bool:
        pass

    @abstractmethod
    def get_event_by_position(self, position: int) -> Event:
        pass

    @abstractmethod
    def get_event(self, position: int) -> Event:
        pass
