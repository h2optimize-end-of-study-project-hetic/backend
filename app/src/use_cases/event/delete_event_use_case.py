from app.src.domain.interface_repositories.event_repository import EventRepository


class DeleteEventUseCase:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def execute(self, event_id: int) -> bool:
        return self.event_repository.delete_event(event_id)
