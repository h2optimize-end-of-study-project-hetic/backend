import logging
import math
from dataclasses import dataclass

from app.src.domain.entities.event_room import EventRoom
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.event_room_repository import EventRoomRepository

logger = logging.getLogger(__name__)

@dataclass
class PaginatedEventRoom:
    event_rooms: list[EventRoom]
    total: int| None
    chunk_size: int| None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetEventRoomListUseCase:
    def __init__(self, event_room_repository: EventRoomRepository):
        self.event_room_repository = event_room_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedEventRoom:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "EventRoom pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        event_rooms, total, first_event_room, last_event_room = self.event_room_repository.paginate_event_rooms(decoded_cursor, (limit + 1))

        next_event_room = None
        if len(event_rooms) == (limit + 1):
            next_event_room = event_rooms.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_event_room.id} if first_event_room else None
        last_cursor = {"id": last_event_room.id} if last_event_room else None
        next_cursor = {"id": next_event_room.id} if next_event_room else None

        return PaginatedEventRoom(
            event_rooms=event_rooms,
            total=total,
            chunk_size=len(event_rooms),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
