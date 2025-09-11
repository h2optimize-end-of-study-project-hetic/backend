from dataclasses import asdict, dataclass
from datetime import datetime

from dateutil.parser import parse as parse_datetime

@dataclass
class Room:
    id: int | None
    name: str
    description: str | None
    floor: int| None
    building_id: int
    area: float| None
    shape: list[list[float]]
    capacity: int| None
    start_at: datetime | None
    end_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None = None
    tags: list | None = None   

    @staticmethod
    def from_dict(data: dict) -> "Room":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return Room(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description"),
            floor=int(data["floor"]) if data["floor"] else None,
            building_id=int(data["building_id"]),
            area=float(data["area"]) if data["area"] else None,
            shape=data.get("shape", []),
            capacity=int(data["capacity"])if data["capacity"] else None,
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

        if self.tags:
            serialized_tags = []
            for tag in self.tags:
                if isinstance(tag, dict):
                    serialized_tags.append(tag)
                elif hasattr(tag, "to_dict"):
                    serialized_tags.append(tag.to_dict())
                else:
                    serialized_tags.append(tag)
            data["tags"] = serialized_tags
        else:
            data["tags"] = None

        return data
