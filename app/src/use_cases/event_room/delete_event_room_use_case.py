from app.src.domain.interface_repositories.event_room_repository import EventRoomRepository


class DeleteEventRoomUseCase:
    def __init__(self, event_room_repository: EventRoomRepository):
        self.event_room_repository = event_room_repository

    def execute(self, event_room_id: int) -> bool:
        return self.event_room_repository.delete_event_room(event_room_id)
