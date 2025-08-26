from abc import ABC, abstractmethod
from app.src.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def select_users(self, offset: int | None = None, limit: int | None = None) -> list[User | None]:
        pass

    @abstractmethod
    def select_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def select_user_by_src_address(self, user_src_address: str) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass
