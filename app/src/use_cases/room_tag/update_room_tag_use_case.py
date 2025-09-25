from app.src.domain.entities.room_tag import RoomTag 
from app.src.domain.interface_repositories.room_tag_repository import RoomTagRepository


class UpdateRoomTagUseCase:
    def __init__(self, room_tag_repository: RoomTagRepository):
        self.room_tag_repository = room_tag_repository

    def execute(self, room_tag_id: int, room_tag_data: dict) -> RoomTag:
        return self.room_tag_repository.update_roomtag(room_tag_id, room_tag_data)
