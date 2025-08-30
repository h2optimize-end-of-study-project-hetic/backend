from datetime import datetime
from dataclasses import asdict, dataclass

from dateutil.parser import parse as parse_datetime

@dataclass
class EventRoom:
    id: int | None
    room_id : int | None
    event_id : int | None
    is_finished : bool |None
    start_at: datetime | None
    end_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict) -> "EventRoom":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return EventRoom(
            id=data.get("id"),
            room_id=data.get("room_id"),
            event_id=data.get("event_id"),
            is_finished=data.get("is_finished"),
            start_at=safe_parse(data.get("start_at")),
            end_at=safe_parse(data.get("end_at")),
            created_at=safe_parse(data.get("created_at")),
            updated_at=safe_parse(data.get("updated_at")),
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
