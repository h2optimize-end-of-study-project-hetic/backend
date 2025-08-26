from app.src.common.exception import NotFoundError, ForeignKeyConstraintError
from sqlalchemy.exc import IntegrityError

class DeleteUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id: int):
        try:
            self.user_repository.delete_user(user_id)
        except ValueError:
            raise NotFoundError(f"User with ID {user_id} not found")
        except IntegrityError as e:
            self.session.rollback()
            if hasattr(e.orig, "pgcode") and e.orig.pgcode == "23503":
                raise ForeignKeyConstraintError(f"User is still referenced: {str(e.orig)}") from e
            raise