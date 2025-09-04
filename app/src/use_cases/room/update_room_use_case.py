from app.src.domain.entities.room import Room
from app.src.domain.interface_repositories.room_repository import RoomRepository


class UpdateRoomUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, room_id: int, room_data: dict) -> Room:
        return self.room_repository.update_room(room_id, room_data)
