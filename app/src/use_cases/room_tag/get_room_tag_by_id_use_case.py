from app.src.domain.entities.room_tag import RoomTag 
from app.src.domain.interface_repositories.room_tag_repository import RoomTagRepository


class GetRoomTagByIdUseCase:
    def __init__(self, room_tag_repository: RoomTagRepository):
        self.room_tag_repository = room_tag_repository

    def execute(self, room_tag_id: int) -> RoomTag:
        room_tag = self.room_tag_repository.select_roomtag_by_id(room_tag_id)

        return room_tag
