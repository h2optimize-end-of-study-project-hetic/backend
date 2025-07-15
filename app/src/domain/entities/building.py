from typing import Any
from datetime import datetime
from dataclasses import asdict, dataclass

from dateutil.parser import parse as parse_datetime


@dataclass
class Building:
    id: int | None
    name: str | None
    description: str | None
    room_count: int | None
    street_number: str | None
    street_name: str | None
    postal_code: str | None
    city: str | None
    country: str | None
    latitude: float | None
    longitude: float | None
    created_at: datetime | None
    updated_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Building":
        return Building(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            room_count=data.get("room_count"),
            street_number=data.get("street_number"),
            street_name=data.get("street_name"),
            postal_code=data.get("postal_code"),
            city=data.get("city"),
            country=data.get("country"),
            latitude=float(data["latitude"]) if data.get("latitude") is not None else None,
            longitude=float(data["longitude"]) if data.get("longitude") is not None else None,
            created_at=parse_datetime(data["created_at"]) if data.get("created_at") else None,
            updated_at=parse_datetime(data["updated_at"]) if data.get("updated_at") else None,
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
