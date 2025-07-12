from datetime import datetime
from typing import Optional, Any, Dict
from dataclasses import dataclass, asdict
from dateutil.parser import parse as parse_datetime

@dataclass
class Building:
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    room_count: Optional[int]
    street_number: Optional[str]
    street_name: Optional[str]
    postal_code: Optional[str]
    city: Optional[str]
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Building":
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

    def to_dict(self) -> Dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data