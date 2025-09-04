from app.src.domain.entities.event import Event
from app.src.domain.interface_repositories.event_repository import EventRepository


class CreateEventUseCase:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def execute(self, event: Event) -> Event:
        return self.event_repository.create_event(event)
