from app.src.common.exception import NotFoundError

class GetUserByIdUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id: int):
        user = self.user_repository.select_user_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User with ID {user_id} not found")
        return user