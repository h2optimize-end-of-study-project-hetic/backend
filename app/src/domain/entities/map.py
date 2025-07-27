from datetime import datetime
from dataclasses import asdict, dataclass

from dateutil.parser import parse as parse_datetime

@dataclass
class Map:
    id: int | None
    building_id : int | None
    filename: str
    path: str
    width: int | None
    length : int | None
    created_at: datetime | None
    updated_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict) -> "Map":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return Map(
            id=data.get("id"),
            building_id=data.get("building_id"),
            filename=data["filename"],
            path=data.get("path"),
            width=data.get("width"),
            length=data.get("length"),
            created_at=safe_parse(data.get("created_at")),
            updated_at=safe_parse(data.get("updated_at")),
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
