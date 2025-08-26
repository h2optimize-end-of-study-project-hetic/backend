from app.src.common.exception import NotFoundError, UpdateFailedError
from passlib.hash import bcrypt

class UpdateUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id: int, user_data: dict):
        try:
            if "password" in user_data and user_data["password"]:
                user_data["password"] = bcrypt.hash(user_data["password"])
            updated_user = self.user_repository.update_user(user_id, user_data)
            if not updated_user:
                raise NotFoundError(f"User with ID {user_id} not found")
            return updated_user
        except NotFoundError:
            raise
        except Exception as e:
            raise UpdateFailedError("User", str(e)) from e