from dataclasses import asdict, dataclass
from datetime import datetime

from dateutil.parser import parse as parse_datetime


@dataclass
class Room:
    id: int | None
    name: str
    description: str | None
    floor: int
    building_id: int
    area: float
    shape: list[list[float]]
    capacity: int
    start_at: datetime | None
    end_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None = None

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
            floor=int(data["floor"]),
            building_id=int(data["building_id"]),
            area=float(data["area"]),
            shape=data.get("shape", []),
            capacity=int(data["capacity"]),
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
