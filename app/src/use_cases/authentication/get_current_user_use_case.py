from app.src.common.exception import NotFoundError
from app.src.domain.entities.user import User
from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.presentation.core.config import settings
from jose import JWTError, jwt

class GetCurrentUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    def execute(self, user_id: int) -> User:

        user = self.user_repository.select_user_by_id(user_id)
        if not user or not user.is_active:
            raise NotFoundError("user", user_id)

        return user
