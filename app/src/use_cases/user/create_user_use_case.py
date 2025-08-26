from app.src.common.exception import AlreadyExistsError, CreationFailedError
from passlib.hash import bcrypt

class CreateUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user):
        try:
            existing_user = self.user_repository.select_user_by_src_address(user.email)
            if existing_user:
                raise AlreadyExistsError(f"User with email {user.email} already exists")
        except Exception:
            pass

        try:
            user.password = bcrypt.hash(user.password)
            new_user = self.user_repository.create_user(user)
            if not new_user:
                raise CreationFailedError("User", "Failed to create user")
            return new_user
        except AlreadyExistsError:
            raise
        except Exception as e:
            raise CreationFailedError("User", str(e)) from e