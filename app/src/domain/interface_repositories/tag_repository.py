from abc import ABC, abstractmethod
from datetime import datetime

from app.src.domain.entities.tag import Tag


class TagRepository(ABC):
    @abstractmethod
    def create_tag(self, tag: Tag) -> Tag:
        pass

    @abstractmethod
    def paginate_tags(self, cursor: int | None, limit: int, with_rooms: bool = False) -> tuple[list[Tag], int, Tag | None, Tag | None]:
        pass

    @abstractmethod
    def select_tags(self, offset: int | None = None, limit: int | None = None, with_rooms: bool = False) -> list[Tag | None]:
        pass

    @abstractmethod
    def count_all_tags(self) -> int:
        pass

    @abstractmethod
    def select_tag_by_id(self, tag_id: int, with_rooms: bool = False) -> Tag:
        pass

    @abstractmethod
    def select_tag_by_src_address(self, tag_src_address: str) -> Tag:
        pass

    @abstractmethod
    def update_tag(self, tag_id: int, tag_data: dict) -> Tag:
        pass

    @abstractmethod
    def delete_tag(self, tag_id: int) -> bool:
        pass

    @abstractmethod
    def get_tag_by_position(self, position: int) -> Tag:
        pass

    @abstractmethod
    def create_with_room_link(self, tag: Tag, room_id: int, start_at: datetime, end_at: datetime | None = None) -> Tag: 
        pass
