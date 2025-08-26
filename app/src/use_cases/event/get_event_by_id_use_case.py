from app.src.domain.entities.event import Event
from app.src.domain.interface_repositories.event_repository import EventRepository


class GetEventByIdUseCase:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def execute(self, event_id: int) -> Event:
        event = self.event_repository.select_event_by_id(event_id)

        return event
