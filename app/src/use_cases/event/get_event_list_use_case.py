import logging
import math
from dataclasses import dataclass

from app.src.domain.entities.event import Event
from app.src.common.utils import decode, encode
from app.src.domain.interface_repositories.event_repository import EventRepository

logger = logging.getLogger(__name__)

@dataclass
class PaginatedEvent:
    events: list[Event]
    total: int| None
    chunk_size: int| None
    chunk_count: int | None
    current_cursor: str | None
    first_cursor: str | None
    last_cursor: str | None
    next_cursor: str | None


class GetEventListUseCase:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def execute(self, cursor: str | None, limit: int | None = None) -> PaginatedEvent:
        limit = limit or 20

        decoded_cursor = None
        if cursor:
            decoded_cursor = decode(cursor, "Event pagination cursor")
            decoded_cursor = decoded_cursor.get("id") if decoded_cursor else None

        events, total, first_event, last_event = self.event_repository.paginate_events(decoded_cursor, (limit + 1))

        next_event = None
        if len(events) == (limit + 1):
            next_event = events.pop(-1)

        chunk_count = math.ceil(total / limit) if limit else 1

        first_cursor = {"id": first_event.id} if first_event else None
        last_cursor = {"id": last_event.id} if last_event else None
        next_cursor = {"id": next_event.id} if next_event else None

        return PaginatedEvent(
            events=events,
            total=total,
            chunk_size=len(events),
            chunk_count=chunk_count,
            current_cursor=encode({"id": decoded_cursor}) if decoded_cursor else encode(first_cursor) if first_cursor else None,
            first_cursor=encode(first_cursor) if first_cursor else None,
            last_cursor=encode(last_cursor) if last_cursor else None,
            next_cursor=encode(next_cursor) if next_cursor else None,
        )
