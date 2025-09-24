from app.src.common.exception import NotFoundError
from app.src.infrastructure.db.repositories.view_repository_sql import UserEventRepository

class GetEventsForUserUseCase:
    def __init__(self, repository: UserEventRepository):
        self.repository = repository

    def execute(self, user_id: int):
        results = self.repository.get_events_for_user(user_id)
        if not results:
            raise NotFoundError("User", user_id)
        return results
