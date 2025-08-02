from sqlmodel import Session, select
from typing import List, Optional

from app.src.domain.entities.user import User
from app.src.infrastructure.db.models.user_model import UserModel
from app.src.domain.interface_repositories.user_repository import UserRepository

class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        pass

    def select_users(self, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Optional[User]]:
        pass

    def select_user_by_id(self, user_id: int) -> User:
        statement = select(UserModel).where(UserModel.id == user_id)
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError(f"User with ID {user_id} not found")
        
        return User(
            id=result.id,
            email=result.email,
        )


    def select_user_by_src_address(self, user_src_address: str) -> User:
        pass

    def update_user(self, user_id: int) -> User:
        pass

    def delete_user(self, user_id: int) -> bool:
        pass