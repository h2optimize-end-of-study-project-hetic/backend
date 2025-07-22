from datetime import datetime
from dataclasses import asdict, dataclass

from dateutil.parser import parse as parse_datetime


@dataclass
class Tag:
    id: int | None
    name: str
    description: str | None
    source_address: str
    created_at: datetime | None
    updated_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict) -> "Tag":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return Tag(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description"),
            source_address=data["source_address"],
            created_at=safe_parse(data.get("created_at")),
            updated_at=safe_parse(data.get("updated_at")),
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
