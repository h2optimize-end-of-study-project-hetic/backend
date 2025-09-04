from dataclasses import dataclass, asdict
from datetime import datetime
from dateutil.parser import parse as parse_datetime

@dataclass
class RoomTag:
    id: int | None
    tag_id: int
    room_id: int
    start_at: datetime | None = None
    end_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict) -> "RoomTag":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return RoomTag(
            id=data.get("id"),
            tag_id=int(data["tag_id"]),
            room_id=int(data["room_id"]),
            start_at=safe_parse(data.get("start_at")),
            end_at=safe_parse(data.get("end_at")),
            created_at=safe_parse(data.get("created_at")),
            updated_at=safe_parse(data.get("updated_at")),
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        for field in ["created_at", "updated_at", "start_at", "end_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
