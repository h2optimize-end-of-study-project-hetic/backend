from typing import List, Optional
from abc import ABC, abstractmethod

from app.src.domain.entities.tag import Tag

class TagRepository(ABC):
    @abstractmethod
    def create_tag(self, tag: Tag) -> Tag:
        pass

    @abstractmethod
    def select_tags(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Optional[Tag]]:
        pass

    @abstractmethod
    def select_tag_by_id(self, tag_id: int) -> Tag:
        pass

    @abstractmethod
    def select_tag_by_src_address(self, tag_src_address: str) -> Tag:
        pass

    @abstractmethod
    def update_tag(self, tag_id: int) -> Tag:
        pass

    @abstractmethod
    def delete_tag(self, tag_id: int) -> bool:
        pass
