import logging

from psycopg2 import errors
from sqlalchemy import func, text
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.src.domain.entities.user import User
from app.src.infrastructure.db.models.user_model import UserModel
from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.common.exception import (
    AlreadyExistsError,
    CreationFailedError,
    DeletionFailedError,
    ForeignKeyConstraintError,
    NotFoundError,
    UpdateFailedError,
)

logger = logging.getLogger(__name__)


class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        pass


    def paginate_users(self, cursor: int | None, limit: int) -> tuple[list[User], int, User | None, User | None]:
        pass


    def select_users(self, offset: int | None = None, limit: int | None = None) -> list[User | None]:
        pass


    def select_user_by_id(self, user_id: int) -> User:
        user_model = self.session.get(UserModel, 1) # to remove
        if not user_model:
            raise NotFoundError("User", user_id)

        return User(**user_model.model_dump())

    def select_user_by_email(self, user_email: str) -> User:
        pass


    def update_user(self, user_id: int, user_data: dict) -> User:
        pass


    def delete_user(self, user_id: int) -> bool:
        pass
