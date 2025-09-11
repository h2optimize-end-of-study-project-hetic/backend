import logging
import math
from dataclasses import dataclass

from app.src.domain.entities.room import Room
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.room_repository import RoomRepository

logger = logging.getLogger(__name__)

@dataclass
class PaginatedRoom:
    rooms: list[Room]
    total: int| None
    chunk_size: int| None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetRoomWithTagListUseCase:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedRoom:
        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "Room pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        rooms, total, first_room, last_room = self.room_repository.paginate_rooms_with_tags(decoded_cursor, (limit + 1))

        next_room = None
        if len(rooms) == (limit + 1):
            next_room = rooms.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_room.id} if first_room else None
        last_cursor = {"id": last_room.id} if last_room else None
        next_cursor = {"id": next_room.id} if next_room else None

        return PaginatedRoom(
            rooms=rooms,
            total=total,
            chunk_size=len(rooms),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
