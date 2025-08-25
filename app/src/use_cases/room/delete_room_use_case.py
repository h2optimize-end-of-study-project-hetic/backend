from app.src.domain.interface_repositories.room_repository import RoomRepository


class DeleteRoomUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, room_id: int) -> bool:
        return self.room_repository.delete_room(room_id)
