from datetime import datetime

from app.src.domain.entities.tag import Tag
from app.src.domain.interface_repositories.tag_repository import TagRepository


class CreateTagWithRoomLinkUseCase:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag: Tag, room_id: int, start_at: datetime | None, end_at: datetime | None = None) -> Tag:
        if not start_at:
            start_at = datetime.now()
    
        return self.tag_repository.create_with_room_link(tag, room_id, start_at, end_at)
    