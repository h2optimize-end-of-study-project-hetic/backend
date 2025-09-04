from abc import ABC, abstractmethod

from app.src.domain.entities.user_group import UserGroup


class UserGroupRepository(ABC):
    @abstractmethod
    def create_user_group(self, user_group: UserGroup) -> UserGroup:
        pass

    @abstractmethod
    def paginate_user_groups(self, cursor: int | None, limit: int) -> tuple[list[UserGroup], int, UserGroup | None, UserGroup | None]:
        pass

    @abstractmethod
    def select_user_groups(self, offset: int | None = None, limit: int | None = None) -> list[UserGroup | None]:
        pass

    @abstractmethod
    def count_all_user_groups(self) -> int:
        pass

    @abstractmethod
    def select_user_group_by_id(self, user_group_id: int) -> UserGroup:
        pass

    @abstractmethod
    def update_user_group(self, user_group_id: int, user_group_data: dict) -> UserGroup:
        pass

    @abstractmethod
    def delete_user_group(self, user_group_id: int) -> bool:
        pass

    @abstractmethod
    def get_user_group_by_position(self, position: int) -> UserGroup:
        pass

    @abstractmethod
    def get_user_group(self, position: int) -> UserGroup:
        pass
