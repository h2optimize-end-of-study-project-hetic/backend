from datetime import datetime

from app.src.domain.entities.tag import Tag
from app.src.domain.interface_repositories.tag_repository import TagRepository
from app.src.domain.interface_repositories.room_tag_repository import RoomTagRepository


class UpdateTagWithRoomLinkUseCase:
    def __init__(self, tag_repository: TagRepository, room_tag_repository: RoomTagRepository):
        self.tag_repository = tag_repository
        self.room_tag_repository = room_tag_repository

    def execute(
        self,
        tag_id: int,
        update_data: dict,
        room_id: int | None,
        start_at: datetime | None,
        end_at: datetime | None,
        unlink: bool = False,
    ) -> Tag:
        updated_tag = self.tag_repository.update_tag(tag_id, update_data)

        if room_id:
            if not start_at:
                start_at = datetime.now()
            self.room_tag_repository.update_roomtag_by_tag_id_room_id(tag_id, room_id, start_at, end_at)

        return self.tag_repository.select_tag_by_id(tag_id, with_rooms=True)
