from app.src.domain.entities.event_room import EventRoom
from app.src.domain.interface_repositories.event_room_repository import EventRoomRepository


class CreateEventRoomUseCase:
    def __init__(self, event_room_repository: EventRoomRepository):
        self.event_room_repository = event_room_repository

    def execute(self, event_room: EventRoom) -> EventRoom:
        return self.event_room_repository.create_event_room(event_room)
