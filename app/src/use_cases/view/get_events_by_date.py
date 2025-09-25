from app.src.infrastructure.db.repositories.view_repository_sql import EventsByDateRepository
from app.src.common.exception import NotFoundError
from datetime import date as Date

class GetEventsByDateUseCase:
    def __init__(self, repository: EventsByDateRepository):
        self.repository = repository

    def execute(self, date: Date):
        results = self.repository.get_events_by_date(date)
        if not results:
            raise NotFoundError("Events by date", date)

        return results

