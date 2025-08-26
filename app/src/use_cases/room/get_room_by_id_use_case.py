from app.src.domain.entities.room import Room
from app.src.domain.interface_repositories.room_repository import RoomRepository


class GetRoomByIdUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, room_id: int) -> Room:
        room = self.room_repository.select_room_by_id(room_id)

        return room
