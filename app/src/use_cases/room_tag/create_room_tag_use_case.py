from datetime import datetime
import logging

from app.src.domain.entities.room_tag import RoomTag 
from app.src.domain.interface_repositories.room_tag_repository import RoomTagRepository

logger = logging.getLogger(__name__)

class CreateRoomTagUseCase:
    def __init__(self, room_tag_repository: RoomTagRepository):
        self.room_tag_repository = room_tag_repository

    def execute(self, room_tag: RoomTag) -> RoomTag:

        if not room_tag.start_at:
            room_tag.start_at = datetime.now()

        return self.room_tag_repository.create_roomtag(room_tag)
