from app.src.common.exception import NotFoundError
from app.src.domain.entities.user import User
from app.src.domain.interface_repositories.user_repository import UserRepository
from app.src.presentation.core.config import settings
from jose import JWTError, jwt

class GetCurrentUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, token: str) -> User:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str | None = payload.get("sub")


            if user_id is None:
                raise NotFoundError("user", token)
        except JWTError:
            raise NotFoundError("user", token)
        
        user = self.user_repository.select_user_by_id(user_id)

        if user is None:
            raise NotFoundError("user", token)
        return user
