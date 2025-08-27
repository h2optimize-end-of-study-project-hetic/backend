from app.src.domain.entities.event_room import EventRoom
from app.src.domain.interface_repositories.event_room_repository import EventRoomRepository


class GetEventRoomByIdUseCase:
    def __init__(self, event_room_repository: EventRoomRepository):
        self.event_room_repository = event_room_repository

    def execute(self, event_room_id: int) -> EventRoom:
        event_room = self.event_room_repository.select_event_room_by_id(event_room_id)

        return event_room
