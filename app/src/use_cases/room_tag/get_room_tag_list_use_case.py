import math
import logging
from dataclasses import dataclass

from app.src.common.utils import decode, encode
from app.src.domain.entities.room_tag import RoomTag 
from app.src.domain.interface_repositories.room_tag_repository import RoomTagRepository


logger = logging.getLogger(__name__)

@dataclass
class PaginatedRoomTag:
    room_tag: list[RoomTag]
    total: int| None
    chunk_size: int| None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetRoomTagListUseCase:
    def __init__(self, room_tag_repository: RoomTagRepository):
        self.room_tag_repository = room_tag_repository

    def execute(self, cursor: str | None, limit: int | None = None, active_only: bool = False) -> PaginatedRoomTag:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "Room tag pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        room_tag, total, first_room_tag, last_room_tag = self.room_tag_repository.paginate_roomtag(
            decoded_cursor, (limit + 1), active_only=active_only
        )
        
        next_room_tag = None
        if len(room_tag) == (limit + 1):
            next_room_tag = room_tag.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_room_tag.id} if first_room_tag else None
        last_cursor = {"id": last_room_tag.id} if last_room_tag else None
        next_cursor = {"id": next_room_tag.id} if next_room_tag else None

        return PaginatedRoomTag(
            room_tag=room_tag,
            total=total,
            chunk_size=len(room_tag),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
