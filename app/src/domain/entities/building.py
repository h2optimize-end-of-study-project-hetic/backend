from datetime import datetime
from dataclasses import asdict, dataclass

from dateutil.parser import parse as parse_datetime

@dataclass
class Building:
    id: int | None
    name : str | None
    description : str | None
    room_count : int | None
    street_number : str | None
    street_name : str | None
    postal_code : str | None
    city : str | None
    country : str | None
    latitude : float | None
    longitude : float | None
    created_at: datetime | None
    updated_at: datetime | None = None

    @staticmethod
    def from_dict(data: dict) -> "Building":
        def safe_parse(value):
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                return parse_datetime(value)
            return None

        return Building(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            room_count=data.get("room_count"),
            street_number=safe_parse(data.get("street_number")),
            street_name=safe_parse(data.get("street_name")),
            postal_code=safe_parse(data.get("postal_code")),
            city=safe_parse(data.get("city")),
            country=safe_parse(data.get("country")),
            latitude=safe_parse(data.get("latitude")),
            longitude=safe_parse(data.get("longitude")),
            created_at=safe_parse(data.get("created_at")),
            updated_at=safe_parse(data.get("updated_at")),
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        for field in ["created_at", "updated_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        return data
