from typing import List, Optional
from abc import ABC, abstractmethod

from app.src.domain.entities.tag import Tag

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, tag: Tag) -> Tag:
        pass

    @abstractmethod
    def select_users(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Optional[Tag]]:
        pass

    @abstractmethod
    def select_user_by_id(self, tag_id: int) -> Tag:
        pass

    @abstractmethod
    def select_user_by_src_address(self, tag_src_address: str) -> Tag:
        pass

    @abstractmethod
    def update_user(self, tag_id: int) -> Tag:
        pass

    @abstractmethod
    def delete_user(self, tag_id: int) -> bool:
        pass
