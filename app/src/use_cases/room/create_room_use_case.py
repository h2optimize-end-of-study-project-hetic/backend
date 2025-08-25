from app.src.domain.entities.room import Room
from app.src.domain.interface_repositories.room_repository import RoomRepository


class CreateRoomUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, room: Room) -> Room:
        return self.room_repository.create_room(room)
