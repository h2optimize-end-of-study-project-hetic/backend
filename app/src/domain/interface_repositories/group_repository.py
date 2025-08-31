from abc import ABC, abstractmethod

from app.src.domain.entities.group import Group


class GroupRepository(ABC):
    @abstractmethod
    def create_group(self, group: Group) -> Group:
        pass

    @abstractmethod
    def paginate_groups(self, cursor: int | None, limit: int) -> tuple[list[Group], int, Group | None, Group | None]:
        pass

    @abstractmethod
    def select_groups(self, offset: int | None = None, limit: int | None = None) -> list[Group | None]:
        pass

    @abstractmethod
    def count_all_groups(self) -> int:
        pass

    @abstractmethod
    def select_group_by_id(self, group_id: int) -> Group:
        pass

    @abstractmethod
    def update_group(self, group_id: int, group_data: dict) -> Group:
        pass

    @abstractmethod
    def delete_group(self, group_id: int) -> bool:
        pass

    @abstractmethod
    def get_group_by_position(self, position: int) -> Group:
        pass

    @abstractmethod
    def get_group(self, position: int) -> Group:
        pass
