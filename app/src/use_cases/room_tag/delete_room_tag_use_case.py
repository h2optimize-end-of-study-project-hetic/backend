from app.src.domain.interface_repositories.room_tag_repository import RoomTagRepository


class DeleteRoomTagUseCase:
    def __init__(self, room_tag_repository: RoomTagRepository):
        self.room_tag_repository = room_tag_repository

    def execute(self, room_tag_id: int) -> bool:
        return self.room_tag_repository.delete_roomtag(room_tag_id)
