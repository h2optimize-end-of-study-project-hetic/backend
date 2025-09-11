from abc import ABC, abstractmethod
from datetime import datetime

from app.src.domain.entities.room_tag import RoomTag


class RoomTagRepository(ABC):
    @abstractmethod
    def create_roomtag(self, roomtag: RoomTag) -> RoomTag:
        pass

    @abstractmethod
    def paginate_roomtag(self, cursor: int | None, limit: int, active_only: bool = False) -> tuple[list[RoomTag], int, RoomTag | None, RoomTag | None]:
        pass

    @abstractmethod
    def select_roomtag(self, offset: int | None = None, limit: int | None = None, active_only: bool = False) -> list[RoomTag | None]:
        pass

    @abstractmethod
    def count_all_roomtag(self, active_only: bool = False) -> int:
        pass

    @abstractmethod
    def select_roomtag_by_id(self, roomtag_id: int) -> RoomTag:
        pass

    @abstractmethod
    def update_roomtag(self, roomtag_id: int, roomtag_data: dict) -> RoomTag:
        pass

    @abstractmethod
    def delete_roomtag(self, roomtag_id: int) -> bool:
        pass

    @abstractmethod
    def get_roomtag_by_position(self, position: int, active_only: bool = False) -> RoomTag:
        pass

    @abstractmethod
    def update_roomtag_by_tag_id_room_id(self, tag_id: int, room_id: int, start_at: datetime, end_at: datetime | None) -> RoomTag:
        pass
